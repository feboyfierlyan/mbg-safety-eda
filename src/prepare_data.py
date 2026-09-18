"""Siapkan data analisis dari salinan UCI lokal; tidak memerlukan internet."""
from pathlib import Path
import hashlib
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
LABELS = ['<2 jam', '2–5 jam', '5–10 jam', '>10 jam']

def prepare(raw):
    assert raw.shape == (649, 33), 'Struktur sumber berubah; periksa ulang.'
    assert raw.isna().sum().sum() == 0
    assert set(raw.studytime.unique()) == {1, 2, 3, 4}
    for col in ['G1', 'G2', 'G3']:
        assert raw[col].between(0, 20).all()
    df = pd.DataFrame({
        'sekolah': raw.school,
        'waktu_belajar': pd.Categorical(raw.studytime.map(dict(enumerate(LABELS, 1))), categories=LABELS, ordered=True),
        'absensi': raw.absences,
        'nilai_periode1': raw.G1 * 5,
        'nilai_periode2': raw.G2 * 5,
        'nilai_akhir': raw.G3 * 5,
    })
    return df

def main():
    source = ROOT / 'data/raw/student-por.csv'
    raw = pd.read_csv(source, sep=';')
    df = prepare(raw)
    dest = ROOT / 'data/processed/data_siswa.csv'
    df.to_csv(dest, index=False)
    provenance = {
        'dataset': 'Student Performance - Portuguese language',
        'creator': 'Paulo Cortez', 'citation_year': 2008,
        'retrieved': '2026-09-18',
        'source_url': 'https://archive.ics.uci.edu/dataset/320/student+performance',
        'download_url': 'https://archive.ics.uci.edu/static/public/320/student+performance.zip',
        'doi': '10.24432/C5TG7T', 'license': 'CC BY 4.0',
        'raw_shape': list(raw.shape), 'analysis_shape': list(df.shape),
        'raw_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
        'processed_sha256': hashlib.sha256(dest.read_bytes()).hexdigest(),
        'transformations': ['Hanya student-por.csv; tidak digabung dengan matematika.',
                            'Pilih 6 kolom dan ubah nama ke Bahasa Indonesia.',
                            'G1, G2, G3 dikali 5: penskalaan aritmetis 0–20 menjadi 0–100, bukan penyetaraan kurikulum.',
                            'studytime diberi label kategori; kode 1–4 bukan jam pasti.',
                            'Semua 649 baris dan nilai nol dipertahankan. Tidak ada imputasi atau penghapusan.'],
    }
    (ROOT/'data/provenance.json').write_text(json.dumps(provenance, indent=2, ensure_ascii=False)+'\n')
    print(f'Data siap: {df.shape[0]} siswa, {df.shape[1]} kolom.')

if __name__ == '__main__':
    main()
