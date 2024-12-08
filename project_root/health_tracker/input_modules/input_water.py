import tkinter as tk
from tkinter import messagebox as msgbox
from PIL import Image, ImageTk
from health_tracker.utils import center_window
from health_tracker.ui import login_window
from health_tracker.database import load_database, save_database, clean_old_data

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
            
            tk.Label(frame, text="Data berhasil disimpan!", bg="pink", fg="green").grid(row=3, column=0, columnspan=2, pady=10)
            water_var.set("")  # Bersihkan input
        except ValueError:
            tk.Label(frame, text="Masukkan angka yang valid!", bg="pink", fg="red").grid(row=3, column=0, columnspan=2, pady=10)

    # Tombol untuk menyimpan gelas air
    tk.Button(frame, text="Simpan", command=save_water).grid(row=4, column=0, pady=10)
    tk.Button(frame, text="Tutup", command=waterWindow.destroy).grid(row=4, column=1, pady=10)
    
    center_window(waterWindow, 640, 320)
    waterWindow.mainloop()