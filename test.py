# Program untuk menghitung progres mingguan kesehatan

# Data kesehatan harian (contoh kasus)
health_data = {
    "2024-11-08": {"steps": 7500, "sleep_hours": 6.5, "water_liters": 1.8},
    "2024-11-09": {"steps": 8000, "sleep_hours": 7.0, "water_liters": 2.0},
    "2024-11-10": {"steps": 6000, "sleep_hours": 6.0, "water_liters": 1.5},
    "2024-11-11": {"steps": 8500, "sleep_hours": 8.0, "water_liters": 2.5},
    "2024-11-12": {"steps": 5000, "sleep_hours": 5.5, "water_liters": 1.2},
    "2024-11-13": {"steps": 9000, "sleep_hours": 7.5, "water_liters": 2.3},
    "2024-11-14": {"steps": 8000, "sleep_hours": 7.0, "water_liters": 2.0},
}

# Target harian
target_steps = 8000
target_sleep = 7
target_water = 2

# Fungsi untuk menghitung rata-rata
def calculate_weekly_progress(data):
    total_steps = sum(entry["steps"] for entry in data.values())
    total_sleep = sum(entry["sleep_hours"] for entry in data.values())
    total_water = sum(entry["water_liters"] for entry in data.values())

    avg_steps = total_steps / len(data)
    avg_sleep = total_sleep / len(data)
    avg_water = total_water / len(data)

    return avg_steps, avg_sleep, avg_water

# Fungsi untuk menganalisis apakah target tercapai
def analyze_progress(avg_steps, avg_sleep, avg_water, target_steps, target_sleep, target_water):
    step_status = "Met" if avg_steps >= target_steps else "Not Met"
    sleep_status = "Met" if avg_sleep >= target_sleep else "Not Met"
    water_status = "Met" if avg_water >= target_water else "Not Met"
    return step_status, sleep_status, water_status

# Main program
avg_steps, avg_sleep, avg_water = calculate_weekly_progress(health_data)
step_status, sleep_status, water_status = analyze_progress(avg_steps, avg_sleep, avg_water, target_steps, target_sleep, target_water)

# Display results
print("--- Weekly Health Progress Report ---")
print(f"Average Steps: {avg_steps:.2f} (Target: {target_steps}) - {step_status}")
print(f"Average Sleep: {avg_sleep:.2f} hours (Target: {target_sleep}) - {sleep_status}")
print(f"Average Water: {avg_water:.2f} liters (Target: {target_water}) - {water_status}")
print("\nSummary:")
print("All targets met!" if step_status == "Met" and sleep_status == "Met" and water_status == "Met" else "Targets not fully met. Keep improving!")