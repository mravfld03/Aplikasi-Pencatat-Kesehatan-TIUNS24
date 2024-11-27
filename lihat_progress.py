import tkinter as tk
import tkinter.messagebox as msgbox

\# Tampilkan hasil progres
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
