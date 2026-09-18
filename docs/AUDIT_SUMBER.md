# Audit sumber dan keputusan kurasi

Snapshot: revisi Wikipedia **29876794**, 18 September 2026, 04.19 UTC. Akses: 18 September 2026. Unit dataset adalah **entri laporan**, didefinisikan sebagai satu blok referensi pada tabel. Ini tidak selalu setara dengan satu wabah, satu dapur, satu sekolah, atau satu orang unik.

## Pemeriksaan struktur seluruh tabel

Parser memeriksa semua `rowspan` dan `colspan`, memastikan tujuh kolom logis, serta memproses tiap sel jumlah hanya sekali dalam blok referensinya. Beberapa sekolah dapat berbagi satu angka. Membaca tabel yang sudah diperluas lalu menjumlahkan setiap baris sekolah akan menggandakan angka tersebut.

Sebanyak 825 baris HTML, termasuk dua baris header, menghasilkan 419 entri. Lima baris tidak menjadi entri: satu baris TOTAL, tiga placeholder wilayah kosong, dan satu baris sekolah lanjutan tanpa angka maupun referensi. Satu baris bermuatan angka tetapi tanpa referensi tetap disimpan sebagai entri dan dikeluarkan dari analisis utama. Subtotal tertulis di sumber tidak dipakai; semua statistik dihitung ulang.

## Pemeriksaan manual terarah

Pemeriksaan ini menargetkan entri besar, rujukan berulang, dan representasi yang ambigu. **Bukan verifikasi independen atas seluruh 419 entri.** Entri yang belum diperiksa diberi status `belum_diperiksa_individual`. Rujukan berbentuk URL artikel belum tentu menjamin artikel benar atau masih dapat diakses.

- **Bandung Barat, 22–24 September 2025, 1.333** (`r298c6`). [Kompas, 25 September 2025](https://bandung.kompas.com/read/2025/09/25/165121378/update-korban-keracunan-mbg-di-bandung-barat-tembus-1333-orang) menyatakan angka itu merupakan akumulasi beberapa kejadian. Dikeluarkan dari analisis utama karena blok meliputi beberapa tanggal. Tidak dipecah menjadi kejadian fiktif.
- **Blora, 26 November 2025, 810** (`r427c6`). [MuriaNews, 9 Desember 2025](https://berita.murianews.com/zulkifli-fahmi/455559/penyebab-810-siswa-keracunan-mbg-dinkes-blora-makanan-terkontaminasi) menyebut 810 tetapi uraian juga menyebut 444 bergejala. Definisi dan pembagi tidak cukup jelas untuk disamakan. Dikeluarkan, tanpa mengganti 810 menjadi 444 secara sepihak.
- **Batang, 31 Oktober 2025, 800** (`r358c6`). [ANTARA Jateng, 31 Oktober 2025](https://jateng.antaranews.com/amp/berita/606837/ratusan-siswa-smk-kandeman-batang-keracunan-masakan-program-mbg) memakai kata “sekitar”. Nilai 800 disimpan, tetapi status diubah menjadi perkiraan dan dikeluarkan dari statistik utama yang hanya memakai angka literal tanpa penanda perkiraan yang diketahui.
- **Kota Padang Panjang, 7 Oktober 2025, 29** (`r33c6`). Rujukan tertanam justru menuju [artikel tentang 11 siswa Lampung Utara pada Januari 2026](https://regional.kompas.com/read/2026/01/13/134340278/11-siswa-sd-di-lampung-utara-keracunan-makan-bergizi-gratis-kepsek-ngamuk). Ditandai salah lokasi dan dikeluarkan. Entri Lampung Utara yang menggunakan artikel yang sama tidak otomatis dikeluarkan.
- **Grobogan, Januari 2026, 803** (`r434c6`). [detikNews, 13 Januari 2026](https://news.detik.com/berita/d-8305630/803-orang-di-grobogan-diduga-keracunan-mbg-dari-menu-ayam) mendukung angka 803 orang terdampak. Pemeriksaan ini mendukung angka, bukan verifikasi seluruh rincian tanggal dan kausalitas.
- **Rembang, 3 September 2026, 777** (`r407c6`). [Media Indonesia, 3 September 2026](https://mediaindonesia.com/nusantara/929333/777-siswa-dan-guru-sma-negeri-1-lasem-rembang-diduga-keracunan-makan-bergizi-grati) merinci 752 siswa dan 25 guru. Jumlah 777 didukung. Dataset mencakup orang yang dilaporkan, tidak khusus siswa.
- **Sidoarjo, September 2026, 748** (`r649c6`). [detikJatim](https://www.detik.com/jatim/berita/d-8648306/korban-keracunan-mbg-di-sidoarjo-jadi-748-orang) mendukung angka 748 dalam pembaruan laporan. Tidak dianggap jumlah yang pasti final.
- **Nganjuk, tanggal tertulis 2 Oktober 2024, 7** (`r526c6`). Tanggal berada di luar periode kajian 2025–2026. Disimpan dalam data audit tetapi dikeluarkan dari analisis, tanpa menebak tahun yang benar.
- **Trenggalek, 15 September 2026, “77 Siswa + Guru”** (`r623c6`). Komponen tambahan tidak jelas pada teks tabel. Angka analitis dibiarkan kosong. Judul rujukan belum cukup untuk mengubah makna sel secara diam-diam.

## Aturan eksklusi utama

Semua entri diperlakukan dengan aturan yang sama: harus memiliki angka literal yang dapat diparsing, satu tanggal harian dalam 6 Januari 2025–18 September 2026, rujukan URL artikel yang spesifik, dan tidak memiliki konflik yang ditemukan dalam audit. Hasil: **374 entri utama**, **45 entri dikeluarkan**. Daftar lengkap dan alasan tersedia pada `data/processed/baris_dikecualikan.csv`.

Istilah “angka literal” hanya menjelaskan bentuk pencatatan, bukan kepastian klinis. Entri yang belum diaudit masih mungkin mengandung perkiraan, ketidaksesuaian definisi, tumpang tindih kejadian, atau angka yang kemudian direvisi.

## Makna perbandingan kepekaan

Skenario longgar memasukkan seluruh angka literal bertahun 2025–2026, termasuk entri yang ditandai bermasalah. Ini sengaja merupakan pembanding kualitas rendah, bukan pengganti analisis utama. Skenario lain membuang lima angka terbesar dari analisis utama. Keduanya membantu memeriksa apakah konsentrasi dampak sepenuhnya bergantung pada aturan kurasi atau beberapa nilai ekstrem.

Kedua skenario tidak menyelesaikan bias publikasi, kelengkapan daftar, ataupun ketiadaan denominator porsi makan. Tidak ada hasil yang ditafsirkan sebagai total nasional korban unik atau risiko per penerima MBG.
