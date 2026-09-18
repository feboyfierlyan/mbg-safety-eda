# Kamus data dan definisi analitis

File utama: `data/processed/mbg_laporan.csv` (419 baris). Encoding UTF-8, delimiter koma. `jumlah_dilaporkan` boleh kosong. CSV menyimpan kedua kelompok, termasuk 45 entri yang tidak masuk analisis utama.

- `entry_id`: identitas deterministik, berupa nomor revisi dan posisi sel referensi HTML. Bukan ID kejadian epidemiologis.
- `tanggal_raw`: teks tanggal dari tabel, termasuk lebih dari satu tanggal jika ada.
- `tanggal`: tanggal ISO ketika dapat dibaca. Untuk beberapa tanggal lengkap, berisi tanggal pertama dan diberi penanda `beberapa_tanggal`; entri tersebut dikeluarkan dari analisis utama. Untuk tanggal berbasis bulan/rentang saja, nilainya kosong.
- `tahun`, `bulan`: penanda tahun dan bulan yang dapat dikenali dari sumber. Bulan/tahun saja tidak dijadikan tanggal harian buatan.
- `presisi_tanggal`: tanggal, beberapa_tanggal, rentang, bulan, atau tidak_tersedia.
- `provinsi`: nama provinsi; alias Aceh dan Kepulauan Bangka Belitung dinormalisasi.
- `kabupaten_kota`: lokasi administratif sebagaimana tercantum. Tidak dianggap kode wilayah resmi yang telah divalidasi.
- `lokasi_raw`: daftar sekolah/tempat dalam blok referensi, dipisahkan tanda `|`. Bukan hitungan sekolah aktual yang terstandar.
- `jumlah_raw`: teks asli kolom Bergejala, dengan beberapa sel dipisahkan `|`.
- `jumlah_dilaporkan`: angka atau jumlah komponen angka yang tertulis. Satuan orang dalam entri laporan, bukan orang unik nasional. Bentuk perkiraan yang dikenali tidak diubah menjadi angka analitis; untuk kasus Batang 800, angka dipertahankan untuk audit tetapi statusnya perkiraan.
- `status_angka`: angka_literal, kualitatif, batas_bukan_angka_pasti, perkiraan, tidak_tersedia, perkiraan_terverifikasi, atau komponen_tidak_jelas. Angka literal tidak berarti telah dikonfirmasi secara medis.
- `jumlah_baris_html`, `jumlah_sel_angka`: ukuran struktur tabel untuk audit parser; bukan proksi jumlah insiden atau jumlah sekolah sebenarnya.
- `source_url`: URL pertama pada catatan kaki sumber; dapat kosong atau berupa beranda, sehingga perlu diperiksa.
- `source_urls_json`: semua URL pada catatan kaki, termasuk tautan arsip jika tersedia.
- `masalah_rujukan`: masalah yang ditemukan, atau kosong jika tidak ada masalah yang ditandai. Kosong tidak menjamin verifikasi penuh.
- `status_audit`: hasil pemeriksaan manual terarah, atau belum_diperiksa_individual.
- `masuk_analisis_utama`: boolean hasil aturan inklusi.
- `alasan_eksklusi`: semua alasan yang ditemukan; satu entri dapat memiliki beberapa alasan. Grafik alur memakai tahap eksklusif agar tidak menghitung ulang entri yang sama.
- `snapshot_revision`, `diakses_pada`: versi dan tanggal akses untuk reproduksi.

## Rumus konsentrasi

Urutkan nilai y menurun. Ambil `k = ceil(0,10 × n)`. Porsi terbesar adalah `100 × sum(y_terbesar_k) / sum(y_seluruh_subset)`. Karena pembulatan, 38 dari 374 entri adalah 10,16%, bukan tepat 10,00%.

## Penggunaan yang tidak didukung

Tidak menghitung risiko individu/per porsi, tidak menyatakan kematian dari sel kosong, tidak menyebut semua angka sebagai siswa, tidak menyetarakan entri dengan dapur, dan tidak menafsirkan hasil sebagai perbandingan kausal provinsi atau tahun.
