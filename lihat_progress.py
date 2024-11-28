import tkinter as tk
import tkinter.messagebox as msgbox

def lihat_progress(username):
    # Jendela untuk melihat progress
    progressWindow = tk.Tk()
    progressWindow.title("Lihat Progress")

    # Label untuk judul
    tk.Label(progressWindow, text=f"Progress {username}", font=("Arial", 16)).pack(pady=10)

    # Data simulasi untuk progress pengguna
    # Ganti dengan pengambilan data asli dari database
    user_progress = {
        "jumlah_langkah": [9000, 10000, 8000, 12000, 11000, 9500, 10000],  # Data langkah (7 hari)
        "jam_tidur": [7, 6.5, 8, 7.5, 6, 7, 8],  # Data jam tidur (7 hari)
        "liter_air": [2, 2.5, 2, 3, 2.5, 2, 2.5]  # Data konsumsi air (7 hari)
    }

    # Target default (bisa disesuaikan)
    steps_target = 10000  # Target langkah harian
    sleep_target = 7  # Target jam tidur harian
    water_target = 2.5  # Target liter air harian

    # Periksa apakah data lengkap
    if not all(len(values) == 7 for values in user_progress.values()):
        tk.Label(progressWindow, text="Warning: Data tidak lengkap!", font=("Arial", 12), fg="red").pack(pady=10)
    else:
        # Hitung rata-rata selama 7 hari
        avg_steps = sum(user_progress["jumlah_langkah"]) / 7
        avg_sleep = sum(user_progress["jam_tidur"]) / 7
        avg_water = sum(user_progress["liter_air"]) / 7

        # Evaluasi target
        steps_eval = "Tercapai" if avg_steps >= steps_target else "Belum Tercapai"
        sleep_eval = "Tercapai" if avg_sleep >= sleep_target else "Belum Tercapai"
        water_eval = "Tercapai" if avg_water >= water_target else "Belum Tercapai"

        # Tampilkan hasil perhitungan
        tk.Label(progressWindow, text=f"Rata-rata Langkah: {avg_steps:.2f} ({steps_eval})", font=("Arial", 12)).pack(pady=5)
        tk.Label(progressWindow, text=f"Rata-rata Jam Tidur: {avg_sleep:.2f} ({sleep_eval})", font=("Arial", 12)).pack(pady=5)
        tk.Label(progressWindow, text=f"Rata-rata Liter Air: {avg_water:.2f} ({water_eval})", font=("Arial", 12)).pack(pady=5)

        # Placeholder untuk grafik performa
        tk.Label(progressWindow, text="Grafik Performa ditampilkan di sini.", font=("Arial", 12), fg="blue").pack(pady=20)

    # Tombol kembali ke menu utama
    tk.Button(progressWindow, text="Tutup", command=progressWindow.destroy).pack(pady=10)

    progressWindow.mainloop()
