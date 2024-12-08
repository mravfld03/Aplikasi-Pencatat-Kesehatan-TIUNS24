from health_tracker.database import load_database
from health_tracker.utils import center_window
from health_tracker.ui import login_window as start_ui

def main():
    # Inisialisasi database
    load_database()

    # Memulai antarmuka pengguna
    start_ui()

if __name__ == "__main__":
    main()