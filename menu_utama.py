import tkinter as tk
from tkinter import messagebox
from tkinter.simpledialog import askstring

class HealthTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Pencatat Kesehatan Harian")
        
        # Target kesehatan harian
        self.targets = {"steps": 8000, "sleep": 7, "water": 2}
        self.health_data = []  # Data kesehatan harian
        
        # Layout utama
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(padx=10, pady=10)
        
        tk.Label(self.main_frame, text="--- Aplikasi Pencatat Kesehatan Harian ---", font=("Arial", 14)).pack(pady=5)
        tk.Button(self.main_frame, text="Input Data Harian", command=self.input_data).pack(fill="x", pady=5)
        tk.Button(self.main_frame, text="Lihat Progres", command=self.show_progress).pack(fill="x", pady=5)
        tk.Button(self.main_frame, text="Keluar", command=root.quit).pack(fill="x", pady=5)
    
    def input_data(self):
        """Fungsi untuk input data kesehatan harian"""
        try:
            steps = int(askstring("Input Data", "Masukkan jumlah langkah harian (x):"))
            sleep = float(askstring("Input Data", "Masukkan durasi tidur harian dalam jam (y):"))
            water = float(askstring("Input Data", "Masukkan konsumsi air harian dalam liter (z):"))
            self.health_data.append({"steps": steps, "sleep": sleep, "water": water})
            messagebox.showinfo("Sukses", "Data berhasil ditambahkan!")
        except (ValueError, TypeError):
            messagebox.showerror("Error", "Input tidak valid! Pastikan data yang dimasukkan benar.")
    
    def calculate_average(self):
        """Menghitung rata-rata untuk semua data yang ada"""
        total_days = len(self.health_data)
        avg_steps = sum(day["steps"] for day in self.health_data) / total_days
        avg_sleep = sum(day["sleep"] for day in self.health_data) / total_days
        avg_water = sum(day["water"] for day in self.health_data) / total_days
        return avg_steps, avg_sleep, avg_water
    
    def check_targets(self, avg_steps, avg_sleep, avg_water):
        """Mengevaluasi apakah target tercapai"""
        return {
            "steps": avg_steps >= self.targets["steps"],
            "sleep": avg_sleep >= self.targets["sleep"],
            "water": avg_water >= self.targets["water"]
        }
    
    def show_progress(self):
        """Fungsi untuk menampilkan progres kesehatan"""
        if not self.health_data:
            messagebox.showinfo("Info", "Belum ada data kesehatan yang tercatat.")
            return
        
        # Hitung rata-rata
        avg_steps, avg_sleep, avg_water = self.calculate_average()
        results = self.check_targets(avg_steps, avg_sleep, avg_water)
        
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


 #tambahan
# Jalankan aplikasi
if __name__ == "__main__":
    root = tk.Tk()
    app = HealthTrackerApp(root)
    root.mainloop()
