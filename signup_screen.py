import tkinter as tk
import tkinter.messagebox as msgbox
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

# Fungsi untuk jendela login
def login_window():
    loginWindow = tk.Tk()
    loginWindow.title("Login")

    tk.Label(loginWindow, text="Username:").grid(row=0, column=0, padx=5, pady=5)
    tk.Label(loginWindow, text="Password:").grid(row=1, column=0, padx=5, pady=5)

    username = tk.Entry(loginWindow)
    password = tk.Entry(loginWindow, show="*")
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

    tk.Button(loginWindow, text="Login", command=login_action).grid(row=2, column=0, padx=5, pady=10)
    tk.Button(loginWindow, text="Daftar jika belum memiliki akun", command=switch_to_register).grid(row=2, column=1, padx=5, pady=10)

    loginWindow.mainloop()

# Fungsi untuk jendela registrasi
def register_window():
    registerWindow = tk.Tk()
    registerWindow.title("Daftar")

    tk.Label(registerWindow, text="Username:").grid(row=0, column=0, padx=5, pady=5)
    tk.Label(registerWindow, text="Password:").grid(row=1, column=0, padx=5, pady=5)
    tk.Label(registerWindow, text="Target yang diinginkan:").grid(row=2, column=0, padx=5, pady=5)
    tk.Label(registerWindow, text="Jumlah langkah/hari:").grid(row=3, column=0, padx=5, pady=5)
    tk.Label(registerWindow, text="Jam tidur/hari:").grid(row=4, column=0, padx=5, pady=5)
    tk.Label(registerWindow, text="Jumlah liter air minum/hari:").grid(row=5, column=0, padx=5, pady=5)

    username = tk.Entry(registerWindow)
    password = tk.Entry(registerWindow, show="*")
    langkah = tk.Entry(registerWindow)
    jamTidur = tk.Entry(registerWindow)
    jumlahLiter = tk.Entry(registerWindow)
    username.grid(row=0, column=1, padx=5, pady=5)
    password.grid(row=1, column=1, padx=5, pady=5)
    langkah.grid(row=3, column=1, padx=5, pady=5)
    jamTidur.grid(row=4, column=1, padx=5, pady=5)
    jumlahLiter.grid(row=5, column=1, padx=5, pady=5)

    # Daftar pilihan untuk target yang diinginkan
    options = ["Mingguan", "Bulanan"]
    target_variable = tk.StringVar(registerWindow)
    target_variable.set(options[0])  # Set default pilihan

    target_menu = tk.OptionMenu(registerWindow, target_variable, *options)
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

    tk.Button(registerWindow, text="Daftar", command=register_action).grid(row=6, column=0, padx=5, pady=10)
    tk.Button(registerWindow, text="Batal", command=lambda: [registerWindow.destroy(), login_window()]).grid(row=6, column=1, padx=5, pady=10)

    registerWindow.mainloop()

# Fungsi untuk jendela utama setelah login
def open_main_window(username):
    mainWindow = tk.Tk()
    mainWindow.title("Halaman Utama")

    # Background frame
    frame = tk.Frame(mainWindow, bg="lightblue", width=400, height=300)
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text=f"Selamat Datang, {username}!", font=("Arial", 16), bg="lightblue").pack(pady=10)
    tk.Label(frame, text=f"Target Anda: {user_data[username]['target']}", font=("Arial", 12), bg="lightblue").pack(pady=5)

    tk.Button(frame, text="Keluar", command=mainWindow.destroy).pack(pady=20)

    mainWindow.mainloop()

# Fungsi utama untuk memulai program
def main():
    login_window()

if __name__ == "__main__":
    main()
