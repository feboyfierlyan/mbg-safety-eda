# Validasi versi 2.0

Tanggal: 18 September 2026.

- Tabel sumber dikunci pada revisi 29876794; SHA-256 snapshot dan CSV tersimpan pada data/provenance.json.
- Ekstraksi seluruh tabel menghasilkan 419 entri; 374 memenuhi aturan utama dan 45 memiliki alasan eksklusi.
- Tiga pengujian otomatis lolos, mencakup angka ambigu, tanggal tidak lengkap, penggandaan rowspan, dan integritas subset.
- Contoh kontrol: 33 santri yang mencakup dua sekolah tetap 33, bukan 66; tiga angka terpisah 87, 76, 43 menjadi 206.
- Notebook valid sesuai nbformat v4; seluruh 14 sel kode dieksekusi berurutan dari kernel baru tanpa error.
- Lima gambar PNG tertanam dalam notebook dan HTML. Judul, label, legenda, sumber, dan denominator diperiksa visual.
- HTML tidak memerlukan script eksternal untuk menampilkan hasil; seluruh lima gambar tersimpan sebagai data inline dan memiliki teks alternatif.
- PDF final terdiri atas empat halaman. Semua halaman dirender dan ditinjau; tidak ada caption yang terpisah ke halaman kosong atau elemen terpotong.
- Naskah yang diucapkan berjumlah 242 kata, sekitar dua menit pada 120 kata/menit; target dengan jeda 2-2,5 menit. Durasi aktual belum direkam.
- Tautan berkas hasil di README diperiksa dan seluruhnya tersedia.

Batas validasi: pemeriksaan teknis dan audit sumber terarah tidak membuktikan seluruh laporan benar, lengkap, bebas tumpang tindih, atau terkonfirmasi medis. Status audit per entri disimpan dalam dataset.
