import tkinter as tk
from tkinter import messagebox as msgbox
from PIL import Image, ImageTk
from .utils import center_window
from .database import load_database, save_database, clean_old_data

user_data = load_database()
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

            tk.Label(frame, text="Data berhasil disimpan!", bg="pink", fg="green").grid(row=3, column=0, columnspan=2, pady=10)
            sleep_var.set("")  # Bersihkan input
        except ValueError:
            tk.Label(frame, text="Masukkan angka yang valid!", bg="pink", fg="red").grid(row=3, column=0, columnspan=2, pady=10)

    # Tombol untuk menyimpan jam tidur
    tk.Button(frame, text="Simpan", command=save_sleep).grid(row=4, column=0, pady=10)
    tk.Button(frame, text="Tutup", command=sleepWindow.destroy).grid(row=4, column=1, pady=10)
    
    center_window(sleepWindow, 640, 320)
    sleepWindow.mainloop()