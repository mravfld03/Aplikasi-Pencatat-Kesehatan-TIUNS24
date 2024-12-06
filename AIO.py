import tkinter as tk
import tkinter.messagebox as msgbox
from PIL import Image, ImageTk
import json
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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

    def login_action():
        uname = username.get()
        pwd = password.get()
        if uname in user_data and user_data[uname]["password"] == pwd:
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
        input_harian_window(mainWindow)
    
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

def input_harian_window(parent):
    inputWindow = tk.Toplevel(parent)
    inputWindow.title("Input Data Harian")
    
    # Dapatkan ukuran layar
    screen_width = parent.winfo_screenwidth()
    screen_height = parent.winfo_screenheight()
    
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
        input_steps_window()
    
    tk.Button(frame, text="Langkah", command=switch_to_input_steps).pack(padx=5)
        
    def switch_to_input_sleep():
        input_sleep_window()
        
    tk.Button(frame, text="Jam Tidur", command=switch_to_input_sleep).pack(padx=5)
    
    def switch_to_input_water():
        input_water_window()
    
    tk.Button(frame, text="Gelas Air", command=switch_to_input_water).pack(padx=5)
    
    def inputharian_ke_main_window():
        inputWindow.destroy()
        open_main_window(username)
    
    tk.Button(frame, text="Kembali", command=inputharian_ke_main_window).pack(pady=15)
    
    center_window(inputWindow, 640, 320)

def input_steps_window():
    inputstepsWindow = tk.Toplevel()
    inputstepsWindow.title("Input Langkah")

    frame = tk.Frame(inputstepsWindow, bg="pink", padx=5, pady=5)
    frame.place(relx=0.5, rely=0.5, anchor="center")
    
    tk.Label(frame, text="Masukkan Jumlah Langkah:", font=("Arial", 14), bg="pink").grid(row=0, column=0, columnspan=2, pady=10)

    # Input jumlah langkah
    steps_var = tk.StringVar()
    tk.Entry(frame, textvariable=steps_var, width=20).grid(row=1, column=0, columnspan=2, pady=5)

    def save_steps():
        try:
            steps = int(steps_var.get())
            if username not in user_data:
                user_data[username] = {"steps": []}
            
            # Tambahkan langkah ke database
            user_data[username]["steps"].append(steps)
            save_database(user_data)

            tk.Label(frame, text="Data berhasil disimpan!", bg="pink", fg="green").grid(row=3, column=0, columnspan=2, pady=10)
            steps_var.set("")  # Bersihkan input
        except ValueError:
            tk.Label(frame, text="Masukkan angka yang valid!", bg="pink", fg="red").grid(row=3, column=0, columnspan=2, pady=10)

    # Tombol untuk menyimpan langkah
    tk.Button(frame, text="Simpan", command=save_steps).grid(row=2, column=0, pady=10)
    tk.Button(frame, text="Tutup", command=inputstepsWindow.destroy).grid(row=2, column=1, pady=10)
    
    center_window(inputstepsWindow, 640, 320)
    inputstepsWindow.mainloop()

def input_sleep_window():
    inputsleepWindow = tk.Toplevel()
    inputsleepWindow.title("Input Jam Tidur")
    
    frame = tk.Frame(inputsleepWindow, bg="pink", padx=5, pady=5)
    frame.place(relx=0.5, rely=0.5, anchor="center")
    
    tk.Label(frame, text="Masukkan Jam Tidur:", font=("Arial", 14), bg="pink").grid(row=0, column=0, columnspan=2, pady=10)

    # Input jumlah langkah
    sleep_var = tk.StringVar()
    tk.Entry(frame, textvariable=sleep_var, width=20).grid(row=1, column=0, columnspan=2, pady=5)

    def save_sleep():
        try:
            sleep = int(sleep_var.get())
            if username not in user_data:
                user_data[username] = {"sleep": []}
            
            # Tambahkan langkah ke database
            user_data[username]["sleep"].append(sleep)
            save_database(user_data)

            tk.Label(frame, text="Data berhasil disimpan!", bg="pink", fg="green").grid(row=3, column=0, columnspan=2, pady=10)
            sleep_var.set("")  # Bersihkan input
        except ValueError:
            tk.Label(frame, text="Masukkan angka yang valid!", bg="pink", fg="red").grid(row=3, column=0, columnspan=2, pady=10)

    # Tombol untuk menyimpan langkah
    tk.Button(frame, text="Simpan", command=save_sleep).grid(row=2, column=0, pady=10)
    tk.Button(frame, text="Tutup", command=inputsleepWindow.destroy).grid(row=2, column=1, pady=10)
    
    center_window(inputsleepWindow, 640, 320)
    inputsleepWindow.mainloop()
    
def input_water_window():
    inputwaterWindow = tk.Toplevel()
    inputwaterWindow.title("Input Gelas Air")
    
    frame = tk.Frame(inputwaterWindow, bg="pink", padx=5, pady=5)
    frame.place(relx=0.5, rely=0.5, anchor="center")
    
    tk.Label(frame, text="Masukkan Jumlah Gelas Air(per 250ml):", font=("Arial", 14), bg="pink").grid(row=0, column=0, columnspan=2, pady=10)

    # Input jumlah langkah
    water_var = tk.StringVar()
    tk.Entry(frame, textvariable=water_var, width=20).grid(row=1, column=0, columnspan=2, pady=5)

    def save_water():
        try:
            water = int(water_var.get())
            if username not in user_data:
                user_data[username] = {"water": []}
            
            # Tambahkan langkah ke database
            user_data[username]["water"].append(water)
            save_database(user_data)

            tk.Label(frame, text="Data berhasil disimpan!", bg="pink", fg="green").grid(row=3, column=0, columnspan=2, pady=10)
            water_var.set("")  # Bersihkan input
        except ValueError:
            tk.Label(frame, text="Masukkan angka yang valid!", bg="pink", fg="red").grid(row=3, column=0, columnspan=2, pady=10)

    # Tombol untuk menyimpan langkah
    tk.Button(frame, text="Simpan", command=save_water).grid(row=2, column=0, pady=10)
    tk.Button(frame, text="Tutup", command=inputwaterWindow.destroy).grid(row=2, column=1, pady=10)
    
    center_window(inputwaterWindow, 640, 320)
    inputwaterWindow.mainloop()
    
def lihat_progress_window(username):
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
    tk.Button(frame, text="Harian", command=progressWindow.destroy).pack(padx=5)
    tk.Button(frame, text=f"{user_data[username]['target']}", command=progressWindow.destroy).pack(padx=5)
    
    def grafik_window():
        show_graph_window()
    
    tk.Button(frame, text="Grafik", command=grafik_window).pack(padx=5)
    
    def progress_ke_main_window():
        progressWindow.destroy()  # Tutup jendela progress
        open_main_window(username)  # Buka jendela main
    
    tk.Button(frame, text="Kembali", command=progress_ke_main_window).pack(pady=15)
    
    center_window(progressWindow, 1280, 720)
    progressWindow.mainloop()
    
def show_graph_window():
    # Membuat jendela baru
    graphWindow = tk.Toplevel()
    graphWindow.title("Jendela Grafik")

    # Membuat data untuk grafik
    x = [1, 2, 3, 4, 5]
    y = [1, 4, 9, 16, 25]

    # Membuat figure dan axes menggunakan matplotlib
    fig, ax = plt.subplots()
    ax.plot(x, y, label="Grafik Contoh")
    ax.set_title("Contoh Grafik")
    ax.set_xlabel("X-Axis")
    ax.set_ylabel("Y-Axis")
    ax.legend()

    # Menambahkan grafik ke Tkinter menggunakan FigureCanvasTkAgg
    canvas = FigureCanvasTkAgg(fig, master=graphWindow)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill=tk.BOTH, expand=True)

    # Tombol untuk menutup jendela
    tk.Button(graphWindow, text="Tutup", command=graphWindow.destroy).pack(pady=10)

# Fungsi utama untuk memulai program
def main():
    login_window()

if __name__ == "__main__":
    main()