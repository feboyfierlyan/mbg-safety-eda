"""Bangun notebook pengumpulan dari dataset yang telah dikurasi."""
from pathlib import Path
import json,textwrap,hashlib
import nbformat as nbf
import pandas as pd
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
STEM='3224600051_Muhammad_Fierlyan_Irwandi_EDA'
df=pd.read_csv(ROOT/'data/processed/mbg_laporan.csv')
a=df[df.masuk_analisis_utama];y=a.jumlah_dilaporkan
n=len(a);k=int(np.ceil(.1*n));share=y.nlargest(k).sum()/y.sum()*100
sha=hashlib.sha256((ROOT/'data/processed/mbg_laporan.csv').read_bytes()).hexdigest()
cells=[]
def md(s):cells.append(nbf.v4.new_markdown_cell(textwrap.dedent(s).strip()))
def code(s):cells.append(nbf.v4.new_code_cell(textwrap.dedent(s).strip()))

md(f'''
<div style="border-top:5px solid #953b45;padding:28px;background:#f8f5f1;color:#172b3a">
<p style="font-size:12px;letter-spacing:2px">CATATAN RISET EKSPLORATIF · MATERI 04</p>
<h1 style="font-size:32px;line-height:1.2">MBG di Balik Angka Kasus</h1>
<p style="font-size:20px">Mengapa menghitung laporan saja tidak cukup?</p>
<p><b>Muhammad Fierlyan Irwandi · 3224600051</b><br>Pengantar Kecerdasan Artifisial dan Pembelajaran Mesin<br>Teknik Komputer · Politeknik Elektronika Negeri Surabaya</p>
<p>Snapshot data: 18 September 2026 · Versi kajian 2.0</p>
</div>

## Abstrak

Kajian ini mengeksplorasi laporan publik dugaan maupun kejadian keracunan yang dikaitkan dengan program Makan Bergizi Gratis (MBG). Sebanyak **419 entri** diekstraksi dari tabel Wikipedia versi tetap, kemudian dikurasi menjadi **374 entri analisis utama**. Unit observasi adalah blok laporan dalam tabel, bukan orang unik atau kejadian epidemiologis yang telah dideduplikasi. Median jumlah yang dilaporkan adalah **32 orang**, sedangkan rata-ratanya **97,75 orang**. Sebanyak **38 entri terbesar (10,16%) memuat 47,82%** dari penjumlahan angka pada subset utama. Pemeriksaan kepekaan menunjukkan pola konsentrasi tetap muncul setelah lima entri terbesar dikeluarkan. Temuan ini mendukung pelaporan frekuensi bersama skala dampak, tetapi tidak mengukur risiko keracunan per porsi maupun keberhasilan program secara keseluruhan.

**Kata kunci:** MBG, EDA, keamanan pangan, kualitas data, konsentrasi laporan.

**Status:** tugas perkuliahan berbentuk catatan riset eksploratif; belum ditelaah sejawat. Notebook ini tidak menyatakan seluruh laporan telah dikonfirmasi secara medis.

**Menjalankan:** unduh paket repositori agar `data/` tersedia, buka notebook dari folder utama, lalu pilih **Restart Kernel and Run All Cells**. Semua output sudah tersimpan. Tidak diperlukan internet untuk menjalankan ulang dengan data lokal.
''')
md('''
## 1. Pendahuluan dan pertanyaan penelitian

MBG dekat dengan kehidupan siswa dan menjadi perdebatan publik ketika muncul laporan gangguan kesehatan. Pertanyaan kajian ini sederhana: **apakah jumlah laporan saja cukup untuk menggambarkan besarnya dampak yang dilaporkan?**

Konteks mutakhir: pada 15 September 2026, BGN menyatakan sedang menyiapkan aplikasi penilaian layanan MBG oleh kepala sekolah [2]. Isu transparansi dan kualitas pelaporan karena itu relevan untuk dianalisis. Pernyataan kebijakan tersebut hanya menjadi konteks, bukan variabel kausal dalam dataset.

Pertanyaan EDA:
1. Berapa banyak entri yang dapat dianalisis setelah pemeriksaan kualitas?
2. Seperti apa distribusi jumlah orang yang dilaporkan per entri?
3. Apakah sebagian kecil entri memuat sebagian besar jumlah yang dilaporkan?
4. Bagaimana sebaran laporan menurut waktu dan provinsi dalam daftar yang tersedia?
5. Apa konsekuensinya untuk pemilihan fitur, target, dan pengumpulan data berikutnya?
''')
md('''
## 2. Data dan metode

### 2.1 Sumber dan unit observasi

Data bersumber dari tabel bagian MBG pada [Wikipedia, revisi 29876794](https://id.wikipedia.org/w/index.php?title=Daftar_kasus_keracunan_massal_makan_siang_gratis&oldid=29876794), diperbarui 18 September 2026 pukul 04.19 UTC dan diakses pada hari yang sama. Tabel mengumpulkan rujukan pemberitaan; ini **sumber sekunder yang tidak lengkap**, bukan registri resmi BGN/BPOM. Tautan sumber per entri, snapshot HTML, dan teks sel asli tersedia dalam repositori.

Satu baris dataset = **satu blok referensi pada tabel sumber**. Angka bersama untuk beberapa sekolah dihitung sekali. Angka terpisah untuk kelompok yang dicatat terpisah dalam blok dijumlahkan. Blok dengan beberapa tanggal tidak dimasukkan dalam analisis utama. Satu entri belum tentu satu insiden, dan beberapa entri masih mungkin merujuk kejadian yang berhubungan.

### 2.2 Kurasi yang dapat diperiksa

- Tabel mempunyai 825 baris HTML termasuk dua header. Parser menghasilkan 419 entri, bukan 823 kejadian.
- Lima baris berupa subtotal, placeholder, atau kelanjutan tanpa angka/rujukan dikeluarkan dari ekstraksi.
- Kata seperti “ratusan”, “puluhan”, batas `>100`, dan komponen tidak jelas tidak diubah menjadi angka pasti.
- Tanggal yang hanya menyebut bulan tetap tidak memiliki tanggal harian; tidak diisi tanggal 1 secara otomatis.
- Analisis utama mensyaratkan angka literal, satu tanggal dalam 6 Januari 2025–18 September 2026, URL artikel yang spesifik, dan tidak ada konflik sumber yang ditemukan.
- Sebanyak 45 entri tetap disimpan untuk audit, tetapi tidak masuk subset utama.

“Angka literal” berarti bentuk angka pada sumber dapat dibaca, **bukan** status terkonfirmasi. Audit manual terarah memeriksa beberapa entri besar dan rujukan bermasalah; sebagian besar sumber belum diperiksa satu per satu. Detail keputusan: `docs/AUDIT_SUMBER.md`.
''')
code('''
from pathlib import Path
import hashlib
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from IPython.display import display, Markdown

pd.set_option("display.max_columns", 24)
pd.set_option("display.max_colwidth", 75)
pd.set_option("display.precision", 3)
plt.rcParams.update({"font.family":"DejaVu Sans", "figure.dpi":110,
                     "savefig.dpi":180, "axes.spines.top":False,
                     "axes.spines.right":False, "axes.titleweight":"bold",
                     "axes.labelcolor":"#25364a", "text.color":"#25364a"})
INK, RED, BLUE, GREY = "#25364a", "#953b45", "#376882", "#87949e"
FIG=Path("figures");FIG.mkdir(exist_ok=True)

def selesai(fig, filename, n_data, catatan=""):
    fig.text(0.01,0.01,f"Sumber: tabel Wikipedia rev. 29876794 + kurasi | snapshot 18 Sep 2026 | n={n_data} entri\\n{catatan}",
             fontsize=8,color="#5b6470")
    fig.tight_layout(rect=(0,.065,1,1))
    fig.savefig(FIG/filename,bbox_inches="tight",facecolor="white")
    plt.show();plt.close(fig)
''')
code(f'''
DATA=Path("data/processed/mbg_laporan.csv")
assert DATA.exists(), "Unduh ZIP repositori agar CSV dan notebook berada dalam satu folder proyek."
assert hashlib.sha256(DATA.read_bytes()).hexdigest()=="{sha}", "Versi CSV berubah; bangun ulang kajian."
df=pd.read_csv(DATA,parse_dates=["tanggal"])
utama=df.loc[df["masuk_analisis_utama"]].copy()
utama["jumlah_dilaporkan"]=utama["jumlah_dilaporkan"].astype(int)
y=utama["jumlah_dilaporkan"]
print("Snapshot: 18 September 2026 | revisi 29876794")
print("Entri tersedia:",len(df),"| analisis utama:",len(utama),"| dikeluarkan:",len(df)-len(utama))
''')
md('''
## 3. Inspeksi awal dataset
### 3.1 `head()` dan `shape`

Kolom lengkap tetap disimpan. Untuk keterbacaan, pratinjau menampilkan variabel utama serta alasan kurasi. Tanggal 2024 yang muncul dalam sumber sengaja dipertahankan dalam tabel audit dan dikeluarkan dari analisis periode kajian.
''')
code('''
kolom_tampil=["entry_id","tanggal","provinsi","kabupaten_kota","jumlah_raw",
               "jumlah_dilaporkan","status_angka","masuk_analisis_utama"]
display(df[kolom_tampil].head())
print("Shape dataset penuh:",df.shape)
print("Shape subset utama:",utama.shape)
print("Provinsi tercantum:",df["provinsi"].nunique())
''')
md('''
**Interpretasi:** 419 entri melampaui syarat tugas minimal 100 baris. Sebanyak 35 provinsi tercantum pada daftar, tetapi tidak adanya entri di provinsi lain tidak membuktikan tidak ada kejadian. Jumlah kolom mencakup identitas, sumber, dan penanda kualitas; semuanya tidak otomatis merupakan fitur model.

### 3.2 `info()` dan `describe()`
''')
code('''
df.info()
display(utama[["jumlah_dilaporkan","tahun","bulan"]].describe().T)
display(df[["provinsi","status_angka","presisi_tanggal"]].describe(include="all").T)
''')
md('''
**Interpretasi:** target numerik memiliki rentang lebar, sehingga rata-rata perlu dibaca bersama median. Tahun dan bulan adalah penanda waktu; mean tahun bukan hasil substantif. Nilai kosong pada jumlah dan tanggal berasal dari keterbatasan pelaporan, sehingga tidak diimputasi dengan nol maupun mean.

### 3.3 Missing value, duplikasi, dan kualitas
''')
code('''
cek=["tanggal","jumlah_dilaporkan","source_url","provinsi","kabupaten_kota"]
display(pd.DataFrame({"missing":df[cek].isna().sum(),"persen":df[cek].isna().mean()*100}))
print("Duplikasi entry_id:",int(df["entry_id"].duplicated().sum()))
kunci=["tanggal","provinsi","kabupaten_kota","jumlah_dilaporkan","source_url"]
print("Duplikasi pada kunci peninjauan, subset utama:",int(utama.duplicated(kunci).sum()))
display(df["status_angka"].value_counts().rename_axis("status_angka").to_frame("entri"))
display(df.loc[~df["masuk_analisis_utama"],
    ["entry_id","tanggal_raw","kabupaten_kota","jumlah_raw","alasan_eksklusi"]].head(10))
''')
md('''
**Interpretasi:** 28 entri tidak memiliki nilai jumlah yang dapat dijadikan angka tunggal dan tujuh tidak memiliki tanggal harian. Tidak ada ID ganda atau duplikasi pada kunci pemeriksaan subset utama. Namun, nol duplikasi teknis tidak menjamin nol tumpang tindih kejadian di dunia nyata. `Masalah_rujukan` dan `alasan_eksklusi` yang kosong berarti tidak diberi penanda tersebut, bukan data hilang yang perlu diimputasi.

Audit menemukan contoh penting: entri 1.333 di Bandung Barat mencakup beberapa kejadian [3], dan entri Padang Panjang memiliki rujukan yang menunjuk Lampung Utara. Keduanya tidak masuk subset utama. Sel kosong pada kolom meninggal di tabel sumber tidak dianggap nol; kajian ini tidak menghitung kematian.
''')
md('''
## 4. Hasil dan visualisasi
### Gambar 1. Mayoritas entri kecil, tetapi ekornya panjang
**Pertanyaan:** mengapa rata-rata dan median berbeda jauh?
''')
code('''
fig,ax=plt.subplots(figsize=(9,4.8))
ax.hist(y,bins=np.arange(0,851,25),color=BLUE,edgecolor="white")
ax.axvline(y.median(),color=INK,ls="--",lw=2,label=f"Median: {y.median():.0f} orang")
ax.axvline(y.mean(),color=RED,lw=2,label=f"Rata-rata: {y.mean():.2f} orang")
ax.set(title="Median 32; rata-rata hampir 98 orang per entri",
       xlabel="Jumlah orang yang dilaporkan per entri",ylabel="Frekuensi (entri)")
ax.legend(frameon=False)
selesai(fig,"01_distribusi.png",len(utama),"Lebar bin 25 orang. Angka laporan; bukan ukuran risiko per porsi.")
display(y.agg(["count","mean","median","min","max"]).to_frame("nilai"))
''')
md('''
**Interpretasi:** median 32 berarti separuh entri bernilai paling banyak 32 orang. Rata-rata 97,75 lebih dari tiga kali median karena beberapa laporan berangka besar menarik mean ke kanan. Skala entri yang tidak seragam turut memengaruhi perbedaan ini. Untuk target yang miring, median dan MAE layak menjadi pembanding jika pemodelan kelak dilakukan. Nilai besar tidak otomatis dibuang sebagai kesalahan.

### Gambar 2. Sebagian kecil entri memuat hampir separuh jumlah
**Pertanyaan:** berapa besar konsentrasi angka yang dilaporkan?
''')
code('''
urut=y.sort_values(ascending=False).reset_index(drop=True)
k=int(np.ceil(.10*len(urut)))
x_pct=np.arange(1,len(urut)+1)/len(urut)*100
y_pct=urut.cumsum()/urut.sum()*100
share_top=float(y_pct.iloc[k-1])
fig,ax=plt.subplots(figsize=(9,5))
ax.plot(np.r_[0,x_pct],np.r_[0,y_pct],color=RED,lw=2.8)
ax.plot([0,100],[0,100],color=GREY,ls="--",label="Acuan jika semua entri sama besar")
ax.scatter([x_pct[k-1]],[share_top],s=70,color=INK,zorder=5)
ax.annotate(f"{k} entri ({x_pct[k-1]:.2f}%)\\nmemuat {share_top:.2f}% jumlah",
            (x_pct[k-1],share_top),xytext=(30,30),textcoords="offset points",
            fontsize=12,color=INK,arrowprops={"arrowstyle":"-","color":INK})
ax.set(xlim=(0,100),ylim=(0,103),title="Sekitar 10% entri memuat hampir 48% jumlah yang dilaporkan",
       xlabel="Porsi entri, diurutkan dari angka terbesar (%)",
       ylabel="Porsi kumulatif jumlah yang dilaporkan (%)")
ax.legend(frameon=False,loc="lower right")
selesai(fig,"02_konsentrasi.png",len(utama),"Denominator: penjumlahan angka pada 374 entri, bukan total nasional orang unik.")
print(f"{k}/{len(urut)} entri = {x_pct[k-1]:.2f}% | bagian jumlah = {share_top:.2f}%")
''')
md('''
**Interpretasi:** 38 dari 374 entri memuat 47,82% dari jumlah yang dijumlahkan pada subset ini. Angka 38 merupakan pembulatan ke atas dari 10% ukuran sampel. Penghitungan satu entri sebagai satu laporan memberi bobot yang sama, padahal besaran angka yang dilaporkan sangat berbeda. Temuan ini mendukung penyajian jumlah laporan **bersama** jumlah orang per laporan. Ini bukan klaim bahwa 10% dapur menyebabkan 48% kasus nasional.

### Gambar 3. Laporan besar muncul pada berbagai waktu
**Pertanyaan:** apakah angka besar hanya tampak pada satu periode?
''')
code('''
fig,ax=plt.subplots(figsize=(10,4.8))
for yr,color in [(2025,BLUE),(2026,RED)]:
    z=utama[utama["tahun"].eq(yr)]
    ax.scatter(z["tanggal"],z["jumlah_dilaporkan"],s=23,alpha=.65,color=color,label=str(yr))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%Y"))
ax.set(title="Sebaran waktu memperlihatkan variasi skala laporan",
       xlabel="Tanggal yang tercantum pada laporan (bulan/tahun)",
       ylabel="Jumlah orang yang dilaporkan per entri")
ax.legend(title="Tahun",frameon=False)
selesai(fig,"03_waktu.png",len(utama),"Cakupan entri utama: 13 Jan 2025–16 Sep 2026. Cakupan pelaporan antarwaktu tidak seragam.")
''')
md('''
**Interpretasi:** laporan berangka besar muncul di 2025 dan 2026. Grafik ini memetakan entri yang tersedia, bukan laju insiden. Perubahan jumlah porsi, perluasan program, libur sekolah, perhatian media, dan keterlambatan pencatatan tidak dikendalikan. Karena 2026 hanya sampai September, membandingkan total dua tahun sebagai persentase kenaikan risiko akan menyesatkan.

### Gambar 4. Lokasi laporan tidak sama dengan peringkat risiko
**Pertanyaan:** di mana jumlah pada entri yang tersedia terkonsentrasi?
''')
code('''
prov=utama.groupby("provinsi")["jumlah_dilaporkan"].agg(jumlah="sum",entri="size")
top=prov.nlargest(8,"jumlah").sort_values("jumlah")
fig,ax=plt.subplots(figsize=(10,5.2))
bars=ax.barh(top.index,top["jumlah"],color=BLUE)
ax.bar_label(bars,labels=[f"{int(row.jumlah):,} · {int(row.entri)} entri" for row in top.itertuples()],padding=6,fontsize=10)
ax.set_xlim(0,top["jumlah"].max()*1.30)
ax.set(title="Delapan provinsi dengan penjumlahan angka laporan terbesar dalam subset",
       xlabel="Penjumlahan jumlah yang dilaporkan (orang; belum dideduplikasi antarentri)",
       ylabel="Provinsi pada entri")
selesai(fig,"04_provinsi.png",len(utama),"Bukan peringkat keamanan: jumlah porsi/penerima per provinsi tidak tersedia.")
display(top.sort_values("jumlah",ascending=False))
''')
md('''
**Interpretasi:** Jawa Tengah memiliki penjumlahan angka tertinggi pada subset yang tersedia, diikuti Jawa Timur dan Jawa Barat. Ini dapat dipengaruhi skala program maupun cakupan media. Tanpa jumlah porsi yang dibagikan pada periode dan wilayah yang sama, provinsi tersebut tidak dapat dinyatakan lebih berisiko. Label jumlah entri disertakan agar pembaca tidak mencampur jumlah laporan dan jumlah orang.

### Gambar 5. Apa yang disisihkan sebelum menarik kesimpulan?
**Pertanyaan:** berapa entri yang tidak lolos aturan analisis utama?
''')
code('''
# Tahap bersifat berurutan dan saling eksklusif, sehingga tidak menghitung entri dua kali.
alasan=np.select([
    df["status_angka"].ne("angka_literal"),
    df["presisi_tanggal"].ne("tanggal"),
    df["masalah_rujukan"].notna(),
    ~df["masuk_analisis_utama"]
], ["Angka tidak pasti / kosong","Tanggal tidak tunggal / tidak lengkap",
    "Rujukan atau definisi bermasalah","Di luar periode kajian"],default="Masuk analisis utama")
alur=pd.Series(alasan).value_counts()
fig,ax=plt.subplots(figsize=(10,4.7))
bars=ax.barh(alur.index[::-1],alur.values[::-1],
             color=[BLUE if t=="Masuk analisis utama" else RED for t in alur.index[::-1]])
ax.bar_label(bars,padding=6)
ax.set_xlim(0,alur.max()*1.12)
ax.set(title="419 entri tersedia; 374 lolos aturan analisis utama",
       xlabel="Jumlah entri (kategori eksklusif)",ylabel="Hasil kurasi berurutan")
selesai(fig,"05_kualitas_data.png",len(df),"Eksklusi bukan berarti laporan palsu; detail tetap disimpan untuk audit.")
display(alur.to_frame("entri"))
''')
md('''
**Interpretasi:** 45 entri (10,74%) tidak masuk statistik utama. Menyimpan alasan eksklusi membuat keputusan analisis dapat ditinjau. Menganggap kata “ratusan” sebagai 100, atau nilai kosong sebagai nol, akan menciptakan ketepatan yang tidak diberikan sumber.
''')
md('''
## 5. Uji kepekaan, bukan pembuktian kausal

Dua pembanding digunakan: mengeluarkan lima entri terbesar dari subset utama, serta memasukkan seluruh angka literal bertahun 2025–2026 meskipun aturan sumber/tanggal dilonggarkan. Skenario longgar sengaja memuat entri bermasalah untuk mengukur perubahan hasil, bukan untuk diutamakan.
''')
code('''
def ringkas(s):
    s=s.dropna();kk=int(np.ceil(.1*len(s)))
    return {"n":len(s),"median":s.median(),"mean":s.mean(),
            "top_n":kk,"porsi_top_persen":s.nlargest(kk).sum()/s.sum()*100}
longgar=df.loc[df["status_angka"].eq("angka_literal") & df["tahun"].ge(2025),"jumlah_dilaporkan"]
sens=pd.DataFrame({
    "Utama":ringkas(y),
    "Tanpa 5 terbesar":ringkas(y.sort_values().iloc[:-5]),
    "Semua angka literal 2025–2026":ringkas(longgar)
}).T
display(sens.round(2))
sens.to_csv("data/processed/sensitivitas.csv",index_label="skenario")
''')
md('''
**Interpretasi:** porsi sekitar 10% entri terbesar adalah 47,82% pada analisis utama, 44,82% setelah lima terbesar dibuang, dan 48,37% pada skenario longgar. Konsentrasi tetap tampak. Ini adalah rentang hasil skenario, **bukan interval kepercayaan**. Bias pelaporan dan tumpang tindih kejadian tetap belum terselesaikan.

## 6. Fitur dan target untuk konteks pembelajaran mesin

Untuk memenuhi tugas, masalah supervisi hipotetisnya adalah memperkirakan **besar angka yang akan tercatat pada suatu entri laporan** dari konteks wilayah dan waktu. Ini bukan sistem untuk memprediksi apakah sebuah makanan aman.

- **Fitur X:** `provinsi` (kategorikal), `tahun` dan `bulan` (penanda waktu). Fitur ini sangat terbatas dan mungkin menangkap pola pelaporan, bukan mekanisme keamanan pangan.
- **Target y:** `jumlah_dilaporkan`, bilangan orang yang dicatat pada entri terpilih. Target berbentuk count, sehingga konteksnya regresi.
- **Dilarang sebagai fitur:** `jumlah_raw`, kelas besar/kecil yang diturunkan dari y, urutan setelah pengurutan y, dan jumlah kematian. Itu berpotensi membocorkan target atau baru tersedia setelah kejadian.
- **Bukan fitur:** ID, URL sumber, dan penanda kurasi. Tujuannya audit, bukan memberikan makna prediktif.
''')
code('''
X=utama[["provinsi","tahun","bulan"]].copy()
y_model=utama["jumlah_dilaporkan"].copy()
print("X:",X.shape,"| y:",y_model.shape)
display(X.head())
assert len(X)==len(y_model)>=100
assert "jumlah_dilaporkan" not in X.columns
assert not X.isna().any().any()
''')
md('''
**Implikasi:** kategori provinsi perlu encoding. Split harus mempertimbangkan urutan waktu dan pengelompokan kejadian yang sama, lalu preprocessing dipelajari hanya pada data latih. Jangan random split begitu saja ketika beberapa laporan bisa merujuk kejadian terkait. Dataset ini belum memiliki ID kejadian yang andal, sehingga belum layak menjadi sistem prediksi operasional. Model sengaja tidak dilatih karena tugas berfokus pada EDA.

Data tambahan yang dibutuhkan untuk kajian risiko: jumlah porsi per dapur per hari, ID kejadian dan dapur, definisi kasus yang seragam, serta hasil konfirmasi dan pembaruan jumlah. Data operasional harus tersedia sebelum outcome jika kelak dipakai sebagai prediktor.

## 7. Lima insight singkat

1. **Kualitas data mengubah sampel:** dari 419 entri tersedia, 374 lolos aturan analisis dan 45 disimpan sebagai catatan audit.
2. **Mean bukan gambaran laporan tipikal:** median 32 orang jauh di bawah rata-rata 97,75 karena distribusi miring ke kanan.
3. **Angka terkonsentrasi:** 38 entri terbesar (10,16%) memuat 47,82% penjumlahan jumlah yang dilaporkan dalam subset utama.
4. **Laporan besar mendominasi penjumlahan:** 115 entri bernilai setidaknya 100 orang (30,75%) memuat 81,17% jumlah dalam subset ini.
5. **Pola tidak bergantung hanya pada lima terbesar:** setelah kelimanya dikeluarkan, sekitar 10% entri terbesar yang tersisa masih memuat 44,82% jumlah.
''')
code('''
besar=y.ge(100)
print(f"Entri >=100: {besar.sum()} ({besar.mean():.2%})")
print(f"Bagian jumlah pada entri >=100: {y[besar].sum()/y.sum():.2%}")
''')
md('''
## 8. Diskusi, keterbatasan, dan kesimpulan

**Pesan utama:** pelaporan keamanan program perlu menunjukkan frekuensi **dan** skala dampak. Dua entri sama-sama bernilai satu dalam hitungan laporan, tetapi dapat melibatkan jumlah orang yang jauh berbeda. Median, mean, dan distribusi membantu menghindari penyederhanaan itu.

Lima batas pembacaan hasil:
1. Daftar tidak lengkap dan dipengaruhi seleksi pemberitaan; sampel tidak acak.
2. Satu entri bukan selalu satu kejadian. Deduplikasi kejadian/orang antarentri belum tersedia.
3. Dugaan dan konfirmasi belum dapat dipisahkan secara konsisten. Angka dapat berubah setelah sumber diperbarui.
4. Tidak ada denominator porsi atau penerima untuk periode/wilayah yang sesuai; risiko per porsi tidak dapat dihitung.
5. Tidak ada kelompok pembanding tanpa MBG dan tidak ada rancangan kausal; manfaat, kerugian bersih, serta penyebab program tidak diestimasi.

Kesimpulannya, subset terpilih memperlihatkan konsentrasi besaran laporan yang kuat. EDA ini memberi alasan untuk menampilkan skala dampak bersama jumlah laporan serta memperbaiki struktur data publik. Kajian tidak menetapkan provinsi paling berbahaya atau memutuskan keberhasilan/kegagalan MBG secara keseluruhan.

## 9. Pemeriksaan instruksi tugas

- [x] Dataset tabular minimal 100 baris: 419 entri, 374 pada analisis utama.
- [x] `head()`, `shape`, `info()`, dan `describe()` beserta interpretasi.
- [x] Minimal tiga visualisasi: lima grafik dengan label dan sumber.
- [x] Identifikasi fitur X dan target y serta risiko kebocoran target.
- [x] Lima insight singkat berbasis hasil hitungan.
- [x] Nama file sesuai NIM dan nama mahasiswa.
- [x] Naskah presentasi sekitar 2–2,5 menit ada pada `PRESENTASI_SINGKAT.md`.

## Referensi

[1] Kontributor Wikipedia. *Daftar kasus keracunan massal makan siang gratis*, bagian MBG. [Revisi 29876794](https://id.wikipedia.org/w/index.php?title=Daftar_kasus_keracunan_massal_makan_siang_gratis&oldid=29876794), 18 September 2026. Adaptasi berlisensi CC BY-SA 4.0. Tautan artikel per entri tersimpan pada CSV/JSON sumber.

[2] Badan Gizi Nasional. [BGN Siapkan Aplikasi Rating MBG, Sekolah Diminta Tak Segan Laporkan SPPG Bermasalah](https://www.bgn.go.id/news/siaran-pers/bgn-siapkan-aplikasi-rating-mbg-sekolah-diminta-tak-segan-laporkan-sppg-bermasalah), 15 September 2026. Konteks kebijakan, tidak dimasukkan ke perhitungan.

[3] Kompas.com. [Update Korban Keracunan MBG di Bandung Barat Tembus 1.333 Orang](https://bandung.kompas.com/read/2025/09/25/165121378/update-korban-keracunan-mbg-di-bandung-barat-tembus-1333-orang), 25 September 2025. Digunakan untuk audit agregasi.

[4] Badan Gizi Nasional. [BGN akan Memulai Program MBG Secara Bertahap](https://www.bgn.go.id/news/artikel/bgn-akan-memulai-program-mbg-secara-bertahap), 5 Januari 2025. Menyebut peluncuran nasional pada 6 Januari 2025.

[5] Sigit, R. *Materi 04: Python dan Data Exploration untuk Machine Learning*. Materi kuliah PENS yang diberikan pengguna, khususnya slide 12–17, 20, dan 22.

Seluruh tanggal akses sumber daring: 18 September 2026. Catatan pemeriksaan tambahan dan keterbatasan verifikasi ada pada `docs/AUDIT_SUMBER.md`.
''')
code('''
hasil={"entri_total":len(df),"entri_utama":len(utama),"entri_dikeluarkan":len(df)-len(utama),
       "median":float(y.median()),"mean":float(y.mean()),"jumlah_dalam_subset":int(y.sum()),
       "top_n":k,"top_n_persen":float(k/len(y)*100),"top_share_persen":share_top,
       "entri_min_100":int(besar.sum()),"entri_min_100_persen":float(besar.mean()*100),
       "share_min_100_persen":float(y[besar].sum()/y.sum()*100),
       "tanggal_min":str(utama.tanggal.min().date()),"tanggal_max":str(utama.tanggal.max().date()),
       "catatan":"Statistik entri laporan terpilih; bukan estimasi nasional korban unik atau risiko."}
Path("data/processed/hasil_ringkas.json").write_text(json.dumps(hasil,indent=2,ensure_ascii=False),encoding="utf-8")
print("Selesai. Lima grafik dan seluruh hasil analisis tersimpan.")
''')
nb=nbf.v4.new_notebook(cells=cells)
nb.metadata={'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},
             'language_info':{'name':'python'},'authors':[{'name':'Muhammad Fierlyan Irwandi'}]}
nbf.write(nb,ROOT/f'{STEM}.ipynb')
print(f'Notebook dibuat: {len(cells)} sel; {sum(c.cell_type=="code" for c in cells)} sel kode.')
