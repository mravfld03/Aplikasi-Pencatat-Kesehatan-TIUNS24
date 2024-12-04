import tkinter as tk
import sqlite3

# Fungsi untuk membuat database dan tabel jika belum ada
def setup_database():
    conn = sqlite3.connect("user_progress.db")
    cursor = conn.cursor()
    # Membuat tabel jika belum ada
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            tanggal TEXT NOT NULL,
            jumlah_langkah INTEGER,
            jam_tidur REAL,
            liter_air REAL
        )
    """)
    conn.commit()
    conn.close()

# Fungsi untuk memasukkan data baru ke database
def tambah_data(username, tanggal, jumlah_langkah, jam_tidur, liter_air):
    conn = sqlite3.connect("user_progress.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO progress (username, tanggal, jumlah_langkah, jam_tidur, liter_air)
        VALUES (?, ?, ?, ?, ?)
    """, (username, tanggal, jumlah_langkah, jam_tidur, liter_air))
    conn.commit()
    conn.close()

# Fungsi untuk melihat progress
def lihat_progress(username):
    # Jendela untuk melihat progress
    progressWindow = tk.Tk()
    progressWindow.title("Lihat Progress")

    # Label untuk judul
    tk.Label(progressWindow, text=f"Progress {username}", font=("Arial", 16)).pack(pady=10)

    # Ambil data dari database
    conn = sqlite3.connect("user_progress.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT jumlah_langkah, jam_tidur, liter_air
        FROM progress
        WHERE username = ?
        ORDER BY tanggal DESC
        LIMIT 7
    """, (username,))
    data = cursor.fetchall()
    conn.close()

    # Periksa apakah data tersedia
    if len(data) < 7:
        tk.Label(progressWindow, text="Warning: Data tidak lengkap!", font=("Arial", 12), fg="red").pack(pady=10)
    else:
        # Pisahkan data untuk perhitungan
        jumlah_langkah = [row[0] for row in data]
        jam_tidur = [row[1] for row in data]
        liter_air = [row[2] for row in data]

        # Hitung rata-rata selama 7 hari
        avg_steps = sum(jumlah_langkah) / 7
        avg_sleep = sum(jam_tidur) / 7
        avg_water = sum(liter_air) / 7

        # Target default
        steps_target = 10000
        sleep_target = 7
        water_target = 2.5

        # Evaluasi target
        steps_eval = "Tercapai" if avg_steps >= steps_target else "Belum Tercapai"
        sleep_eval = "Tercapai" if avg_sleep >= sleep_target else "Belum Tercapai"
        water_eval = "Tercapai" if avg_water >= water_target else "Belum Tercapai"

        # Tampilkan hasil perhitungan
        tk.Label(progressWindow, text=f"Rata-rata Langkah: {avg_steps:.2f} ({steps_eval})", font=("Arial", 12)).pack(pady=5)
        tk.Label(progressWindow, text=f"Rata-rata Jam Tidur: {avg_sleep:.2f} ({sleep_eval})", font=("Arial", 12)).pack(pady=5)
        tk.Label(progressWindow, text=f"Rata-rata Liter Air: {avg_water:.2f} ({water_eval})", font=("Arial", 12)).pack(pady=5)

    # Tombol kembali ke menu utama
    tk.Button(progressWindow, text="Tutup", command=progressWindow.destroy).pack(pady=10)

    progressWindow.mainloop()

# Fungsi untuk input data baru
def input_data(username):
    # Jendela untuk input data
    inputWindow = tk.Tk()
    inputWindow.title("Input Data")

    tk.Label(inputWindow, text=f"Input Data untuk {username}", font=("Arial", 16)).pack(pady=10)

    # Form input
    tk.Label(inputWindow, text="Tanggal (YYYY-MM-DD):").pack()
    tanggal_entry = tk.Entry(inputWindow)
    tanggal_entry.pack()

    tk.Label(inputWindow, text="Jumlah Langkah:").pack()
    langkah_entry = tk.Entry(inputWindow)
    langkah_entry.pack()

    tk.Label(inputWindow, text="Jam Tidur:").pack()
    tidur_entry = tk.Entry(inputWindow)
    tidur_entry.pack()

    tk.Label(inputWindow, text="Liter Air:").pack()
    air_entry = tk.Entry(inputWindow)
    air_entry.pack()

    # Fungsi untuk menyimpan data
    def simpan_data():
        tanggal = tanggal_entry.get()
        jumlah_langkah = int(langkah_entry.get())
        jam_tidur = float(tidur_entry.get())
        liter_air = float(air_entry.get())

        tambah_data(username, tanggal, jumlah_langkah, jam_tidur, liter_air)
        tk.Label(inputWindow, text="Data berhasil disimpan!", font=("Arial", 12), fg="green").pack(pady=10)

    tk.Button(inputWindow, text="Simpan", command=simpan_data).pack(pady=10)
    tk.Button(inputWindow, text="Tutup", command=inputWindow.destroy).pack(pady=10)

    inputWindow.mainloop()

# Setup database
setup_database()

# Contoh penggunaan
username = "user123"
input_data(username)  # Untuk memasukkan data
lihat_progress(username)  # Untuk melihat progress
