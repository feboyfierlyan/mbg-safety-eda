# Validasi versi 3.0

Tanggal pemeriksaan: 18 September 2026.

- Dataset mentah: 649 baris × 33 kolom; analisis: 649 baris × 6 kolom.
- Nol nilai kosong dan nol duplikat identik pada seluruh kolom mentah.
- Seluruh baris dipertahankan, termasuk 15 nilai akhir nol.
- SHA-256 CSV sumber dan turunan tercatat dalam `data/provenance.json`.
- Tiga pengujian otomatis lolos: integritas sumber, penskalaan ketiga nilai tanpa kehilangan nol/urutan, dan kategori waktu belajar beserta jumlah anggotanya.
- Notebook valid menurut nbformat v4. Sepuluh sel kode dijalankan berurutan dari kernel baru tanpa error.
- Empat grafik PNG tertanam dalam notebook dan HTML; HTML tidak membutuhkan script eksternal untuk membaca hasil dan memiliki empat teks alternatif gambar.
- Semua grafik memiliki judul, satuan, label sumbu, dan sumber. Grafik utama mulai dari nol; ukuran kelompok dicantumkan.
- Catatan riset PDF final terdiri dari tiga halaman yang dirender dan ditinjau secara visual.
- Naskah yang diucapkan berjumlah 193 kata: sekitar 1,6 menit pada 120 kata/menit, dengan target sekitar dua menit termasuk jeda. Durasi aktual belum direkam.
- Angka utama diperiksa konsistensinya pada notebook, grafik, README, PDF, dan naskah presentasi.
- Tautan berkas lokal pada README tersedia.

Pemeriksaan teknis ini tidak menjadikan data historis representatif untuk populasi lain dan tidak membuktikan hubungan sebab-akibat. Selisih rata-rata kelompok tidak diuji signifikansinya.
