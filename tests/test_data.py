"""Kontrol integritas dan transformasi yang memengaruhi interpretasi hasil."""
from pathlib import Path
import hashlib
import json
import sys
import unittest
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src'))
from prepare_data import prepare, LABELS

class TestStudentData(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = pd.read_csv(ROOT/'data/raw/student-por.csv', sep=';')
        cls.df = prepare(cls.raw)

    def test_source_and_rows(self):
        p = json.loads((ROOT/'data/provenance.json').read_text())
        self.assertEqual(hashlib.sha256((ROOT/'data/raw/student-por.csv').read_bytes()).hexdigest(), p['raw_sha256'])
        self.assertEqual(self.df.shape, (649, 6))
        self.assertEqual(int(self.raw.duplicated().sum()), 0)
        self.assertEqual(int(self.df.isna().sum().sum()), 0)

    def test_scaling_keeps_zeros_and_order(self):
        for src, dest in [('G1','nilai_periode1'),('G2','nilai_periode2'),('G3','nilai_akhir')]:
            pd.testing.assert_series_equal(self.df[dest]/5, self.raw[src].astype(float), check_names=False)
        self.assertEqual(int(self.df.nilai_akhir.eq(0).sum()), 15)

    def test_categories_are_not_hours(self):
        self.assertEqual(list(self.df.waktu_belajar.cat.categories), LABELS)
        self.assertEqual(self.df.waktu_belajar.value_counts(sort=False).tolist(), [212,305,97,35])
        grouped = self.df.groupby('waktu_belajar', observed=False).nilai_akhir.mean()
        self.assertAlmostEqual(grouped.iloc[2]-grouped.iloc[0], 11.912322504182, places=8)

if __name__ == '__main__':
    unittest.main()
