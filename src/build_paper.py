"""Bangun PDF ringkasan riset: python src/build_paper.py (lihat requirements-paper.txt)."""
from pathlib import Path
import json
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'MBG_Catatan_Riset.pdf'
metrics=json.loads((ROOT/'data/processed/hasil_ringkas.json').read_text())
assert metrics['entri_utama']==374 and round(metrics['top_share_persen'],2)==47.82
INK=HexColor('#203345');RED=HexColor('#953b45');PALE=HexColor('#f3f1ec');LINE=HexColor('#d7dde0')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='TitleMBG',fontName='Times-Bold',fontSize=25,leading=28,textColor=INK,spaceAfter=7))
styles.add(ParagraphStyle(name='SubMBG',fontName='Times-Roman',fontSize=14,leading=18,textColor=INK,spaceAfter=11))
styles.add(ParagraphStyle(name='BodyMBG',fontName='Times-Roman',fontSize=10.5,leading=14.4,alignment=TA_JUSTIFY,spaceAfter=7))
styles.add(ParagraphStyle(name='SectionMBG',fontName='Helvetica-Bold',fontSize=12,leading=16,textColor=RED,spaceBefore=10,spaceAfter=7))
styles.add(ParagraphStyle(name='SmallMBG',fontName='Helvetica',fontSize=8.2,leading=11,textColor=INK,spaceAfter=5))
styles.add(ParagraphStyle(name='CaptionMBG',fontName='Times-Italic',fontSize=9,leading=12,textColor=INK,spaceAfter=9))
styles.add(ParagraphStyle(name='RefMBG',fontName='Times-Roman',fontSize=9,leading=12,spaceAfter=7,wordWrap='CJK'))
story=[]
def p(text,style='BodyMBG'):story.append(Paragraph(text,styles[style]))
def h(text):p(text,'SectionMBG')
def fig(name,width=170*mm):
    im=Image(str(ROOT/'figures'/name));im.drawHeight=width*im.imageHeight/im.imageWidth;im.drawWidth=width;story.append(im)
def table(rows,widths):
    t=Table([[Paragraph(str(v),styles['SmallMBG']) for v in row] for row in rows],colWidths=widths,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),PALE),('LINEBELOW',(0,0),(-1,0),.7,LINE),
                          ('LINEBELOW',(0,-1),(-1,-1),.7,LINE),('VALIGN',(0,0),(-1,-1),'TOP'),
                          ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
    story.append(t);story.append(Spacer(1,7))
def footer(canvas,doc):
    canvas.setStrokeColor(LINE);canvas.line(20*mm,17*mm,190*mm,17*mm)
    canvas.setFont('Helvetica',7.5);canvas.setFillColor(INK)
    canvas.drawString(20*mm,12*mm,'MBG di Balik Angka Kasus | Catatan riset eksploratif | 18 September 2026')
    canvas.drawRightString(190*mm,12*mm,str(doc.page))

p('CATATAN RISET EKSPLORATIF - TUGAS MATERI 04','SmallMBG')
p('MBG di Balik Angka Kasus','TitleMBG')
p('Mengapa menghitung laporan saja tidak cukup?','SubMBG')
p('<b>Muhammad Fierlyan Irwandi</b> | NIM 3224600051<br/>Teknik Komputer, Politeknik Elektronika Negeri Surabaya<br/>Pengantar Kecerdasan Artifisial dan Pembelajaran Mesin','SmallMBG')
p('Versi 2.0 | Snapshot 18 September 2026 | Belum ditelaah sejawat','SmallMBG')
h('Abstrak')
p('Kajian ini mengeksplorasi distribusi dan konsentrasi besaran laporan publik terkait dugaan maupun kejadian keracunan Makan Bergizi Gratis (MBG). Tabel Wikipedia versi tetap menghasilkan 419 entri yang dikurasi menjadi 374 entri analisis utama. Unit observasi adalah blok laporan dalam tabel, bukan orang unik atau kejadian epidemiologis yang telah dideduplikasi. Median jumlah yang dilaporkan adalah 32 orang dan rata-ratanya 97,75 orang. Sebanyak 38 entri terbesar (10,16%) memuat 47,82% penjumlahan angka pada subset utama. Pola konsentrasi tetap muncul pada dua skenario kepekaan. Hasil mendukung penyajian frekuensi bersama skala dampak. Kajian tidak mengestimasi risiko per porsi, total nasional korban unik, maupun efek kausal program.')
p('<b>Kata kunci:</b> MBG; exploratory data analysis; keamanan pangan; kualitas data.','SmallMBG')
h('1. Pendahuluan')
p('Jumlah laporan sering menjadi ringkasan cepat persoalan keamanan pangan, tetapi setiap laporan dapat memuat skala yang berbeda. Pertanyaan kajian ini adalah seberapa beragam dan terkonsentrasi angka orang yang dilaporkan dalam entri publik terkait MBG. Isu pelaporan tetap aktual: BGN pada 15 September 2026 menyampaikan rencana aplikasi penilaian layanan oleh sekolah [2]. Informasi ini menjadi konteks, bukan penjelas kausal hasil.')
h('2. Data dan metode')
p('Sumber adalah bagian MBG pada tabel Wikipedia revisi 29876794, diperbarui 18 September 2026 pukul 04.19 UTC [1]. Tautan rujukan per entri dan snapshot HTML dipertahankan. Satu entri didefinisikan sebagai satu blok referensi. Parser mengenali sel gabungan sehingga angka bersama untuk beberapa sekolah hanya dihitung sekali. Entri dapat tetap mencakup lebih dari satu kejadian atau tumpang tindih dengan entri lain.')
p('Analisis utama mensyaratkan angka literal, satu tanggal harian dalam 6 Januari 2025-18 September 2026, URL artikel yang spesifik, dan tidak ada konflik yang ditemukan. Periode berawal dari peluncuran nasional [4]. Kata seperti "ratusan", batas numerik, serta angka kosong tidak diimputasi. Audit manual terarah dilakukan atas beberapa nilai besar dan rujukan bermasalah; seluruh artikel belum diverifikasi independen.')
table([['Komponen','Jumlah / definisi'],['Entri tersedia','419 entri pada 35 provinsi tercantum'],['Subset utama','374 entri; 13 Jan 2025-16 Sep 2026'],['Dikeluarkan, tetap disimpan','45 entri (10,74%), beserta alasan eksklusi']], [70*mm,100*mm])

story.append(PageBreak())
h('3. Hasil: distribusi dan konsentrasi')
p('Median sebesar 32 jauh di bawah rata-rata 97,75 orang per entri. Distribusi miring ke kanan: sejumlah laporan berangka besar menarik mean ke atas. Nilai besar tidak otomatis dihapus sebagai outlier karena dapat merepresentasikan informasi substantif, walaupun ketidakseragaman skala pelaporan tetap menjadi batasan.')
fig('01_distribusi.png',155*mm)
p('<b>Gambar 1.</b> Distribusi jumlah orang yang dilaporkan pada 374 entri utama. Histogram memakai lebar bin 25 orang. Garis vertikal menunjukkan median dan mean.','CaptionMBG')
p('Untuk mengukur konsentrasi, nilai diurutkan menurun. Dipilih k = ceil(0,10 x n), lalu porsi dihitung sebagai jumlah pada k entri terbesar dibagi penjumlahan pada seluruh subset. Dengan n = 374, k = 38 atau 10,16% entri. Kelompok ini memuat 47,82% jumlah yang dijumlahkan. Entri bernilai setidaknya 100 orang berjumlah 115 (30,75%) dan memuat 81,17% jumlah pada subset.')
fig('02_konsentrasi.png',155*mm)
p('<b>Gambar 2.</b> Kurva kumulatif dari entri terbesar ke terkecil. Denominator adalah penjumlahan angka laporan pada subset, bukan populasi penerima MBG. Porsi tersebut tidak boleh diterjemahkan menjadi persentase dapur atau insiden nasional.','CaptionMBG')

story.append(PageBreak())
h('4. Sebaran wilayah dan pemeriksaan kepekaan')
fig('04_provinsi.png')
p('<b>Gambar 3.</b> Delapan provinsi dengan penjumlahan angka terbesar pada subset utama. Besaran ini mencerminkan catatan yang tersedia dan bukan peringkat keamanan; cakupan program dan pelaporan dapat berbeda antarwilayah.','CaptionMBG')
p('Uji kepekaan membandingkan subset utama dengan dua skenario: membuang lima entri terbesar, serta melonggarkan aturan menjadi seluruh angka literal bertahun 2025-2026. Skenario longgar tetap mencakup entri bermasalah sehingga hanya dipakai sebagai pembanding, bukan estimasi alternatif yang diutamakan.')
table([['Skenario','n','Median','Porsi sekitar 10% terbesar'],
       ['Utama','374','32','47,82% (38 entri)'],
       ['Tanpa lima terbesar','369','31','44,82% (37 entri)'],
       ['Seluruh angka literal 2025-2026','387','33','48,37% (39 entri)']], [78*mm,17*mm,22*mm,53*mm])
p('Konsentrasi tetap terlihat pada kedua pembanding. Rentang 44,82%-48,37% adalah hasil perubahan skenario, bukan interval kepercayaan. Tidak ada inferensi ke populasi nasional karena pengumpulan data tidak menggunakan sampel acak.')
h('5. Diskusi dan implikasi untuk machine learning')
p('Temuan memperlihatkan mengapa frekuensi perlu disajikan bersama skala dampak. Satu entri berbobot satu dalam hitungan laporan, tetapi angka orang di dalamnya dapat berbeda jauh. Statistik sederhana seperti median, mean, dan distribusi membantu pembaca memahami perbedaan itu sebelum menarik kesimpulan kebijakan.')
p('Untuk tugas identifikasi fitur dan target, X hipotetis berisi provinsi, tahun, dan bulan; y adalah jumlah yang tercatat pada entri. Ini konteks regresi atas besaran laporan, bukan prediksi keamanan makanan. Variabel jumlah mentah dan kelas yang diturunkan dari y tidak boleh menjadi fitur. Pemodelan belum dilakukan. Data tambahan perlu mencakup ID kejadian, jumlah porsi per dapur dan tanggal, definisi kasus, serta pembaruan konfirmasi. Pembagian latih-uji harus memperhatikan waktu dan kelompok kejadian yang sama.')

story.append(PageBreak())
h('6. Audit sumber dan keterbatasan')
p('Pemeriksaan manual menemukan bahwa angka 1.333 untuk Bandung Barat mengakumulasi beberapa kejadian [3]. Entri tersebut dikeluarkan karena meliputi beberapa tanggal. Entri 810 di Blora juga dikeluarkan karena sumber menyebut 444 bergejala tanpa definisi yang cukup jelas [5]. Angka 800 di Batang diperlakukan sebagai perkiraan karena laporan ANTARA memakai kata "sekitar" [6]. Pemeriksaan rujukan menemukan satu entri Padang Panjang yang menunjuk artikel Lampung Utara. Catatan rinci dan keputusan tersimpan pada audit sumber.')
p('Terdapat lima batas utama. Pertama, daftar tidak lengkap dan dipengaruhi seleksi pemberitaan. Kedua, unit laporan tidak seragam dan orang/kejadian antarentri belum dideduplikasi. Ketiga, dugaan dan konfirmasi belum dipisahkan secara konsisten. Keempat, denominator porsi makan yang sesuai tidak tersedia. Kelima, tidak ada kelompok pembanding atau rancangan kausal. Karena itu, kajian tidak menyimpulkan risiko per porsi, provinsi paling berbahaya, maupun manfaat atau kerugian bersih program.')
h('7. Kesimpulan dan reproduksi')
p('Dalam subset yang dipilih, besaran laporan sangat tidak merata: sekitar sepuluh persen entri memuat hampir separuh jumlah yang dijumlahkan. Pola bertahan pada pemeriksaan kepekaan. Pelaporan MBG akan lebih informatif bila frekuensi disertai skala dampak dan definisi unit yang jelas.')
p('Repositori menyimpan snapshot, CSV 419 entri, 45 eksklusi, kode parser, notebook dengan 14 sel kode terjalankan, lima grafik, dan pemeriksaan otomatis. Snapshot dan adaptasi data berlisensi CC BY-SA 4.0. Kode asli berlisensi MIT. Tautan proyek: <link href="https://github.com/feboyfierlyan/mbg-safety-eda" color="#953b45">github.com/feboyfierlyan/mbg-safety-eda</link>.')
h('Referensi')
refs=[
    '[1] Kontributor Wikipedia. Daftar kasus keracunan massal makan siang gratis, bagian MBG. Revisi 29876794, 18 September 2026. <link href="https://id.wikipedia.org/w/index.php?title=Daftar_kasus_keracunan_massal_makan_siang_gratis&amp;oldid=29876794" color="#953b45">Versi permanen</link>.',
    '[2] Badan Gizi Nasional. BGN Siapkan Aplikasi Rating MBG, Sekolah Diminta Tak Segan Laporkan SPPG Bermasalah. 15 September 2026. <link href="https://www.bgn.go.id/news/siaran-pers/bgn-siapkan-aplikasi-rating-mbg-sekolah-diminta-tak-segan-laporkan-sppg-bermasalah" color="#953b45">Siaran pers</link>.',
    '[3] Kompas.com. Update Korban Keracunan MBG di Bandung Barat Tembus 1.333 Orang. 25 September 2025. <link href="https://bandung.kompas.com/read/2025/09/25/165121378/update-korban-keracunan-mbg-di-bandung-barat-tembus-1333-orang" color="#953b45">Artikel sumber</link>.',
    '[4] Badan Gizi Nasional. BGN akan Memulai Program MBG Secara Bertahap. 5 Januari 2025. <link href="https://www.bgn.go.id/news/artikel/bgn-akan-memulai-program-mbg-secara-bertahap" color="#953b45">Artikel BGN</link>.',
    '[5] MuriaNews. Penyebab 810 Siswa Keracunan MBG, Dinkes Blora: Makanan Terkontaminasi. 9 Desember 2025. <link href="https://berita.murianews.com/zulkifli-fahmi/455559/penyebab-810-siswa-keracunan-mbg-dinkes-blora-makanan-terkontaminasi" color="#953b45">Artikel audit</link>.',
    '[6] ANTARA Jateng. Ratusan siswa SMK Kandeman Batang keracunan masakan program MBG. 31 Oktober 2025. <link href="https://jateng.antaranews.com/amp/berita/606837/ratusan-siswa-smk-kandeman-batang-keracunan-masakan-program-mbg" color="#953b45">Artikel audit</link>.',
    '[7] Sigit, R. Materi 04: Python dan Data Exploration untuk Machine Learning. Materi kuliah PENS; instruksi tugas pada slide 22.'
]
for r in refs:p(r,'RefMBG')
p('Seluruh sumber daring diakses pada 18 September 2026. Ini catatan riset perkuliahan, bukan publikasi yang telah ditelaah sejawat.','SmallMBG')
doc=SimpleDocTemplate(str(OUT),pagesize=A4,rightMargin=20*mm,leftMargin=20*mm,topMargin=18*mm,bottomMargin=22*mm,
                     title='MBG di Balik Angka Kasus',author='Muhammad Fierlyan Irwandi',subject='EDA laporan publik MBG, snapshot 18 September 2026')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(OUT)
