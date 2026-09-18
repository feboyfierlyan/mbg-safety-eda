"""Ekstraksi snapshot Wikipedia: satu blok referensi = satu entri laporan.

Jalankan dari folder repositori: python src/prepare_data.py
Tidak memerlukan internet. Nilai ambigu dipertahankan, tidak ditebak.
"""
from pathlib import Path
from collections import defaultdict
from urllib.parse import urlparse
import re
import json
import hashlib
import pandas as pd
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
REVISION = 29876794
SOURCE_URL = f'https://id.wikipedia.org/w/index.php?title=Daftar_kasus_keracunan_massal_makan_siang_gratis&oldid={REVISION}'
MONTHS = dict(zip(['Januari','Februari','Maret','April','Mei','Juni','Juli','Agustus','September','Oktober','November','Desember'], range(1,13)))

def parse_count(text):
    """Angka literal bukan bukti konfirmasi medis. Jangan imputasi kata 'ratusan'."""
    text = text.strip()
    if not text or 'TBA' in text: return None, 'tidak_tersedia'
    if any(w in text.lower() for w in ['puluhan','ratusan','belasan','ribuan']): return None, 'kualitatif'
    if '>' in text or '<' in text: return None, 'batas_bukan_angka_pasti'
    if '±' in text or 'sekitar' in text.lower(): return None, 'perkiraan'
    if re.search(r'\+\s*(guru|siswa)',text,re.I): return None, 'komponen_tidak_jelas'
    values = re.findall(r'\d+(?:[.,]\d{3})*', text)
    if not values: return None, 'tidak_tersedia'
    return sum(int(re.sub(r'[.,]','',v)) for v in values), 'angka_literal'

def parse_dates(values):
    raw = ' | '.join(values)
    clean = re.sub(r'\s+',' ',values[0]).strip()
    precision = 'tanggal' if len(values)==1 else 'beberapa_tanggal'
    day = re.fullmatch(r'(\d{1,2}) ([A-Za-z]+) (20\d{2})',clean)
    if day and day.group(2) in MONTHS:
        dt = pd.Timestamp(int(day.group(3)), MONTHS[day.group(2)], int(day.group(1)))
        return dt.date().isoformat(),dt.year,dt.month,precision
    ym = re.search(r'([A-Za-z]+) (20\d{2})',clean)
    year,month=(int(ym.group(2)),MONTHS.get(ym.group(1))) if ym else (None,None)
    return None,year,month,('rentang' if 'S/d' in raw else 'bulan' if year else 'tidak_tersedia')

def prepare():
    snapshot = ROOT / 'data/raw/wikipedia_29876794.html'
    soup = BeautifulSoup(snapshot.read_text(encoding='utf-8'), 'html.parser')
    tables = [t for t in soup.find_all('table') if 'Tanggal Kejadian' in t.get_text() and 'Bergejala' in t.get_text()]
    assert len(tables)==1
    table=tables[0]; trs=table.find_all('tr'); grid={}; cells={}
    for ri,tr in enumerate(trs):
        ci=0
        for cell in tr.find_all(['td','th'],recursive=False):
            while (ri,ci) in grid: ci+=1
            key=f'r{ri}c{ci}'
            cells[key]={'text':cell.get_text(' ',strip=True),
                        'refs':[a['href'][1:] for a in cell.select('sup.reference a[href]')]}
            for dr in range(int(cell.get('rowspan',1))):
                for dc in range(int(cell.get('colspan',1))):
                    assert (ri+dr,ci+dc) not in grid
                    grid[ri+dr,ci+dc]=key
            ci+=int(cell.get('colspan',1))
    groups=defaultdict(list); ignored=[]
    for ri in range(2,len(trs)):
        assert all((ri,c) in grid for c in range(7)), f'Lebar tabel berubah pada {ri}'
        vals=[cells[grid[ri,c]] for c in range(7)]
        if 'TOTAL' in vals[0]['text']:
            ignored.append({'row':ri,'reason':'subtotal_sumber_tidak_dipakai'});continue
        if not vals[6]['refs']:
            if not vals[4]['text']:
                ignored.append({'row':ri,'reason':'baris_lanjutan_atau_placeholder_tanpa_angka_dan_rujukan'});continue
        groups[grid[ri,6]].append(ri)
    raw=[]; records=[]
    for ref_cell, row_ids in groups.items():
        r={'entry_id':f'W{REVISION}-{ref_cell}', 'table_rows':row_ids}
        for ci,name in enumerate(['dates','province','district','places','counts','deaths','refs']):
            origins=list(dict.fromkeys(grid[ri,ci] for ri in row_ids))
            r[name]=[cells[k]['text'] for k in origins]
        ref_ids=list(dict.fromkeys(ref for ri in row_ids for ref in cells[grid[ri,6]]['refs']))
        urls=[];citations=[]
        for rid in ref_ids:
            note=soup.find(id=rid)
            if note:
                urls.extend(a['href'] for a in note.select('a.external[href]') if a['href'].startswith('http'))
                citations.append(note.get_text(' ',strip=True))
        urls=list(dict.fromkeys(urls))
        r.update(reference_ids=ref_ids,source_urls=urls,citations=citations)
        raw.append(r)
        counts=[parse_count(t) for t in r['counts']]
        number=sum(v for v,_ in counts) if all(v is not None for v,_ in counts) else None
        status='angka_literal' if number is not None else next(s for v,s in counts if v is None)
        date,year,month,precision=parse_dates(r['dates'])
        issue='';audit='belum_diperiksa_individual';source=urls[0] if urls else ''
        if not source: issue='tanpa_rujukan'
        elif urlparse(source).path in ['','/']: issue='rujukan_hanya_beranda'
        # Hasil pemeriksaan manual tersimpan di docs/AUDIT_SUMBER.md.
        if ref_cell=='r33c6': issue='rujukan_salah_lokasi';audit='rujukan_tidak_cocok'
        if ref_cell=='r427c6': issue='definisi_810_vs_444_tidak_jelas';audit='konflik_definisi_jumlah'
        if ref_cell=='r358c6': status='perkiraan_terverifikasi';audit='sekitar_800_menurut_ANTARA'
        if ref_cell=='r298c6': audit='agregat_beberapa_kejadian'
        if ref_cell in ['r434c6','r407c6','r649c6']: audit='angka_didukung_artikel_diperiksa'
        # Entri utama: angka literal, satu tanggal, rujukan artikel, tanpa konflik yang ditemukan.
        reasons=[]
        if status!='angka_literal': reasons.append(status)
        if precision!='tanggal': reasons.append('tanggal_'+precision)
        if issue: reasons.append(issue)
        if date and pd.Timestamp(date)>pd.Timestamp('2026-09-18'): reasons.append('melewati_cutoff')
        if year and year<2025: reasons.append('di_luar_periode_2025_2026')
        if date and pd.Timestamp(date)<pd.Timestamp('2025-01-06'): reasons.append('sebelum_peluncuran_nasional')
        records.append({
            'entry_id':r['entry_id'],'tanggal_raw':' | '.join(r['dates']), 'tanggal':date,
            'tahun':year,'bulan':month,'presisi_tanggal':precision,
            'provinsi':{'Nanggroe Aceh Darussalam':'Aceh','Bangka Belitung':'Kepulauan Bangka Belitung'}.get(r['province'][0],r['province'][0]),
            'kabupaten_kota':' | '.join(r['district']), 'lokasi_raw':' | '.join(r['places']),
            'jumlah_raw':' | '.join(r['counts']), 'jumlah_dilaporkan':number, 'status_angka':status,
            'jumlah_baris_html':len(row_ids),'jumlah_sel_angka':len(r['counts']),
            'source_url':source,'source_urls_json':json.dumps(urls,ensure_ascii=False),
            'masalah_rujukan':issue or None,'status_audit':audit,
            'masuk_analisis_utama':not reasons,'alasan_eksklusi':'; '.join(reasons) or None,
            'snapshot_revision':REVISION,'diakses_pada':'2026-09-18'
        })
    df=pd.DataFrame(records)
    for c in ['tahun','bulan','jumlah_dilaporkan']: df[c]=df[c].astype('Int64')
    df=df.sort_values(['tanggal','entry_id'],na_position='last').reset_index(drop=True)
    out=ROOT/'data/processed';out.mkdir(exist_ok=True,parents=True)
    df.to_csv(out/'mbg_laporan.csv',index=False)
    (ROOT/'data/raw/entries_with_sources.json').write_text(json.dumps(raw,ensure_ascii=False,indent=2),encoding='utf-8')
    (out/'baris_dikecualikan.csv').write_text(df.loc[~df.masuk_analisis_utama].to_csv(index=False),encoding='utf-8')
    (out/'ignored_html_rows.json').write_text(json.dumps(ignored,ensure_ascii=False,indent=2))
    metadata={'source_url':SOURCE_URL,'revision':REVISION,'retrieved':'2026-09-18',
              'revision_timestamp_utc':'2026-09-18T04:19:00Z',
              'html_sha256':hashlib.sha256(snapshot.read_bytes()).hexdigest(),
              'csv_sha256':hashlib.sha256((out/'mbg_laporan.csv').read_bytes()).hexdigest(),
              'html_rows_including_headers':len(trs),'entries':len(df),
              'main_analysis_entries':int(df.masuk_analisis_utama.sum()),
              'unit':'Satu blok referensi dalam tabel, bukan selalu satu kejadian epidemiologis.',
              'license':'CC BY-SA 4.0; adaptasi tabel Wikipedia dengan atribusi dan pencatatan perubahan.'}
    (ROOT/'data/provenance.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2))
    return df

if __name__=='__main__':
    data=prepare();main=data[data.masuk_analisis_utama]
    y=main.jumlah_dilaporkan.astype(float); topn=int(len(y)*.1+.999999)
    print('All / main:',len(data),len(main),'provinces',data.provinsi.nunique())
    print('Numeric status:',data.status_angka.value_counts().to_dict())
    print('Date precision:',data.presisi_tanggal.value_counts().to_dict())
    print('Dates:',main.tanggal.min(),main.tanggal.max())
    print('Mean/median/sum:',y.mean(),y.median(),y.sum())
    print('Top10%',topn,y.nlargest(topn).sum()/y.sum()*100)
    print('>=100',int((y>=100).sum()),y[y>=100].sum()/y.sum()*100)
    print('Duplicates',main.duplicated(['tanggal','provinsi','kabupaten_kota','jumlah_dilaporkan','source_url']).sum())
    print(main.nlargest(10,'jumlah_dilaporkan')[['entry_id','kabupaten_kota','jumlah_dilaporkan']].to_string(index=False))
