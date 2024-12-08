import tkinter as tk
from tkinter import messagebox as msgbox
from PIL import Image, ImageTk
from health_tracker.utils import center_window
from health_tracker.ui import login_window
from health_tracker.database import load_database, save_database, clean_old_data

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