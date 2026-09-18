# Kamus data dan keputusan analisis

Sumber: Cortez (2008), [Student Performance, UCI](https://doi.org/10.24432/C5TG7T), lisensi CC BY 4.0. File mentah `student-por.csv` dipisahkan dengan titik koma; file analisis memakai koma.

Unit observasi: satu catatan siswa pada mata pelajaran Bahasa Portugis. Jumlah 649 baris, dua sekolah. Analisis memakai seluruh baris dan memilih enam kolom:

- **sekolah** ← `school`: GP atau MS; kategori, bukan urutan kualitas sekolah.
- **waktu_belajar** ← `studytime`: 1 = <2 jam, 2 = 2–5 jam, 3 = 5–10 jam, 4 = >10 jam per minggu. Kategori berurutan, bukan jam pasti. Label mengikuti sumber; ambiguitas batas tepat 5 jam tidak diperbaiki tanpa data asli jam individual.
- **absensi** ← `absences`: jumlah ketidakhadiran sekolah yang tercatat; dipertahankan sebagai konteks, bukan fitur prediksi dalam contoh karena waktu rekap belum jelas.
- **nilai_periode1** ← `G1 × 5`: nilai periode pertama pada skala tampilan 0–100.
- **nilai_periode2** ← `G2 × 5`: nilai periode kedua pada skala tampilan 0–100.
- **nilai_akhir** ← `G3 × 5`: nilai akhir pada skala tampilan 0–100; target analisis.

G1, G2, G3 semula berskala 0–20. Penskalaan linier tidak mengubah urutan siswa, bentuk relatif distribusi, atau korelasi. Ini bukan penyetaraan standar nilai Indonesia. Nol tidak dianggap data hilang. Angka di grafik memakai satu desimal, perhitungan tetap memakai presisi asli.

Tidak ada imputasi, penghapusan baris, atau penggabungan dengan `student-mat.csv`. Pada berkas analisis, dua siswa bisa memiliki enam nilai identik; hal itu tidak cukup untuk menyatakan duplikasi siswa. Pemeriksaan duplikat identik dilakukan atas seluruh 33 kolom mentah.

## Istilah statistik dalam bahasa sederhana

- **Rata-rata:** jumlah seluruh nilai dibagi banyaknya siswa.
- **Median:** nilai tengah setelah semua nilai diurutkan.
- **n:** banyaknya siswa yang dihitung dalam kelompok.
- **Selisih poin:** 66,1 dikurangi 54,2 adalah sekitar 11,9 poin; bukan kenaikan 11,9 persen.
- **Korelasi Pearson:** ukuran hubungan linier antara dua angka, dari -1 sampai +1. Bukan persentase akurasi dan bukan bukti sebab-akibat.
- **Analisis sensitivitas:** menghitung ulang setelah mengubah satu keputusan, untuk melihat apakah pola berubah. Bukan alasan menghilangkan data dari hasil utama.

## Asal dan integritas

Data mentah diunduh dari paket resmi UCI pada 18 September 2026. Salinan CSV dan dokumentasi variabel disimpan di `data/raw/`. DOI, URL unduh, langkah transformasi, serta SHA-256 berkas mentah dan turunan disimpan pada `data/provenance.json`.

Dataset berhubungan dengan studi tahun 2008. Tanggal unduh tidak boleh dilabeli sebagai tahun pengumpulan atau bukti bahwa data mewakili kondisi pendidikan terkini. Informasi sumber yang belum tersedia, seperti sebab nilai nol atau jam belajar persis, tidak direka.
