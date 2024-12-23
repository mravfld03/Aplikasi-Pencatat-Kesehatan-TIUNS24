import tkinter as tk
import tkinter.messagebox as msgbox
from PIL import Image, ImageTk
import json
import os
import matplotlib.pyplot as plt
from datetime import date, datetime, timedelta

# Nama file database
database_file = "user_database.json"

# Fungsi untuk memuat database dari file JSON
def load_database():
    if os.path.exists(database_file):
        with open(database_file, "r") as file:
            return json.load(file)
    return {}  # Jika file tidak ditemukan, kembalikan dictionary kosong

# Fungsi untuk menyimpan database ke file JSON
def save_database(data):
    with open(database_file, "w") as file:
        json.dump(data, file, indent=4)

# Database pengguna
user_data = load_database()

def clean_old_data(username):
    if username not in user_data:
        return

    # Tentukan batas waktu berdasarkan target pengguna
    target = user_data[username].get("target", "Mingguan")
    days_limit = 7 if target == "Mingguan" else 30  # 7 hari untuk mingguan, 30 hari untuk bulanan

    # Tanggal saat ini
    today = date.today()

    # Bersihkan data lama untuk setiap kategori data harian
    for category in ["data_harian_steps", "data_harian_sleep", "data_harian_water"]:
        if category in user_data[username]:
            keys_to_delete = []
            for data_date in list(user_data[username][category].keys()):
                try:
                    # Konversi string tanggal ke objek date
                    data_date_obj = datetime.strptime(data_date, "%Y-%m-%d").date()
                    
                    # Periksa jika data lebih lama dari batas waktu
                    if (today - data_date_obj).days > days_limit:
                        keys_to_delete.append(data_date)
                except ValueError:
                    continue  # Lewati data yang tidak sesuai format tanggal

            # Hapus data lama dari database
            for key in keys_to_delete:
                del user_data[username][category][key]

    # Simpan database yang diperbarui
    save_database(user_data)

# Fungsi untuk menyesuaikan ukuran dan posisi tengah jendela
def center_window(window, width=1280, height=720):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

# Fungsi untuk jendela login
def login_window():
    loginWindow = tk.Tk()
    loginWindow.title("Login")
    
    loginWindow.state('zoomed')

    # Pasang gambar background
    bg_image = Image.open(r'images/bgutama.jpg')  # Pastikan file ini ada di direktori yang sama
    bg_image = bg_image.resize((loginWindow.winfo_screenwidth(), loginWindow.winfo_screenheight()))
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(loginWindow, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)

    frame = tk.Frame(loginWindow, bg="pink", padx=5, pady=5)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(text=f"Selamat datang di Aplikasi Pencatat Kesehatan Harian", font=("Arial", 24), bg="pink").pack(pady=100)
    tk.Label(frame, text="Username:", bg="white").grid(row=0, column=0, padx=5, pady=5)
    tk.Label(frame, text="Password:", bg="white").grid(row=1, column=0, padx=5, pady=5)

    username = tk.Entry(frame)
    password = tk.Entry(frame, show="*")
    username.grid(row=0, column=1, padx=5, pady=5)
    password.grid(row=1, column=1, padx=5, pady=5)
    
    def toggle_password():
        if password.cget('show') == '*':
            password.config(show='')
            toggle_button.config(text='👁️')  # Ganti simbol mata
        else:
            password.config(show='*')
            toggle_button.config(text='👁️')  # Ganti simbol mata
            
    toggle_button = tk.Button(frame, text="👁️", command=toggle_password, bg="white")
    toggle_button.grid(row=1, column=2, padx=5, pady=5)

    def login_action():
        uname = username.get()
        pwd = password.get()
        if uname in user_data and user_data[uname]["password"] == pwd:
            # Bersihkan data lama
            clean_old_data(uname)
            
            msgbox.showinfo("Login Berhasil", "Selamat datang, " + uname)
            loginWindow.destroy()
            open_main_window(uname)
        else:
            msgbox.showerror("Login Gagal", "Username atau password salah.")

    def switch_to_register():
        loginWindow.destroy()
        register_window()

    tk.Button(frame, text="Login", command=login_action).grid(row=2, column=0, padx=5, pady=10)
    tk.Button(frame, text="Daftar jika belum memiliki akun", command=switch_to_register).grid(row=2, column=1, padx=5, pady=10)

    # Sesuaikan ukuran jendela
    center_window(loginWindow, 1280, 720)
    loginWindow.mainloop()

# Fungsi untuk jendela registrasi
def register_window():
    registerWindow = tk.Tk()
    registerWindow.title("Daftar")
    
    registerWindow.state('zoomed')

    # Pasang gambar background
    bg_image = Image.open(r'images/bgutama.jpg')
    bg_image = bg_image.resize((registerWindow.winfo_screenwidth(), registerWindow.winfo_screenheight()))
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(registerWindow, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)

    frame = tk.Frame(registerWindow, bg="pink", padx=20, pady=20)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(frame, text="Username:", bg="white").grid(row=0, column=0, padx=5, pady=5)
    tk.Label(frame, text="Password:", bg="white").grid(row=1, column=0, padx=5, pady=5)
    tk.Label(frame, text="Target yang diinginkan:", bg="white").grid(row=2, column=0, padx=5, pady=5)
    tk.Label(frame, text="Jumlah langkah/hari:", bg="white").grid(row=3, column=0, padx=5, pady=5)
    tk.Label(frame, text="Jam tidur/hari:", bg="white").grid(row=4, column=0, padx=5, pady=5)
    tk.Label(frame, text="Jumlah gelas air minum(per 250ml)/hari:", bg="white").grid(row=5, column=0, padx=5, pady=5)

    username = tk.Entry(frame)
    password = tk.Entry(frame, show="*")
    langkah = tk.Entry(frame)
    jamTidur = tk.Entry(frame)
    gelasair = tk.Entry(frame)
    username.grid(row=0, column=1, padx=5, pady=5)
    password.grid(row=1, column=1, padx=5, pady=5)
    langkah.grid(row=3, column=1, padx=5, pady=5)
    jamTidur.grid(row=4, column=1, padx=5, pady=5)
    gelasair.grid(row=5, column=1, padx=5, pady=5)

    # Daftar pilihan untuk target yang diinginkan
    options = ["Mingguan", "Bulanan"]
    target_variable = tk.StringVar(registerWindow)
    target_variable.set(options[0])  # Set default pilihan

    target_menu = tk.OptionMenu(frame, target_variable, *options)
    target_menu.grid(row=2, column=1, padx=5, pady=5)
    
    def toggle_password():
        if password.cget('show') == '*':
            password.config(show='')
            toggle_button.config(text='👁️')  # Ganti simbol mata
        else:
            password.config(show='*')
            toggle_button.config(text='👁️')  # Ganti simbol mata
            
    toggle_button = tk.Button(frame, text="👁️", command=toggle_password, bg="white")
    toggle_button.grid(row=1, column=2, padx=5, pady=5)
    
    def validate_number(entry, field_name):
        value = entry.get()
        if not value.isdigit():
            msgbox.showerror("Input Tidak Valid", f"{field_name} harus berupa angka.")
            entry.delete(0, tk.END)  # Hapus input yang tidak valid

    # Tambahkan validasi input angka
    langkah.bind("<FocusOut>", lambda e: validate_number(langkah, "Langkah"))
    jamTidur.bind("<FocusOut>", lambda e: validate_number(jamTidur, "Jam Tidur"))
    gelasair.bind("<FocusOut>", lambda e: validate_number(gelasair, "Gelas Air"))

    def register_action():
        uname = username.get()
        pwd = password.get()
        target = target_variable.get()
        steps = langkah.get()
        sleep = jamTidur.get()
        water = gelasair.get()

        if uname in user_data:
            msgbox.showerror("Gagal Daftar", "Username sudah terdaftar.")
        elif uname and pwd:
            user_data[uname] = {
                "password": pwd,
                "target": target,
                "langkah": steps,
                "jamTidur": sleep,
                "gelasair": water
            }
            save_database(user_data)
            msgbox.showinfo("Berhasil Daftar", "Akun berhasil dibuat!")
            registerWindow.destroy()
            login_window()
        else:
            msgbox.showerror("Gagal Daftar", "Username dan password tidak boleh kosong.")

    tk.Button(frame, text="Daftar", command=register_action).grid(row=6, column=0, padx=5, pady=10)
    tk.Button(frame, text="Batal", command=lambda: [registerWindow.destroy(), login_window()]).grid(row=6, column=1, padx=5, pady=10)

    center_window(registerWindow, 1280, 720)
    registerWindow.mainloop()

# Fungsi untuk jendela utama setelah login
def open_main_window(username):
    global bg_photo
    
    mainWindow = tk.Tk()
    mainWindow.title("Aplikasi Pencatat Kesehatan Harian")
    mainWindow.state('zoomed')
    
    bg_image = Image.open(r'images/bgutama.jpg')
    bg_image = bg_image.resize((mainWindow.winfo_screenwidth(), mainWindow.winfo_screenheight()))
    bg_photo = ImageTk.PhotoImage(bg_image)
    
    bg_label = tk.Label(mainWindow, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)

    frame = tk.Frame(mainWindow, bg="pink", padx=20, pady=20)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(text=f"Aplikasi Pencatat Kesehatan Harian", font=("Arial", 24), bg="pink").pack(pady=100)
    tk.Label(frame, text=f"Selamat Datang, {username}!", font=("Arial", 16), bg="lightblue").pack(pady=10)
    tk.Label(frame, text=f"Target Anda: {user_data[username]['target']}", font=("Arial", 12), bg="lightblue").pack(pady=5)
    
    def switch_input_harian():
        mainWindow.withdraw()
        input_harian_window(mainWindow, username)
    
    def switch_to_lihat_progress():
        mainWindow.destroy()
        lihat_progress_window(username)
        
    def confirm_exit():
        response = msgbox.askyesno("Konfirmasi Keluar", "Anda yakin ingin keluar?")
        if response:
            mainWindow.destroy()
            
    tk.Button(frame, text="Input Data Harian", command=switch_input_harian).pack(padx=5)
    tk.Button(frame, text="Lihat Progress", command=switch_to_lihat_progress).pack(padx=5)
    tk.Button(frame, text="Keluar", command=confirm_exit).pack(pady=15)

    center_window(mainWindow, 1280, 720)
    mainWindow.mainloop()

def input_harian_window(parent_window, username):
    inputWindow = tk.Toplevel(parent_window)
    inputWindow.title("Input Data Harian")
    
    # Dapatkan ukuran layar
    screen_width = parent_window.winfo_screenwidth()
    screen_height = parent_window.winfo_screenheight()
    
    # Muat gambar latar belakang
    bg_image = Image.open(r'images/bgutama.jpg')
    bg_image = bg_image.resize((screen_width, screen_height))
    bg_photo = ImageTk.PhotoImage(bg_image)
    
    # Label untuk latar belakang
    bg_label = tk.Label(inputWindow, image=bg_photo)
    bg_label.image = bg_photo  # Simpan referensi
    bg_label.place(relwidth=1, relheight=1)
    frame = tk.Frame(inputWindow, bg="pink", padx=20, pady=20)
    frame.place(relx=0.5, rely=0.5, anchor="center")
    
    tk.Label(frame, text="Selamat Datang!", font=("Arial", 16), bg="lightblue").pack(pady=10)
    tk.Label(frame, text="Input Data Anda", font=("Arial", 12), bg="lightblue").pack(pady=5)
    
    def switch_to_input_steps():
        input_steps_window(username)
    
    tk.Button(frame, text="Langkah", command=switch_to_input_steps).pack(padx=5)
        
    def switch_to_input_sleep():
        input_sleep_window(username)
        
    tk.Button(frame, text="Jam Tidur", command=switch_to_input_sleep).pack(padx=5)
    
    def switch_to_input_water():
        input_water_window(username)
    
    tk.Button(frame, text="Gelas Air", command=switch_to_input_water).pack(padx=5)
    
    def inputharian_ke_main_window():
        inputWindow.destroy()
        parent_window.deiconify()
        parent_window.state('zoomed')
    
    tk.Button(frame, text="Kembali", command=inputharian_ke_main_window).pack(pady=15)
    
    center_window(inputWindow, 640, 320)

def input_steps_window(username):
    stepsWindow = tk.Toplevel()
    stepsWindow.title("Input Langkah")

    frame = tk.Frame(stepsWindow, bg="pink", padx=5, pady=5)
    frame.place(relx=0.5, rely=0.5, anchor="center")
    
    last_steps_label = tk.Label(frame, text="", font=("Arial", 10), bg="pink", fg="blue")
    last_steps_label.grid(row=2, column=0, columnspan=2, pady=14)
    
    today = str(date.today())  # Dapatkan tanggal hari ini dalam format string (YYYY-MM-DD)
    
    if username in user_data and "data_harian_steps" in user_data[username]:
        if today in user_data[username]["data_harian_steps"]:
            last_steps = user_data[username]["data_harian_steps"][today]
            last_time = user_data[username]["data_harian_steps"].get(f"{today}_time", "Tidak diketahui")
            last_steps_label.config(text=f"Data terakhir: {last_steps} langkah pada {last_time}")
        else:
            last_steps_label.config(text="Belum ada data langkah untuk hari ini.")
    else:
        last_steps_label.config(text="Belum ada data langkah sebelumnya.")
    
    tk.Label(frame, text="Masukkan Jumlah Langkah:", font=("Arial", 14), bg="pink").grid(row=0, column=0, columnspan=2, pady=10)

    # Input jumlah langkah
    steps_var = tk.StringVar()
    tk.Entry(frame, textvariable=steps_var, width=20).grid(row=1, column=0, columnspan=2, pady=5)

    def save_steps():
        try:
            steps = int(steps_var.get())

            # Bersihkan data lama
            clean_old_data(username)
            
            if username not in user_data:
                msgbox.showerror("Error", f"Username '{username}' tidak ditemukan.")
                return

            # Pastikan "data_harian" ada dalam data user
            if "data_harian_steps" not in user_data[username]:
                user_data[username]["data_harian_steps"] = {}

            # Simpan data langkah untuk tanggal hari ini
            now = datetime.now().strftime("%H:%M:%S")  # Waktu sekarang
            user_data[username]["data_harian_steps"][today] = steps
            user_data[username]["data_harian_steps"][f"{today}_time"] = now
            save_database(user_data)
            
            last_steps_label.config(text=f"Data terakhir: {steps} langkah pada {now}")

            target_steps = int(user_data[username].get("langkah", 0))  # Ambil target langkah dari database
            if steps < target_steps:
                warning_text = f"Peringatan: Anda belum mencapai target harian {target_steps} langkah!"
                tk.Label(frame, text=warning_text, bg="pink", fg="red", wraplength=300).grid(row=5, column=0, columnspan=2, pady=10)
            else:
                success_text = "Selamat! Anda telah mencapai target harian."
                tk.Label(frame, text=success_text, bg="pink", fg="green", wraplength=300).grid(row=5, column=0, columnspan=2, pady=10)
            
            tk.Label(frame, text="Data berhasil disimpan!", bg="pink", fg="green").grid(row=3, column=0, columnspan=2, pady=10)
            steps_var.set("")  # Bersihkan input
        except ValueError:
            tk.Label(frame, text="Masukkan angka yang valid!", bg="pink", fg="red").grid(row=3, column=0, columnspan=2, pady=10)

    # Tombol untuk menyimpan langkah
    tk.Button(frame, text="Simpan", command=save_steps).grid(row=4, column=0, pady=10)
    tk.Button(frame, text="Tutup", command=stepsWindow.destroy).grid(row=4, column=1, pady=10)
    
    center_window(stepsWindow, 640, 320)
    stepsWindow.mainloop()

def input_sleep_window(username):
    sleepWindow = tk.Toplevel()
    sleepWindow.title("Input Jam Tidur")
    
    frame = tk.Frame(sleepWindow, bg="pink", padx=5, pady=5)
    frame.place(relx=0.5, rely=0.5, anchor="center")
    
    last_sleep_label = tk.Label(frame, text="", font=("Arial", 10), bg="pink", fg="blue")
    last_sleep_label.grid(row=2, column=0, columnspan=2, pady=14)
    
    today = str(date.today())  # Dapatkan tanggal hari ini dalam format string (YYYY-MM-DD)
    
    if username in user_data and "data_harian_sleep" in user_data[username]:
        if today in user_data[username]["data_harian_sleep"]:
            last_sleep = user_data[username]["data_harian_sleep"][today]
            last_time = user_data[username]["data_harian_sleep"].get(f"{today}_time", "Tidak diketahui")
            last_sleep_label.config(text=f"Data terakhir: {last_sleep} jam tidur pada {last_time}")
        else:
            last_sleep_label.config(text="Belum ada data jam tidur untuk hari ini.")
    else:
        last_sleep_label.config(text="Belum ada data jam tidur sebelumnya.")
    
    tk.Label(frame, text="Masukkan Jam Tidur:", font=("Arial", 14), bg="pink").grid(row=0, column=0, columnspan=2, pady=10)

    # Input jumlah jam tidur
    sleep_var = tk.StringVar()
    tk.Entry(frame, textvariable=sleep_var, width=20).grid(row=1, column=0, columnspan=2, pady=5)

    def save_sleep():
        try:
            sleep = int(sleep_var.get())

            # Bersihkan data lama
            clean_old_data(username)

            if username not in user_data:
                msgbox.showerror("Error", f"Username '{username}' tidak ditemukan.")
                return

            # Pastikan "data_harian" ada dalam data user
            if "data_harian_sleep" not in user_data[username]:
                user_data[username]["data_harian_sleep"] = {}

            # Simpan data jam tidur untuk tanggal hari ini
            now = datetime.now().strftime("%H:%M:%S")  # Waktu sekarang
            user_data[username]["data_harian_sleep"][today] = sleep
            user_data[username]["data_harian_sleep"][f"{today}_time"] = now
            save_database(user_data)
            
            last_sleep_label.config(text=f"Data terakhir: {sleep} jam tidur pada {now}")

            target_sleep = int(user_data[username].get("jamTidur", 0))  # Ambil target langkah dari database
            if sleep < target_sleep:
                warning_text = f"Peringatan: Anda belum mencapai target harian {target_sleep} jam tidur!"
                tk.Label(frame, text=warning_text, bg="pink", fg="red", wraplength=300).grid(row=5, column=0, columnspan=2, pady=10)
            else:
                success_text = "Selamat! Anda telah mencapai target harian."
                tk.Label(frame, text=success_text, bg="pink", fg="green", wraplength=300).grid(row=5, column=0, columnspan=2, pady=10)
            
            tk.Label(frame, text="Data berhasil disimpan!", bg="pink", fg="green").grid(row=3, column=0, columnspan=2, pady=10)
            sleep_var.set("")  # Bersihkan input
        except ValueError:
            tk.Label(frame, text="Masukkan angka yang valid!", bg="pink", fg="red").grid(row=3, column=0, columnspan=2, pady=10)

    # Tombol untuk menyimpan jam tidur
    tk.Button(frame, text="Simpan", command=save_sleep).grid(row=4, column=0, pady=10)
    tk.Button(frame, text="Tutup", command=sleepWindow.destroy).grid(row=4, column=1, pady=10)
    
    center_window(sleepWindow, 640, 320)
    sleepWindow.mainloop()
    
def input_water_window(username):
    waterWindow = tk.Toplevel()
    waterWindow.title("Input Gelas Air")
    
    frame = tk.Frame(waterWindow, bg="pink", padx=5, pady=5)
    frame.place(relx=0.5, rely=0.5, anchor="center")
    
    last_water_label = tk.Label(frame, text="", font=("Arial", 10), bg="pink", fg="blue")
    last_water_label.grid(row=2, column=0, columnspan=2, pady=14)
    
    today = str(date.today())  # Dapatkan tanggal hari ini dalam format string (YYYY-MM-DD)
    
    if username in user_data and "data_harian_water" in user_data[username]:
        if today in user_data[username]["data_harian_water"]:
            last_water = user_data[username]["data_harian_water"][today]
            last_time = user_data[username]["data_harian_water"].get(f"{today}_time", "Tidak diketahui")
            last_water_label.config(text=f"Data terakhir: {last_water} gelas air pada {last_time}")
        else:
            last_water_label.config(text="Belum ada data gelas air untuk hari ini.")
    else:
        last_water_label.config(text="Belum ada data gelas air sebelumnya.")
    
    tk.Label(frame, text="Masukkan Jumlah Gelas Air(per 250ml):", font=("Arial", 14), bg="pink").grid(row=0, column=0, columnspan=2, pady=10)

    # Input jumlah gelas air
    water_var = tk.StringVar()
    tk.Entry(frame, textvariable=water_var, width=20).grid(row=1, column=0, columnspan=2, pady=5)

    def save_water():
        try:
            water = int(water_var.get())

            # Bersihkan data lama
            clean_old_data(username)

            if username not in user_data:
                msgbox.showerror("Error", f"Username '{username}' tidak ditemukan.")
                return

            # Pastikan "data_harian" ada dalam data user
            if "data_harian_water" not in user_data[username]:
                user_data[username]["data_harian_water"] = {}

            # Simpan data gelas air untuk tanggal hari ini
            now = datetime.now().strftime("%H:%M:%S")  # Waktu sekarang
            user_data[username]["data_harian_water"][today] = water
            user_data[username]["data_harian_water"][f"{today}_time"] = now
            save_database(user_data)

            last_water_label.config(text=f"Data terakhir: {water} gelas air pada {now}")
            
            target_water = int(user_data[username].get("gelasair", 0))  # Ambil target langkah dari database
            if water < target_water:
                warning_text = f"Peringatan: Anda belum mencapai target harian {target_water} gelas air!"
                tk.Label(frame, text=warning_text, bg="pink", fg="red", wraplength=300).grid(row=5, column=0, columnspan=2, pady=10)
            else:
                success_text = "Selamat! Anda telah mencapai target harian."
                tk.Label(frame, text=success_text, bg="pink", fg="green", wraplength=300).grid(row=5, column=0, columnspan=2, pady=10)
            
            tk.Label(frame, text="Data berhasil disimpan!", bg="pink", fg="green").grid(row=3, column=0, columnspan=2, pady=10)
            water_var.set("")  # Bersihkan input
        except ValueError:
            tk.Label(frame, text="Masukkan angka yang valid!", bg="pink", fg="red").grid(row=3, column=0, columnspan=2, pady=10)

    # Tombol untuk menyimpan gelas air
    tk.Button(frame, text="Simpan", command=save_water).grid(row=4, column=0, pady=10)
    tk.Button(frame, text="Tutup", command=waterWindow.destroy).grid(row=4, column=1, pady=10)
    
    center_window(waterWindow, 640, 320)
    waterWindow.mainloop()
    
def lihat_progress_window(username):
    # Bersihkan data lama
    clean_old_data(username)
    progressWindow = tk.Tk()
    progressWindow.title("Lihat Progress")
    
    progressWindow.state('zoomed')
    
    screen_width = progressWindow.winfo_screenwidth()
    screen_height = progressWindow.winfo_screenheight()
    
    # Muat gambar latar belakang
    bg_image = Image.open(r'images/bgutama.jpg')
    bg_image = bg_image.resize((screen_width, screen_height))
    bg_photo = ImageTk.PhotoImage(bg_image)
    
    # Label untuk latar belakang
    bg_label = tk.Label(progressWindow, image=bg_photo)
    bg_label.image = bg_photo  # Simpan referensi
    bg_label.place(relwidth=1, relheight=1)
    
    frame = tk.Frame(progressWindow, bg="pink", padx=20, pady=20)
    frame.place(relx=0.5, rely=0.5, anchor="center")
    
    tk.Label(frame, text="Selamat Datang!", font=("Arial", 16), bg="lightblue").pack(pady=10)
    tk.Label(frame, text="Pilih Progress", font=("Arial", 12), bg="lightblue").pack(pady=5)
    
    def grafik_window():
        show_graph_window()
    
    def grafikharian_window():
        show_graph2_window()
    
    tk.Button(frame, text="Harian", command=grafikharian_window).pack(padx=5)
    tk.Button(frame, text=f"{user_data[username]['target']}", command=grafik_window).pack(padx=5)
    
    def progress_ke_main_window():
        progressWindow.destroy()  # Tutup jendela progress
        open_main_window(username)  # Buka jendela main
    
    tk.Button(frame, text="Kembali", command=progress_ke_main_window).pack(pady=15)
    
    center_window(progressWindow, 1280, 720)
    progressWindow.mainloop()

def show_graph2_window():
    graph2Window = tk.Toplevel()
    graph2Window.title("Grafik Progress Harian")

    screen_width = graph2Window.winfo_screenwidth()
    screen_height = graph2Window.winfo_screenheight()
    
    bg_image = Image.open(r'images/bgutama.jpg')
    bg_image = bg_image.resize((screen_width, screen_height))
    bg_photo = ImageTk.PhotoImage(bg_image)
    
    # Label untuk latar belakang
    bg_label = tk.Label(graph2Window, image=bg_photo)
    bg_label.image = bg_photo  # Simpan referensi
    bg_label.place(relwidth=1, relheight=0.75)
    
    tk.Label(graph2Window, text="Masukkan username anda untuk melihat progress hari ini", font=("Arial", 12), bg="pink").pack(pady=5)
    
    username_entry = tk.Entry(graph2Window)
    username_entry.pack(pady=10)
    
    warning_label = tk.Label(graph2Window, text="", font=("Arial", 10), fg="red", bg="pink")
    warning_label.pack(pady=5)
    
    def read_data(file_path):
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"File {file_path} tidak ditemukan.")
            return {}
        except json.JSONDecodeError:
            print("File JSON tidak valid.")
            return {}

    def plot_data_today(file_path, username):
        today_date = datetime.now().strftime("%Y-%m-%d")
        data = read_data(file_path)
        
        if not data or username not in data:
            print(f"Data untuk pengguna '{username}' tidak ditemukan.")
            return

        user_data = data[username]
        steps = user_data.get("data_harian_steps", {}).get(today_date, None)
        sleep = user_data.get("data_harian_sleep", {}).get(today_date, None)
        water = user_data.get("data_harian_water", {}).get(today_date, None)

        if steps is None or sleep is None or water is None:
            print(f"Data untuk hari ini ({today_date}) tidak lengkap untuk pengguna '{username}'.")
            return

        try:
            target_steps = int(user_data.get("langkah", 0))
            target_sleep = int(user_data.get("jamTidur", 0))
            target_water = int(user_data.get("gelasair", 0))
        except ValueError:
            print("Format target tidak valid.")
            return
        # Plot data
        labels = ['Steps', 'Sleep (hours)', 'Water (per250ml)']
        values = [steps, sleep, water]
        targets = [target_steps, target_sleep, target_water]
        y_limits = [max(target_steps + 2000, 10000), 10, 10]

        fig, axs = plt.subplots(1, 3, figsize=(18, 6))
        colors = ['blue', 'green', 'purple']

        unmet_targets = []
        for i, ax in enumerate(axs):
            ax.bar(labels[i], values[i], color=colors[i])
            ax.axhline(targets[i], color='red', linestyle='--', linewidth=2, label=f'Target: {targets[i]}')
            ax.set_title(f"{labels[i]} Progress ({today_date})")
            ax.set_ylim(0, y_limits[i])  # Batas sumbu y khusus untuk setiap grafik
            ax.set_ylabel("Jumlah")
            ax.grid(axis='y', linestyle='--', alpha=0.7)
            ax.legend()
            
            if values[i] < targets[i]:
                unmet_targets.append(labels[i])

        # Periksa apakah ada target yang belum tercapai
        if unmet_targets:
            warning_label.config(text=f"Belum memenuhi target harian: {', '.join(unmet_targets)}")
        else:
            warning_label.config(text="Semua target hari ini sudah tercapai! 🎉")
            
        plt.tight_layout()
        plt.show()
        
    tk.Button(graph2Window, text="Tampilkan Grafik Hari Ini", command=lambda: plot_data_today('user_database.json', username_entry.get())).pack(pady=20)

    center_window(graph2Window, 560, 240)
    graph2Window.mainloop()

def show_graph_window():
    graphWindow = tk.Toplevel()
    graphWindow.title("Grafik Progress")

    screen_width = graphWindow.winfo_screenwidth()
    screen_height = graphWindow.winfo_screenheight()
    
    bg_image = Image.open(r'images/bgutama.jpg')
    bg_image = bg_image.resize((screen_width, screen_height))
    bg_photo = ImageTk.PhotoImage(bg_image)
    
    # Label untuk latar belakang
    bg_label = tk.Label(graphWindow, image=bg_photo)
    bg_label.image = bg_photo  # Simpan referensi
    bg_label.place(relwidth=1, relheight=0.75)
    
    tk.Label(graphWindow, text="Masukkan username anda untuk melihat progress", font=("Arial", 12), bg="pink").pack(pady=5)
    
    username_entry = tk.Entry(graphWindow)
    username_entry.pack(pady=10)
    
    def read_data(file_path):
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
            # Periksa keberadaan kunci
            if not all(key in data for key in ['data_harian_steps', 'data_harian_sleep', 'data_harian_water']):
                raise KeyError("Salah satu kunci tidak ditemukan dalam file JSON.")
            return data
        except FileNotFoundError:
            print(f"File {file_path} tidak ditemukan.")
            return {}
        except json.JSONDecodeError:
            print("File JSON tidak valid.")
            return {}

    # Fungsi utama untuk membuat grafik
    def plot_data(file_path, username):
        data = read_data(file_path)
        if not data or username not in data:
            print(f"Data untuk pengguna '{username}' tidak ditemukan.")
            return

        # Ambil data untuk pengguna spesifik
        user_data = data[username]
        
        if not all(key in user_data for key in ['data_harian_steps', 'data_harian_sleep', 'data_harian_water']):
            print(f"Data tidak lengkap untuk pengguna '{username}'.")
            return
        
        steps_data = user_data.get("data_harian_steps", {})
        sleep_data = user_data.get("data_harian_sleep", {})
        water_data = user_data.get("data_harian_water", {})

        if not steps_data or not sleep_data or not water_data:
            print("Data tidak lengkap untuk membuat grafik.")
            return
        
        # Mengambil data valid untuk langkah, tidur, dan air
        steps_data = {k: v for k, v in steps_data.items() if not k.endswith('_time')}
        sleep_data = {k: v for k, v in sleep_data.items() if not k.endswith('_time')}
        water_data = {k: v for k, v in water_data.items() if not k.endswith('_time')}

        # Mengurutkan data berdasarkan tanggal
        try:
            steps_data = dict(sorted(steps_data.items(), key=lambda x: datetime.strptime(x[0], "%Y-%m-%d")))
            sleep_data = dict(sorted(sleep_data.items(), key=lambda x: datetime.strptime(x[0], "%Y-%m-%d")))
            water_data = dict(sorted(water_data.items(), key=lambda x: datetime.strptime(x[0], "%Y-%m-%d")))
        except ValueError as e:
            print(f"Kesalahan dalam format tanggal: {e}")
            return

        try:
            target_steps = int(user_data.get("langkah", 0))
            target_sleep = int(user_data.get("jamTidur", 0))
            target_water = int(user_data.get("gelasair", 0))
        except ValueError:
            print("Format target tidak valid.")
            return
        
        # Plot data
        plt.figure(figsize=(12, 8))

        # Grafik langkah
        plt.subplot(3, 1, 1)
        plt.plot(steps_data.keys(), steps_data.values(), marker='o', label='Steps', color='blue')
        plt.axhline(y=target_steps, color='red', linestyle='--', label=f'Target: {target_steps}')
        plt.title('Daily Steps')
        plt.xlabel('Date')
        plt.ylabel('Steps')
        plt.ylim(0, max(target_steps + 2000, max(steps_data.values(), default=0) + 2000))
        plt.xticks(rotation=45)
        plt.legend()

        # Grafik tidur
        plt.subplot(3, 1, 2)
        plt.plot(sleep_data.keys(), sleep_data.values(), marker='o', label='Sleep (hours)', color='green')
        plt.axhline(y=target_sleep, color='red', linestyle='--', label=f'Target: {target_sleep}')
        plt.title('Daily Sleep')
        plt.xlabel('Date')
        plt.ylabel('Hours')
        plt.ylim(0, 10)
        plt.xticks(rotation=45)
        plt.legend()

        # Grafik air
        plt.subplot(3, 1, 3)
        plt.plot(water_data.keys(), water_data.values(), marker='o', label='Water (per250ml)', color='purple')
        plt.axhline(y=target_water, color='red', linestyle='--', label=f'Target: {target_water}')
        plt.title('Daily Water Intake')
        plt.xlabel('Date')
        plt.ylabel('per250ml')
        plt.ylim(0, 10)
        plt.xticks(rotation=45)
        plt.legend()

        plt.tight_layout()
        plt.show()
        
    # Tombol untuk memanggil grafik
    tk.Button(graphWindow, text="Tampilkan Grafik", command=lambda: plot_data('user_database.json', username_entry.get())).pack(pady=20)

    center_window(graphWindow, 560, 240)
    graphWindow.mainloop()

# Fungsi utama untuk memulai program
def main():
    login_window()

if __name__ == "__main__":
    main()
