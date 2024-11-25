import tkinter as tk
import tkinter.messagebox as msgbox

def main():
    mainWindow = tk.Tk()
    mainWindow.title("Program Utama")
    
    def btnSalamClick(*args):
        msgbox.showinfo("New Message", "Hallo, Selamat siang")
        
    # membuat tombol
    # cara 1 
    btnExit = tk.Button(mainWindow, command=mainWindow.destroy)
    btnExit['text'] = "Selamat Datang di Aplikasi Pencatat Kesehatan, klik tombol ini untuk lanjutkan"
    btnExit.pack()
    
    # cara 2
    # btnSalam = tk.Button(mainWindow, text="Salam")
    # btnSalam.pack()
    #btnSalam.bind('<Button-1>', btnSalamClick)
    # txtNim
    
    mainWindow.mainloop()

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
            if uname in user_data and user_data[uname] == pwd:
                msgbox.showinfo("Login Berhasil", "Selamat datang, " + uname)
                loginWindow.destroy()
                open_main_window()
            else:
                msgbox.showerror("Login Gagal", "Username atau password salah.")

        def switch_to_register():
            loginWindow.destroy()
            register_window()

        tk.Button(loginWindow, text="Login", command=login_action).grid(row=2, column=0, padx=5, pady=10)
        tk.Button(loginWindow, text="Daftar jika belum memiliki akun", command=switch_to_register).grid(row=2, column=1, padx=5, pady=10)

        loginWindow.mainloop()

    def register_window():
        registerWindow = tk.Tk()
        registerWindow.title("Daftar")

        tk.Label(registerWindow, text="Username:").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(registerWindow, text="Password:").grid(row=1, column=0, padx=5, pady=5)
        tk.Label(registerWindow, text="Target yang diinginkan").grid(row=2, column=0, padx=5, pady=5)


        username = tk.Entry(registerWindow)
        password = tk.Entry(registerWindow, show="*")
        Target_yang_diinginkan = tk.Entry(registerWindow)
        username.grid(row=0, column=1, padx=5, pady=5)
        password.grid(row=1, column=1, padx=5, pady=5)
        Target_yang_diinginkan.grid(row=2, column=1, padx=5, pady=5)

        def register_action():
            uname = username.get()
            pwd = password.get()
            if uname in user_data:
                msgbox.showerror("Gagal Daftar", "Username sudah terdaftar.")
            elif uname and pwd:
                user_data[uname] = pwd
                msgbox.showinfo("Berhasil Daftar", "Akun berhasil dibuat!")
                registerWindow.destroy()
                login_window()
            else:
                msgbox.showerror("Gagal Daftar", "Username dan password tidak boleh kosong.")

        tk.Button(registerWindow, text="Daftar", command=register_action).grid(row=3, column=0, padx=5, pady=10)
        tk.Button(registerWindow, text="Batal", command=lambda: [registerWindow.destroy(), login_window()]).grid(row=3, column=1, padx=5, pady=10)

        registerWindow.mainloop()

    # Mulai dari jendela login
    login_window()

if __name__ == "__main__":
    main()