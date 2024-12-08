import tkinter as tk
from tkinter import messagebox as msgbox
from PIL import Image, ImageTk
from .utils import center_window
from .ui import login_window
from .database import load_database, save_database, clean_old_data
from health_tracker.input_modules.input_harian import input_harian_window
from health_tracker.input_modules.input_steps import input_steps_window
from health_tracker.input_modules.input_sleep import input_sleep_window
from health_tracker.input_modules.input_water import input_water_window

def lihat_progress_window(username):
    # Bersihkan data lama
    clean_old_data(username)
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
    
    def grafik_window():
        show_graph_window()
    
    def grafikharian_window():
        show_graph2_window()
    
    tk.Button(frame, text="Harian", command=grafikharian_window).pack(padx=5)
    tk.Button(frame, text=f"{user_data[username]['target']}", command=grafik_window).pack(padx=5)
    
    def progress_ke_main_window():
        progressWindow.destroy()  # Tutup jendela progress
        open_main_window(username)  # Buka jendela main
    
    tk.Button(frame, text="Kembali", command=progress_ke_main_window).pack(pady=15)
    
    center_window(progressWindow, 1280, 720)
    progressWindow.mainloop()

def show_graph2_window():
    graph2Window = tk.Toplevel()
    graph2Window.title("Grafik Progress Harian")

    screen_width = graph2Window.winfo_screenwidth()
    screen_height = graph2Window.winfo_screenheight()
    
    bg_image = Image.open(r'images/bgutama.jpg')
    bg_image = bg_image.resize((screen_width, screen_height))
    bg_photo = ImageTk.PhotoImage(bg_image)
    
    # Label untuk latar belakang
    bg_label = tk.Label(graph2Window, image=bg_photo)
    bg_label.image = bg_photo  # Simpan referensi
    bg_label.place(relwidth=1, relheight=0.75)
    
    tk.Label(graph2Window, text="Masukkan username anda untuk melihat progress hari ini", font=("Arial", 12), bg="pink").pack(pady=5)
    
    username_entry = tk.Entry(graph2Window)
    username_entry.pack(pady=10)
    
    def read_data(file_path):
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"File {file_path} tidak ditemukan.")
            return {}
        except json.JSONDecodeError:
            print("File JSON tidak valid.")
            return {}

    def plot_data_today(file_path, username):
        today_date = datetime.now().strftime("%Y-%m-%d")
        data = read_data(file_path)
        
        if not data or username not in data:
            print(f"Data untuk pengguna '{username}' tidak ditemukan.")
            return

        user_data = data[username]
        steps = user_data.get("data_harian_steps", {}).get(today_date, None)
        sleep = user_data.get("data_harian_sleep", {}).get(today_date, None)
        water = user_data.get("data_harian_water", {}).get(today_date, None)

        if steps is None or sleep is None or water is None:
            print(f"Data untuk hari ini ({today_date}) tidak lengkap untuk pengguna '{username}'.")
            return

        # Plot data
        labels = ['Steps', 'Sleep (hours)', 'Water (liters)']
        values = [steps, sleep, water]

        plt.figure(figsize=(8, 6))
        plt.bar(labels, values, color=['blue', 'green', 'purple'])
        plt.title(f"Progress Harian ({today_date})")
        plt.ylabel("Jumlah")
        plt.xticks(rotation=0)
        plt.tight_layout()
        plt.show()
        
    tk.Button(graph2Window, text="Tampilkan Grafik Hari Ini", command=lambda: plot_data_today('user_database.json', username_entry.get())).pack(pady=20)

    center_window(graph2Window, 560, 240)
    graph2Window.mainloop()

def show_graph_window():
    graphWindow = tk.Toplevel()
    graphWindow.title("Grafik Progress")

    screen_width = graphWindow.winfo_screenwidth()
    screen_height = graphWindow.winfo_screenheight()
    
    bg_image = Image.open(r'images/bgutama.jpg')
    bg_image = bg_image.resize((screen_width, screen_height))
    bg_photo = ImageTk.PhotoImage(bg_image)
    
    # Label untuk latar belakang
    bg_label = tk.Label(graphWindow, image=bg_photo)
    bg_label.image = bg_photo  # Simpan referensi
    bg_label.place(relwidth=1, relheight=0.75)
    
    tk.Label(graphWindow, text="Masukkan username anda untuk melihat progress", font=("Arial", 12), bg="pink").pack(pady=5)
    
    username_entry = tk.Entry(graphWindow)
    username_entry.pack(pady=10)
    
    def read_data(file_path):
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
            # Periksa keberadaan kunci
            if not all(key in data for key in ['data_harian_steps', 'data_harian_sleep', 'data_harian_water']):
                raise KeyError("Salah satu kunci tidak ditemukan dalam file JSON.")
            return data
        except FileNotFoundError:
            print(f"File {file_path} tidak ditemukan.")
            return {}
        except json.JSONDecodeError:
            print("File JSON tidak valid.")
            return {}

    # Fungsi utama untuk membuat grafik
    def plot_data(file_path, username):
        data = read_data(file_path)
        if not data or username not in data:
            print(f"Data untuk pengguna '{username}' tidak ditemukan.")
            return

        # Ambil data untuk pengguna spesifik
        user_data = data[username]
        
        if not all(key in user_data for key in ['data_harian_steps', 'data_harian_sleep', 'data_harian_water']):
            print(f"Data tidak lengkap untuk pengguna '{username}'.")
            return
        
        steps_data = user_data.get("data_harian_steps", {})
        sleep_data = user_data.get("data_harian_sleep", {})
        water_data = user_data.get("data_harian_water", {})

        if not steps_data or not sleep_data or not water_data:
            print("Data tidak lengkap untuk membuat grafik.")
            return
        
        # Mengambil data valid untuk langkah, tidur, dan air
        steps_data = {k: v for k, v in steps_data.items() if not k.endswith('_time')}
        sleep_data = {k: v for k, v in sleep_data.items() if not k.endswith('_time')}
        water_data = {k: v for k, v in water_data.items() if not k.endswith('_time')}

        # Mengurutkan data berdasarkan tanggal
        try:
            steps_data = dict(sorted(steps_data.items(), key=lambda x: datetime.strptime(x[0], "%Y-%m-%d")))
            sleep_data = dict(sorted(sleep_data.items(), key=lambda x: datetime.strptime(x[0], "%Y-%m-%d")))
            water_data = dict(sorted(water_data.items(), key=lambda x: datetime.strptime(x[0], "%Y-%m-%d")))
        except ValueError as e:
            print(f"Kesalahan dalam format tanggal: {e}")
            return

        # Plot data
        plt.figure(figsize=(12, 8))

        # Grafik langkah
        plt.subplot(3, 1, 1)
        plt.plot(steps_data.keys(), steps_data.values(), marker='o', label='Steps', color='blue')
        plt.title('Daily Steps')
        plt.xlabel('Date')
        plt.ylabel('Steps')
        plt.xticks(rotation=45)
        plt.legend()

        # Grafik tidur
        plt.subplot(3, 1, 2)
        plt.plot(sleep_data.keys(), sleep_data.values(), marker='o', label='Sleep (hours)', color='green')
        plt.title('Daily Sleep')
        plt.xlabel('Date')
        plt.ylabel('Hours')
        plt.xticks(rotation=45)
        plt.legend()

        # Grafik air
        plt.subplot(3, 1, 3)
        plt.plot(water_data.keys(), water_data.values(), marker='o', label='Water (liters)', color='purple')
        plt.title('Daily Water Intake')
        plt.xlabel('Date')
        plt.ylabel('Liters')
        plt.xticks(rotation=45)
        plt.legend()

        plt.tight_layout()
        plt.show()
        
    # Tombol untuk memanggil grafik
    tk.Button(graphWindow, text="Tampilkan Grafik", command=lambda: plot_data('user_database.json', username_entry.get())).pack(pady=20)

    center_window(graphWindow, 560, 240)
    graphWindow.mainloop()