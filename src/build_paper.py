"""Bangun catatan riset tiga halaman setelah notebook selesai dijalankan."""
from pathlib import Path
import json
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm

ROOT = Path(__file__).resolve().parents[1]
m = json.loads((ROOT/'data/processed/hasil_ringkas.json').read_text())
assert m['jumlah_siswa'] == 649
assert round(m['selisih_5_10_dengan_kurang2'], 1) == 11.9
assert round(m['r_periode2_akhir'], 2) == .92
INK, ACCENT, PALE, LINE = map(HexColor, ['#253449','#168278','#f1f5f6','#d2dbe0'])
styles = getSampleStyleSheet()
for name, font, size, leading, extra in [
    ('TitleStudy','Times-Bold',25,28,{'textColor':INK,'spaceAfter':9}),
    ('SubtitleStudy','Times-Roman',14,18,{'spaceAfter':10}),
    ('BodyStudy','Times-Roman',10.5,14.3,{'alignment':TA_JUSTIFY,'spaceAfter':7}),
    ('SectionStudy','Helvetica-Bold',12,16,{'textColor':ACCENT,'spaceBefore':9,'spaceAfter':7}),
    ('SmallStudy','Helvetica',8.2,11.3,{'spaceAfter':6}),
    ('CaptionStudy','Times-Italic',9,12,{'spaceAfter':8}),
    ('RefStudy','Times-Roman',9,12,{'spaceAfter':7}),
]:
    styles.add(ParagraphStyle(name=name,fontName=font,fontSize=size,leading=leading,**extra))
story=[]
def p(text, style='BodyStudy'): story.append(Paragraph(text, styles[style]))
def h(text): p(text,'SectionStudy')
def fig(name, width=155*mm):
    im=Image(str(ROOT/'figures'/name)); im.drawHeight=width*im.imageHeight/im.imageWidth; im.drawWidth=width
    story.append(im)
def table(rows, widths):
    t=Table([[Paragraph(str(x), styles['SmallStudy']) for x in row] for row in rows], colWidths=widths)
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),PALE),('LINEBELOW',(0,0),(-1,0),.7,LINE),
                          ('LINEBELOW',(0,-1),(-1,-1),.7,LINE),('VALIGN',(0,0),(-1,-1),'TOP'),
                          ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),4)]))
    story.append(t);story.append(Spacer(1,6))
def footer(canvas,doc):
    canvas.setStrokeColor(LINE);canvas.line(20*mm,17*mm,190*mm,17*mm)
    canvas.setFont('Helvetica',7.5);canvas.setFillColor(INK)
    canvas.drawString(20*mm,12*mm,'Waktu Belajar dan Nilai Akhir | Catatan riset eksploratif | Versi 3.0')
    canvas.drawRightString(190*mm,12*mm,str(doc.page))

p('CATATAN RISET EKSPLORATIF - TUGAS MATERI 04','SmallStudy')
p('Belajar Lebih Lama,<br/>Nilai Lebih Tinggi?','TitleStudy')
p('Analisis eksploratif waktu belajar dan nilai akhir 649 siswa','SubtitleStudy')
p('<b>Muhammad Fierlyan Irwandi</b> | NIM 3224600051<br/>Teknik Komputer, Politeknik Elektronika Negeri Surabaya<br/>Pengantar Kecerdasan Artifisial dan Pembelajaran Mesin','SmallStudy')
p('18 September 2026 | Data historis UCI | Catatan perkuliahan, belum ditelaah sejawat','SmallStudy')
h('Abstrak')
p('Apakah kelompok siswa yang belajar lebih lama memiliki rata-rata nilai lebih tinggi? Kajian ini menggunakan 649 catatan siswa mata pelajaran Bahasa Portugis dari dua sekolah di Portugal pada dataset UCI Student Performance. Seluruh baris dipertahankan. Nilai asli 0-20 dikalikan lima untuk tampilan 0-100. Rata-rata empat kategori waktu belajar per minggu adalah 54,2; 60,5; 66,1; dan 65,3. Kategori terlama tidak memiliki rata-rata tertinggi. Pola selisih antara kategori 5-10 jam dan kurang dari 2 jam tetap terlihat ketika sekolah dianalisis terpisah dan nilai nol dikeluarkan sebagai skenario pembanding. Hasil bersifat deskriptif; tidak menetapkan jam belajar ideal atau membuktikan efek kausal.')
p('<b>Kata kunci:</b> waktu belajar; prestasi siswa; exploratory data analysis; nilai akhir.','SmallStudy')
h('1. Pendahuluan')
p('Durasi belajar mudah dipahami, tetapi satu angka durasi belum tentu menjelaskan seluruh hasil belajar. Pertanyaan penelitian berfokus pada hubungan kategori waktu belajar mingguan dengan rata-rata nilai akhir. Analisis juga memeriksa jumlah siswa per kelompok, sebaran nilai, serta hubungan nilai periode kedua dengan nilai akhir. Tujuannya adalah memahami data sebelum mempertimbangkan model prediksi.')
h('2. Data dan metode')
p('Sumber adalah student-por.csv dari UCI [1], yang dikumpulkan melalui laporan sekolah dan kuesioner. Dataset berhubungan dengan studi tahun 2008 [2] dan diunduh pada 18 September 2026; tanggal unduh bukan tahun data. Tabel mentah memiliki 649 baris dan 33 kolom. Enam kolom dipilih: sekolah, kategori waktu belajar, absensi, dan tiga nilai periode. File matematika tidak digabung karena sebagian siswa muncul pada kedua mata pelajaran.')
p('Empat kategori waktu belajar mengikuti sumber: &lt;2, 2-5, 5-10, dan &gt;10 jam per minggu. Kode kategori bukan jam pasti. Nilai G1, G2, G3 dikali lima sebagai penskalaan aritmetis, bukan penyetaraan standar nilai Indonesia. Tidak ada nilai kosong atau duplikat identik pada 33 kolom mentah. Sebanyak 15 nilai akhir nol dipertahankan karena berada dalam rentang sah sumber. Tidak ada imputasi atau penghapusan baris.')
p('Statistik yang digunakan adalah frekuensi, rata-rata, median, rentang, dan korelasi Pearson untuk pasangan nilai. Visualisasi memakai histogram, diagram batang, dan scatter plot. Pemeriksaan tambahan dilakukan per sekolah dan tanpa nilai nol. Tidak dilakukan eksperimen, estimasi efek kausal, atau pengujian signifikansi perbedaan kelompok.')

story.append(PageBreak())
h('3. Hasil')
table([['Waktu belajar / minggu','Jumlah siswa','Rata-rata nilai','Median'],
       ['<2 jam','212','54,2','55'],['2-5 jam','305','60,5','60'],
       ['5-10 jam','97','66,1','65'],['>10 jam','35','65,3','65']],
      [62*mm,36*mm,40*mm,32*mm])
p('Rata-rata keseluruhan adalah 59,53 dan median 60; rentang teramati 0-95. Kelompok 2-5 jam paling banyak, yaitu 305 siswa (47,0%). Kelompok &gt;10 jam hanya mencakup 35 siswa (5,4%), sehingga rata-rata antar kategori berasal dari ukuran kelompok yang tidak sama.')
fig('03_belajar_dan_nilai.png',170*mm)
p('<b>Gambar 1.</b> Rata-rata nilai akhir berdasarkan kategori waktu belajar. Nilai 0-100 adalah nilai asli dikali lima; n adalah jumlah siswa. Sumbu vertikal dimulai dari nol. Batang menunjukkan ringkasan kelompok, bukan efek kausal.','CaptionStudy')
p('Selisih rata-rata kategori 5-10 jam dengan &lt;2 jam adalah 11,9 poin. Kategori &gt;10 jam memiliki rata-rata 0,8 poin lebih rendah daripada 5-10 jam. Selisih kecil ini tidak ditafsirkan sebagai bukti durasi optimal atau kerugian akibat belajar lebih lama.')
h('Hubungan dengan nilai sebelumnya')
p('Korelasi Pearson nilai periode kedua dengan nilai akhir adalah 0,92. Siswa dengan nilai periode kedua lebih tinggi cenderung memiliki nilai akhir lebih tinggi. Keduanya berasal dari rangkaian penilaian mata pelajaran yang sama. Angka 0,92 adalah ukuran hubungan, bukan akurasi model sebesar 92%. Scatter plot lengkap tersedia dalam notebook bersama histogram nilai dan diagram jumlah siswa.')
p('<b>Makna hasil:</b> rata-rata kelompok belajar memberi ringkasan yang berguna, tetapi ukuran kelompok dan riwayat nilai perlu dibaca bersama. Tinggi batang tidak menjelaskan hasil setiap individu dan tidak memberikan ukuran efek menambah satu jam belajar.')

story.append(PageBreak())
h('4. Pemeriksaan tambahan dan diskusi')
p('Pada sekolah GP, rata-rata kategori &lt;2 jam adalah 57,6 dan kategori 5-10 jam 67,8. Pada sekolah MS, nilainya 49,8 dan 61,5. Arah selisih tetap sama ketika sekolah dipisahkan. Namun, pemeriksaan ini belum mengendalikan perbedaan kemampuan awal, dukungan belajar, ataupun faktor lain antar siswa.')
p('Sebagai skenario tambahan, 15 nilai akhir nol dikeluarkan sehingga tersisa 634 siswa. Rata-rata kategori &lt;2 jam menjadi 56,3, sedangkan kategori 5-10 jam tetap 66,1. Pola selisih positif bertahan. Skenario ini tidak mengganti analisis utama: alasan nilai nol tidak diketahui dan menghapusnya tanpa dasar dapat menimbulkan bias.')
p('Temuan utama menunjukkan pentingnya membedakan kecenderungan kelompok dengan kepastian individu. Durasi yang lebih panjang berkaitan dengan rata-rata yang lebih tinggi pada beberapa kategori, tetapi tidak terus meningkat. Data ini tidak dapat menjelaskan mengapa rata-rata dua kategori teratas berdekatan atau apakah perbedaannya mewakili populasi yang lebih luas.')
h('5. Implikasi untuk machine learning')
p('Contoh target adalah nilai akhir; fitur dapat berupa waktu belajar, nilai periode pertama, dan nilai periode kedua jika tujuan prediksi dilakukan setelah kedua nilai itu tersedia. Untuk prediksi pada awal tahun, nilai periode sebelumnya dalam tahun yang sama belum tersedia dan harus dikeluarkan. Waktu pengumpulan kuesioner juga perlu dipastikan sesuai dengan waktu prediksi. Absensi tidak dimasukkan ke contoh fitur karena waktu rekapnya belum jelas.')
p('Korelasi tinggi antara nilai periode kedua dan nilai akhir masuk akal sebagai pola rangkaian penilaian pada mata pelajaran yang sama; ini tidak membuktikan bahwa model akan mencapai akurasi tertentu. Notebook tidak melatih model. Pengembangan berikutnya perlu menetapkan waktu prediksi, membagi data latih/uji, dan mengevaluasi kesalahan terhadap prediksi acuan sederhana.')
h('6. Keterbatasan dan kesimpulan')
p('Kajian memakai data historis dari dua sekolah dan satu mata pelajaran. Durasi merupakan kategori kuesioner, bukan pengukuran jam individual. Jumlah siswa per kelompok tidak sama, faktor pembeda belum dikendalikan, dan perbedaan kelompok tidak diuji signifikansinya. Hasil tidak digeneralisasi ke seluruh siswa atau mahasiswa Indonesia dan tidak menetapkan jam belajar ideal.')
p('<b>Kesimpulan:</b> kelompok yang belajar lebih lama cenderung memiliki rata-rata nilai lebih tinggi, tetapi durasi terpanjang bukan rata-rata tertinggi pada sampel ini. Waktu belajar memberi petunjuk, sementara penjelasan hasil individu memerlukan informasi yang lebih lengkap.')
h('Ketersediaan data dan reproduksi')
p('Repositori memuat data sumber, data enam kolom, notebook dengan output, empat grafik, pemeriksaan otomatis, dan petunjuk menjalankan ulang. Dataset dan adaptasi berlisensi CC BY 4.0, kode asli MIT. Proyek: <link href="https://github.com/feboyfierlyan/student-study-eda" color="#168278">github.com/feboyfierlyan/student-study-eda</link>.','SmallStudy')
h('Referensi')
for ref in [
    '[1] Cortez, P. (2008). <i>Student Performance</i> [Dataset]. UCI Machine Learning Repository. <link href="https://doi.org/10.24432/C5TG7T" color="#168278">doi:10.24432/C5TG7T</link>. Diakses 18 September 2026. CC BY 4.0.',
    '[2] Cortez, P., &amp; Silva, A. M. G. (2008). <i>Using Data Mining to Predict Secondary School Student Performance</i>. Studi pengantar yang ditautkan pada <link href="https://archive.ics.uci.edu/dataset/320/student+performance" color="#168278">halaman dataset UCI</link>.',
    '[3] Sigit, R. <i>Materi 04: Python dan Data Exploration untuk Machine Learning</i>. Instruksi tugas perkuliahan pada slide 22.',
]: p(ref,'RefStudy')

out=ROOT/'Belajar_dan_Nilai_Catatan_Riset.pdf'
doc=SimpleDocTemplate(str(out),pagesize=A4,leftMargin=20*mm,rightMargin=20*mm,
                     topMargin=18*mm,bottomMargin=22*mm,
                     title='Belajar Lebih Lama, Nilai Lebih Tinggi?',author='Muhammad Fierlyan Irwandi',
                     subject='EDA waktu belajar dan nilai akhir 649 siswa')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(out)
