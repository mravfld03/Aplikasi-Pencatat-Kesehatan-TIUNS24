def input_data():
    """Fungsi untuk input data kesehatan harian"""
    steps = int(input("Masukkan jumlah langkah harian (x): "))
    sleep = float(input("Masukkan durasi tidur harian dalam jam (y): "))
    water = float(input("Masukkan konsumsi air harian dalam liter (z): "))
    return {"steps": steps, "sleep": sleep, "water": water}

def calculate_average(data, period):
    """Menghitung rata-rata untuk periode tertentu"""
    total_days = len(data)
    avg_steps = sum(day["steps"] for day in data) / total_days
    avg_sleep = sum(day["sleep"] for day in data) / total_days
    avg_water = sum(day["water"] for day in data) / total_days
    return avg_steps, avg_sleep, avg_water

def check_targets(avg_steps, avg_sleep, avg_water, targets):
    """Mengevaluasi apakah target tercapai"""
    results = {
        "steps": avg_steps >= targets["steps"],
        "sleep": avg_sleep >= targets["sleep"],
        "water": avg_water >= targets["water"]
    }
    return results

def main():
    # Target kesehatan harian
    targets = {"steps": 8000, "sleep": 7, "water": 2}
    health_data = []  # Data kesehatan harian

    while True:
        print("\n--- Aplikasi Pencatat Kesehatan Harian ---")
        print("1. Input Data Harian")
        print("2. Lihat Progres")
        print("3. Keluar")
        menu_choice = input("Pilih menu: ")

        if menu_choice == "1":
            # Input data kesehatan harian
            data = input_data()
            health_data.append(data)
            print("Data berhasil ditambahkan!")

        elif menu_choice == "2":
            # Cek apakah ada data
            if not health_data:
                print("Belum ada data kesehatan yang tercatat.")
                continue
            
            # Input periode (mingguan/bulanan)
            period = input("Masukkan periode (mingguan/bulanan): ").lower()
            if period not in ["mingguan", "bulanan"]:
                print("Periode tidak valid!")
                continue
            
            # Hitung rata-rata
            avg_steps, avg_sleep, avg_water = calculate_average(health_data, period)
            print("\n--- Hasil Progres Kesehatan ---")
            print(f"Rata-rata langkah: {avg_steps:.2f}")
            print(f"Rata-rata tidur: {avg_sleep:.2f} jam")
            print(f"Rata-rata konsumsi air: {avg_water:.2f} liter")

            # Analisis apakah target tercapai
            results = check_targets(avg_steps, avg_sleep, avg_water, targets)
            if all(results.values()):
                print("Semua target tercapai! Lanjutkan kerja baik ini!")
            else:
                print("Beberapa target belum tercapai:")
                if not results["steps"]:
                    print("- Target langkah belum tercapai.")
                if not results["sleep"]:
                    print("- Target tidur belum tercapai.")
                if not results["water"]:
                    print("- Target konsumsi air belum tercapai.")
                print("Tetap semangat untuk meningkatkan kesehatan!")

        elif menu_choice == "3":
            print("Terima kasih telah menggunakan aplikasi!")
            break

        else:
            print("Pilihan menu tidak valid, coba lagi!")

if __name__ == "_main_":
    main()