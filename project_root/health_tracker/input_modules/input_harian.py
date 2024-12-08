import tkinter as tk
from tkinter import messagebox as msgbox
from PIL import Image, ImageTk
from health_tracker.utils import center_window
from health_tracker.ui import login_window
from health_tracker.database import load_database, save_database, clean_old_data

def input_harian_window(parent_window, username):
    inputWindow = tk.Toplevel(parent_window)
    inputWindow.title("Input Data Harian")
    
    # Dapatkan ukuran layar
    screen_width = parent_window.winfo_screenwidth()
    screen_height = parent_window.winfo_screenheight()
    
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
        input_steps_window(username)
    
    tk.Button(frame, text="Langkah", command=switch_to_input_steps).pack(padx=5)
        
    def switch_to_input_sleep():
        input_sleep_window(username)
        
    tk.Button(frame, text="Jam Tidur", command=switch_to_input_sleep).pack(padx=5)
    
    def switch_to_input_water():
        input_water_window(username)
    
    tk.Button(frame, text="Gelas Air", command=switch_to_input_water).pack(padx=5)
    
    def inputharian_ke_main_window():
        inputWindow.destroy()
        parent_window.deiconify()
        parent_window.state('zoomed')
    
    tk.Button(frame, text="Kembali", command=inputharian_ke_main_window).pack(pady=15)
    
    center_window(inputWindow, 640, 320)
