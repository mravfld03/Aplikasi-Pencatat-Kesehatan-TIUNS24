import tkinter as tk
import tkinter.messagebox as msgbox
from PIL import Image, ImageTk
import json
import os

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

    # Pasang gambar background
    bg_image = Image.open(r'D:\Kelompok_8_Aplikasi_Pencatat_Kesehatan_TIUNS24\background.jpg')  # Pastikan file ini ada di direktori yang sama
    bg_image = bg_image.resize((loginWindow.winfo_screenwidth(), loginWindow.winfo_screenheight()))
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(loginWindow, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)

    frame = tk.Frame(loginWindow, bg="white", padx=20, pady=20)
    frame.place(relx=0.5, rely=0.5, anchor="center")

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

    # Pasang gambar background
    bg_image = Image.open(r'D:\Kelompok_8_Aplikasi_Pencatat_Kesehatan_TIUNS24\background.jpg')
    bg_image = bg_image.resize((registerWindow.winfo_screenwidth(), registerWindow.winfo_screenheight()))
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(registerWindow, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)

    frame = tk.Frame(registerWindow, bg="white", padx=20, pady=20)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(frame, text="Username:", bg="white").grid(row=0, column=0, padx=5, pady=5)
    tk.Label(frame, text="Password:", bg="white").grid(row=1, column=0, padx=5, pady=5)
    tk.Label(frame, text="Target yang diinginkan:", bg="white").grid(row=2, column=0, padx=5, pady=5)
    tk.Label(frame, text="Jumlah langkah/hari:", bg="white").grid(row=3, column=0, padx=5, pady=5)
    tk.Label(frame, text="Jam tidur/hari:", bg="white").grid(row=4, column=0, padx=5, pady=5)
    tk.Label(frame, text="Jumlah liter air minum/hari:", bg="white").grid(row=5, column=0, padx=5, pady=5)

    username = tk.Entry(frame)
    password = tk.Entry(frame, show="*")
    langkah = tk.Entry(frame)
    jamTidur = tk.Entry(frame)
    jumlahLiter = tk.Entry(frame)
    username.grid(row=0, column=1, padx=5, pady=5)
    password.grid(row=1, column=1, padx=5, pady=5)
    langkah.grid(row=3, column=1, padx=5, pady=5)
    jamTidur.grid(row=4, column=1, padx=5, pady=5)
    jumlahLiter.grid(row=5, column=1, padx=5, pady=5)

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
        lgkh = langkah.get()
        jmTdr = jamTidur.get()
        jmlLiter = jumlahLiter.get()

        if uname in user_data:
            msgbox.showerror("Gagal Daftar", "Username sudah terdaftar.")
        elif uname and pwd:
            user_data[uname] = {"password": pwd, "target": target, "langkah": lgkh, "jamTidur": jmTdr, "jumlahLiter": jmlLiter}
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
def open_main_window(uname):
    mainWindow = tk.Tk()
    mainWindow.title("Aplikasi Pencatat Kesehatan Harian")
    
    bg_image = Image.open(r'D:\Kelompok_8_Aplikasi_Pencatat_Kesehatan_TIUNS24\background.jpg')
    bg_image = bg_image.resize((mainWindow.winfo_screenwidth(), mainWindow.winfo_screenheight()))
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(mainWindow, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)
     
        # Layout utama
    frame = tk.Frame(mainWindow, bg="white", padx=20, pady=20)
    frame.place(relx=0.5, rely=0.5, anchor="center")
    
        # Target kesehatan harian
    uname.targets = {"steps": 8000, "sleep": 7, "water": 2}
    uname.health_data = []  # Data kesehatan harian
        
    tk.Label(uname.main_frame, text="--- Aplikasi Pencatat Kesehatan Harian ---", font=("Arial", 14)).pack(pady=5)
    tk.Button(uname.main_frame, text="Input Data Harian", command=uname.input_data).pack(fill="x", pady=5)
    tk.Button(uname.main_frame, text="Lihat Progres", command=uname.show_progress).pack(fill="x", pady=5)
    tk.Button(uname.main_frame, text="Keluar", command=root.quit).pack(fill="x", pady=5)
    
    def input_data(uname):
        """Fungsi untuk input data kesehatan harian"""
        try:
            steps = int(askstring("Input Data", "Masukkan jumlah langkah harian (x):"))
            sleep = float(askstring("Input Data", "Masukkan durasi tidur harian dalam jam (y):"))
            water = float(askstring("Input Data", "Masukkan konsumsi air harian dalam liter (z):"))
            uname.health_data.append({"steps": steps, "sleep": sleep, "water": water})
            messagebox.showinfo("Sukses", "Data berhasil ditambahkan!")
        except (ValueError, TypeError):
            messagebox.showerror("Error", "Input tidak valid! Pastikan data yang dimasukkan benar.")
    
    def calculate_average(uname):
        """Menghitung rata-rata untuk semua data yang ada"""
        total_days = len(uname.health_data)
        avg_steps = sum(day["steps"] for day in uname.health_data) / total_days
        avg_sleep = sum(day["sleep"] for day in uname.health_data) / total_days
        avg_water = sum(day["water"] for day in uname.health_data) / total_days
        return avg_steps, avg_sleep, avg_water
    
    def check_targets(uname, avg_steps, avg_sleep, avg_water):
        """Mengevaluasi apakah target tercapai"""
        return {
            "steps": avg_steps >= uname.targets["steps"],
            "sleep": avg_sleep >= uname.targets["sleep"],
            "water": avg_water >= uname.targets["water"]
        }
    
    def show_progress(uname):
        """Fungsi untuk menampilkan progres kesehatan"""
        if not uname.health_data:
            messagebox.showinfo("Info", "Belum ada data kesehatan yang tercatat.")
            return
        
        # Hitung rata-rata
        avg_steps, avg_sleep, avg_water = uname.calculate_average()
        results = uname.check_targets(avg_steps, avg_sleep, avg_water)
        
        # Tampilkan hasil progres
        progress_text = (
            f"--- Hasil Progres Kesehatan ---\n\n"
            f"Rata-rata langkah: {avg_steps:.2f}\n"
            f"Rata-rata tidur: {avg_sleep:.2f} jam\n"
            f"Rata-rata konsumsi air: {avg_water:.2f} liter\n\n"
        )
        if all(results.values()):
            progress_text += "Semua target tercapai! Lanjutkan kerja baik ini!"
        else:
            progress_text += "Beberapa target belum tercapai:\n"
        if not results["steps"]:
            progress_text += "- Target langkah belum tercapai.\n"
        if not results["sleep"]:
            progress_text += "- Target tidur belum tercapai.\n"
        if not results["water"]:
            progress_text += "- Target konsumsi air belum tercapai.\n"
            progress_text += "Tetap semangat untuk meningkatkan kesehatan!"
        
        messagebox.showinfo("Progres Kesehatan", progress_text)
        
    center_window(mainWindow, 1280, 720)
    mainWindow.mainloop()

# Fungsi utama untuk memulai program
def main():
    login_window()
    open_main_window(uname)

if __name__ == "__main__":
    main()
