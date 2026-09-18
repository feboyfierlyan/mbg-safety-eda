# Sumber dataset

- Nama: Wine Quality, subset wine merah (winequality-red.csv).
- Penyedia: UCI Machine Learning Repository.
- Halaman: https://archive.ics.uci.edu/dataset/186/wine+quality
- DOI: https://doi.org/10.24432/C56S3T
- Arsip unduhan: https://archive.ics.uci.edu/static/public/186/wine+quality.zip
- Alternatif CSV: https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv
- Diunduh: 18 September 2026.
- Lisensi dataset pada UCI: CC BY 4.0, https://creativecommons.org/licenses/by/4.0/.
- Atribusi: Cortez, P., Cerdeira, A., Almeida, F., Matos, T., & Reis, J. (2009). Wine Quality [Dataset].
- CSV disimpan identik dengan berkas unduhan, tanpa pengubahan isi atau nama kolom.
- Format: UTF-8/ASCII, pemisah titik koma, 1.599 baris data + header, 12 kolom.
- SHA-256: `4a402cf041b025d4566d954c3b9ba8635a3a8a01e039005d97d6a710278cf05e`

File `winequality.names` adalah metadata asli yang menyertai dataset. Skala target yang didefinisikan sumber adalah 0–10; skor yang muncul dalam subset merah adalah 3–8. Satuan fitur tidak dirinci pada metadata tersebut, sehingga laporan mempertahankan skala asli tanpa konversi.

Dataset hanya memuat hasil uji fisikokimia dan penilaian sensorik. Tidak tersedia ID sampel, varietas anggur, merek, atau harga. Deduplikasi pada notebook hanya digunakan sebagai analisis sensitivitas; CSV sumber tetap utuh.
