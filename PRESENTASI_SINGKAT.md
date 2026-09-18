# Belajar Lebih Lama, Nilai Lebih Tinggi?

**Muhammad Fierlyan Irwandi · 3224600051**  
Target penyampaian: **sekitar 2 menit**, dengan jeda. Cukup tampilkan satu grafik: [rata-rata nilai tiap kelompok](figures/03_belajar_dan_nilai.png).

## Naskah yang diucapkan

### Pembuka · 0:00–0:20

Kalau ingin nilai lebih tinggi, kita sering mendengar satu saran: belajar lebih lama.

Tapi apakah siswa yang belajar paling lama selalu mendapat nilai paling tinggi?

Saya Fierlyan. Untuk menjawabnya, saya membandingkan waktu belajar dan nilai akhir 649 siswa.

### Data · 0:20–0:40

Datanya berasal dari dua sekolah di Portugal, untuk mata pelajaran Bahasa Portugis. Ini data historis dari UCI, bukan survei siswa Indonesia.

Waktu belajar dibagi menjadi empat kelompok. Nilai saya tampilkan pada skala nol sampai seratus agar mudah dibaca.

### Temuan · 0:40–1:15

Perhatikan grafik ini.

Kelompok yang belajar kurang dari dua jam per minggu memiliki rata-rata nilai sekitar 54. Pada kelompok lima sampai sepuluh jam, rata-ratanya sekitar 66.

Tetapi kelompok yang belajar lebih dari sepuluh jam justru rata-ratanya sekitar 65.

Jadi, rata-rata cenderung naik, tetapi tidak terus naik pada setiap kelompok.

### Makna dan penutup · 1:15–2:00

Apakah berarti lima sampai sepuluh jam adalah waktu belajar terbaik? Belum tentu.

Kelompok paling lama hanya berisi 35 siswa. Kemampuan awal dan kondisi belajar mereka juga bisa berbeda. Analisis ini menunjukkan hubungan, bukan membuktikan sebab-akibat.

Kesimpulannya: durasi belajar berkaitan dengan nilai, tetapi belum cukup untuk menjelaskan hasil setiap siswa.

Durasi belajar memberi petunjuk. Untuk memahami hasil seorang siswa, kita tetap perlu melihat gambaran yang lebih lengkap.

Terima kasih.

## Cara membawakan

- Setelah pertanyaan pembuka, berhenti satu detik dan lihat audiens.
- Ketika menyebut 54, 66, dan 65, tunjuk batang yang sesuai. Angka boleh dibulatkan saat berbicara.
- Ucapkan “belum tentu” dengan tenang, tanpa memberi kesan belajar lama itu sia-sia.
- Jangan membaca definisi statistik atau seluruh tabel. Grafik lain menjadi cadangan.
- Penanda waktu adalah panduan latihan. Rekam sekali dengan timer; durasi aktual bergantung tempo dan jeda.

## Jawaban singkat jika ditanya

**Apa inti tugas ini?**  
Membandingkan rata-rata nilai empat kelompok waktu belajar, lalu memeriksa apakah polanya terus meningkat.

**Apa arti satu baris data?**  
Satu catatan siswa pada mata pelajaran Bahasa Portugis; ada 649 baris dari dua sekolah.

**Kenapa nilainya dikali lima?**  
Nilai asli berskala 0–20. Mengalikan lima membuatnya 0–100, misalnya 12 menjadi 60. Ini hanya perubahan skala, bukan penyetaraan aturan kelulusan.

**Jadi harus belajar lima sampai sepuluh jam?**  
Data ini tidak bisa menetapkan jam ideal. Kita tidak melakukan eksperimen; perbedaan rata-rata bisa berkaitan dengan banyak faktor.

**Kenapa lebih dari sepuluh jam tidak paling tinggi?**  
Penyebabnya belum dapat ditentukan. Kelompok itu kecil, dan kemampuan maupun keadaan siswa bisa berbeda. Selisihnya juga hanya sekitar 0,8 poin dari kelompok 5–10 jam.

**Apa fitur dan target untuk ML?**  
Targetnya nilai akhir. Contoh fitur: kategori waktu belajar serta nilai periode pertama dan kedua, jika prediksi dilakukan setelah kedua nilai itu tersedia. Pada awal tahun, nilai-nilai tersebut belum boleh dipakai.

**Apa arti korelasi 0,92 pada grafik cadangan?**  
Nilai periode kedua yang lebih tinggi cenderung diikuti nilai akhir lebih tinggi. Itu ukuran hubungan, bukan akurasi prediksi 92%.

**Apakah nilai nol dibuang?**  
Tidak. Ada 15 nilai nol dan semuanya dipertahankan karena sumber mengizinkan nilai 0–20. Penyebab nilai nol tidak dijelaskan.

**Apakah ini berlaku untuk mahasiswa Indonesia?**  
Belum tentu. Data historis berasal dari dua sekolah di Portugal dan satu mata pelajaran. Hasil hanya mendeskripsikan sampel ini.

**Mengapa tidak membuat model?**  
Tugas ini berfokus pada EDA. Memahami isi dan batas data perlu dilakukan sebelum memprediksi.
