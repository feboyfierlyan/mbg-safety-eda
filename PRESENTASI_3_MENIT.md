# Naskah presentasi 3 menit

**Muhammad Fierlyan Irwandi · 3224600051**  
Mata kuliah: Pengantar Kecerdasan Artifisial dan Pembelajaran Mesin

Target durasi sekitar 3 menit pada kecepatan 115–125 kata/menit. Gunakan lima penanda waktu berikut saat latihan. Buka notebook atau HTML dan tampilkan grafik yang disebutkan.

## 0:00–0:25 · Tujuan dan dataset

Selamat pagi. Saya Muhammad Fierlyan Irwandi, NIM 3224600051. Pada tugas ini, saya melakukan exploratory data analysis terhadap dataset Wine Quality merah dari UCI. Tujuannya memahami hubungan pengukuran fisikokimia dengan kualitas wine serta menemukan masalah data sebelum pemodelan. Dataset berisi 1.599 observasi dengan sebelas fitur dan satu target, yaitu skor quality.

## 0:25–0:55 · Struktur dan kualitas data

Saya memulai dengan head, shape, info, dan describe. Semua kolom terbaca sebagai angka. Tidak ditemukan nilai kosong, tetapi ada 240 baris identik tambahan, sekitar lima belas persen. Saya mempertahankan data asli karena tidak tersedia identitas sampel untuk memastikan penyebab pengulangan. Namun, jika membuat model, kombinasi fitur identik perlu ditempatkan pada partisi yang sama agar tidak tersebar ke data latih dan uji.

## 0:55–1:25 · Distribusi target [tampilkan grafik 2]

Diagram batang menunjukkan bahwa skor lima dan enam mendominasi sekitar delapan puluh dua setengah persen data. Sebaliknya, skor tiga hanya memiliki sepuluh observasi, dan skor delapan hanya delapan belas. Artinya, target tidak seimbang. Model yang terlihat akurat secara keseluruhan belum tentu mengenali kualitas yang jarang muncul. Karena itu, evaluasi klasifikasi perlu melihat macro-F1 dan confusion matrix per kelas.

## 1:25–2:10 · Hubungan fitur dengan target [grafik 3 dan 5]

Boxplot menunjukkan median alkohol sebesar 9,7 pada skor lima, lalu 10,5 pada skor enam, 11,5 pada skor tujuh, dan 12,15 pada skor delapan. Meskipun demikian, distribusinya masih tumpang tindih. Heatmap memperkuat pola ini: korelasi alkohol dengan kualitas sekitar positif 0,48, sedangkan keasaman volatil sekitar negatif 0,39. Jadi, keduanya layak diuji sebagai fitur. Namun, korelasi tidak membuktikan sebab-akibat dan belum menunjukkan akurasi model. Hasilnya juga relatif serupa ketika baris identik dihitung sekali.

## 2:10–3:00 · Nilai ekstrem dan kesimpulan

Pemeriksaan IQR menandai 155 nilai gula residual sebagai kandidat outlier. Saya tidak langsung menghapusnya karena nilai ekstrem belum tentu salah. Dari seluruh analisis, lima temuan utamanya adalah data lengkap tetapi berulang, target tidak seimbang, hubungan positif alkohol, hubungan negatif keasaman volatil, serta kandidat outlier pada gula residual. Sebelas pengukuran menjadi fitur X, sementara quality menjadi target y dan tidak dimasukkan ke fitur. Notebook ini berhenti pada EDA. Tahap berikutnya adalah memvalidasi duplikasi, menyiapkan pembagian data yang tepat, dan mempelajari preprocessing hanya dari data latih. Terima kasih.

## Pertanyaan yang mungkin muncul

- **Mengapa memilih dataset ini?** Data resmi, ukurannya melampaui 100 baris, seluruh variabel mudah dibaca sebagai tabel, dan temuan EDA dapat dihubungkan dengan keputusan pemodelan.
- **Mengapa tidak langsung menghapus duplikat?** Tidak ada ID sampel yang membuktikan bahwa catatan tersebut merupakan kesalahan. Saya mempertahankan sumber, lalu melakukan perbandingan dengan deduplikasi.
- **Mengapa menghitung Spearman?** Target merupakan skor ordinal. Spearman memeriksa hubungan berdasarkan peringkat sebagai pelengkap Pearson yang merangkum hubungan linear.
- **Apakah alkohol paling penting bagi model?** Belum bisa disimpulkan. Alkohol memiliki korelasi Pearson terbesar dengan target di antara fitur, tetapi pentingnya fitur bagi model harus dievaluasi tersendiri.
- **Apa perbedaan missing value dan outlier?** Missing value berarti nilai tidak tersedia. Outlier berarti nilai tersedia tetapi relatif ekstrem menurut suatu aturan statistik.
- **Apa batas hasilnya?** Analisis ini bersifat deskriptif pada sampel wine merah tertentu. Tidak menguji sebab-akibat dan belum mengukur performa prediksi.
