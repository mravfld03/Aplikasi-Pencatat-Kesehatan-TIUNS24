# Kelompok 8 TI UNS 2024
Aplikasi Pencatat Kesehatan Harian
### Anggota:
- Syifa Alea Nisrina (I0324124)
- Muhammad Rafli Dhiyanuddin (I0324127)
- Abelard Rafael Jeremia Widlan (I0324138)

Tema: Aplikasi Pencatat Kesehatan Harian

Deskripsi Umum:
Aplikasi ini bertujuan membantu pengguna melacak dan memantau aktivitas kesehatan harian, seperti jumlah langkah, durasi tidur, dan jumlah air yang dikonsumsi. Dengan aplikasi ini, pengguna bisa mencatat setiap aktivitas kesehatan setiap hari, melihat progres mingguan atau bulanan, dan mendapatkan peringatan jika target kesehatan harian tidak terpenuhi.

Flowchart:
![Flowchart](https://ibb.co.com/f8THnCH)

Tujuan Aplikasi:
1. Memberikan kemudahan bagi pengguna untuk mencatat aktivitas kesehatannya.
2. Memotivasi pengguna untuk mencapai target kesehatan harian.
3. Menyediakan ringkasan progres kesehatan, baik harian, mingguan, maupun bulanan.
---
Fitur-Fitur Utama
1. Catatan Harian
Pengguna dapat mencatat:
Jumlah Langkah: Input jumlah langkah harian.
Durasi Tidur: Input jumlah jam tidur.
Jumlah Air: Input jumlah air (ml) yang dikonsumsi.
Aplikasi akan menyimpan catatan ini dan menyusun ringkasan harian yang bisa diakses kapan saja.

2. Target Harian
Pengguna bisa mengatur target harian untuk tiap aktivitas:
Target jumlah langkah (misal: 10,000 langkah).
Target durasi tidur (misal: 8 jam).
Target konsumsi air (misal: 2000 ml).

Aplikasi akan memberikan notifikasi atau peringatan jika target harian belum tercapai.

3. Ringkasan dan ringkasan Mingguan/Bulanan
Menampilkan ringkasan data kesehatan dalam bentuk ringkasan untuk:
Langkah harian selama satu minggu/bulan.
Durasi tidur mingguan/bulanan.
Konsumsi air rata-rata.

Ringkasan ini memberikan pengguna gambaran visual tentang konsistensi aktivitas kesehatannya.

4. Peringatan & Pengingat Otomatis
Memberikan peringatan jika pengguna belum mencapai target harian.
Mengirimkan pengingat harian untuk mencatat data kesehatan periode.

---
Struktur Program dan Penggunaan Kriteria

1. Input & Output
Input: Jumlah langkah, durasi tidur, jumlah air.
Output: Ringkasan harian, ringkasan mingguan/bulanan, status apakah target harian tercapai atau belum.

2. Tipe Data & Operator
Tipe Data: Integer/float untuk angka (langkah, jam tidur, air), string untuk nama data kesehatan.
Operator: Operator aritmatika untuk menghitung rata-rata, perbandingan untuk mengecek apakah target tercapai.

3. Loop (Perulangan)
Mengulangi proses input harian dan menampilkan ringkasan mingguan atau bulanan.
Menampilkan ringkasan data kesehatan dalam bentuk ringkasan berdasarkan catatan mingguan/bulanan.

4. Percabangan
Mengecek apakah setiap input mingguan/bulanan mencapai target atau tidak.
Memberikan peringatan jika target harian belum tercapai.

5. Konsep Array
Menyimpan data kesehatan harian dalam bentuk array untuk langkah, durasi tidur, dan konsumsi air.
Data array akan digunakan untuk menghitung rata-rata mingguan/bulanan dan menampilkan ringkasan.

---
Alur Penggunaan Aplikasi

1. Pengaturan Awal
Pengguna pertama kali memasukkan target harian untuk langkah, durasi tidur, dan jumlah air yang ingin dicapai.
2. Pencatatan Data Harian
Setiap hari, pengguna memasukkan data kesehatan harian. Aplikasi menyimpan data ini dan langsung mengecek apakah target harian terpenuhi.
3. Peringatan Harian
Jika target tidak tercapai dalam setiap waktu, aplikasi akan memberikan peringatan untuk mengingatkan pengguna.
5. Ringkasan
Pada akhir minggu atau bulan, pengguna dapat melihat ringkasan progres kesehatannya. Aplikasi menampilkan ringkasan yang menunjukkan tren kesehatan pengguna, misalnya apakah jumlah langkah cenderung meningkat atau menurun.
6. Penyesuaian Target
Pengguna dapat menyesuaikan targetnya kapan saja berdasarkan progres dan kebutuhan yang dirasa cocok.
---
Teknologi dan Antarmuka
Antarmuka Desktop:
Dibuat dengan GUI untuk tampilan yang lebih menarik.
