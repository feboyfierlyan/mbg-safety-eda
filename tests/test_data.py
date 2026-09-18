"""Pemeriksaan parsing untuk mencegah angka rekaan dan penggandaan rowspan."""
import sys
import unittest
from pathlib import Path
import pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from prepare_data import parse_count, parse_dates, prepare

class DataTests(unittest.TestCase):
    def test_counts_do_not_invent_precision(self):
        self.assertEqual(parse_count('1.333 Siswa'),(1333,'angka_literal'))
        self.assertEqual(parse_count('11 Siswa + 1 Guru'),(12,'angka_literal'))
        self.assertEqual(parse_count('48 Siswa, 9 Guru dan 1 Kepala Sekolah'),(58,'angka_literal'))
        for value in ['Ratusan Siswa','>100 Siswa','± 7 siswa','77 Siswa + Guru','']:
            self.assertIsNone(parse_count(value)[0],value)

    def test_incomplete_dates_stay_incomplete(self):
        self.assertIsNone(parse_dates(['Agustus 2025'])[0])
        self.assertEqual(parse_dates(['22 September 2025','24 September 2025'])[3],'beberapa_tanggal')

    def test_snapshot_and_reference_blocks(self):
        data=prepare();self.assertEqual(len(data),419)
        self.assertEqual(data.entry_id.nunique(),419)
        self.assertEqual(int(data.masuk_analisis_utama.sum()),374)
        # 33 santri mencakup dua sekolah: tidak menjadi 66.
        row=data.set_index('entry_id').loc['W29876794-r4c6']
        self.assertEqual(row.jumlah_baris_html,2)
        self.assertEqual(row.jumlah_dilaporkan,33)
        # Angka terpisah pada tiga sekolah dijumlahkan hanya sekali.
        row=data.set_index('entry_id').loc['W29876794-r132c6']
        self.assertEqual(row.jumlah_dilaporkan,206)
        main=data[data.masuk_analisis_utama]
        self.assertTrue(main.jumlah_dilaporkan.notna().all())
        self.assertTrue((pd.to_datetime(main.tanggal)>=pd.Timestamp('2025-01-06')).all())
        self.assertFalse(main.masalah_rujukan.notna().any())
        self.assertEqual(main.jumlah_dilaporkan.sum(),36559)

if __name__=='__main__':unittest.main()
