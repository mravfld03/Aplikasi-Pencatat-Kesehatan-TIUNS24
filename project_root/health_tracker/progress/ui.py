import tkinter as tk
from tkinter import messagebox as msgbox
from PIL import Image, ImageTk
from .utils import center_window
from .database import load_database, save_database, clean_old_data

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
