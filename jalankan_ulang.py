"""Jalankan semua sel dan ekspor HTML. Pakai: python jalankan_ulang.py"""
from pathlib import Path
import os
import tempfile
import re
import sys

ROOT = Path(__file__).resolve().parent
os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "eda-mbg-mpl"))
os.environ.setdefault("IPYTHONDIR", str(Path(tempfile.gettempdir()) / "eda-mbg-ipython"))

import nbformat
from nbclient import NotebookClient
from nbconvert import HTMLExporter
from jupyter_client import KernelManager

notebook_path = ROOT / "3224600051_Muhammad_Fierlyan_Irwandi_EDA.ipynb"
notebook = nbformat.read(notebook_path, as_version=4)
nbformat.validate(notebook)
manager = KernelManager(kernel_name="python3")
# Gunakan interpreter yang menjalankan skrip, termasuk ketika berada di venv.
manager.kernel_spec.argv = [sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"]
NotebookClient(notebook, timeout=180, km=manager,
               resources={"metadata": {"path": str(ROOT)}}).execute(cleanup_kc=True)
nbformat.write(notebook, notebook_path)

exporter = HTMLExporter(template_name="lab")
exporter.exclude_input_prompt = True
exporter.exclude_output_prompt = True
exporter.mathjax_url = ""
body, _ = exporter.from_notebook_node(notebook)
# Seluruh tabel dan grafik tertanam. Tak ada widget atau persamaan yang memerlukan CDN.
body = re.sub(r'<script\b[^>]*\bsrc=[^>]*>\s*</script>', '', body, flags=re.I)
body = body.replace('<title>Notebook</title>', '<title>MBG di Balik Angka Kasus — Muhammad Fierlyan Irwandi</title>')
captions = [
    'Histogram jumlah dilaporkan pada 374 entri MBG: median 32, mean 97,75 orang.',
    'Kurva konsentrasi: 38 entri terbesar memuat 47,82 persen jumlah pada subset utama.',
    'Scatter plot tanggal dan jumlah yang dilaporkan pada 2025 sampai September 2026.',
    'Delapan provinsi dengan penjumlahan angka laporan terbesar, bukan peringkat risiko.',
    'Alur kualitas data: 419 entri tersedia dan 374 masuk analisis utama.'
]
for caption in captions:
    body = body.replace('alt="No description has been provided for this image"', f'alt="{caption}"', 1)
css = '''<style>
body { background:#f4f3ef; color:#203044; }
main { max-width:1120px; margin:28px auto; padding:30px 32px; background:white; }
.jp-RenderedHTMLCommon { font-family:system-ui,-apple-system,sans-serif; line-height:1.7; }
.jp-RenderedHTMLCommon h2 { color:#953b45; margin-top:2em; padding-top:.4em; border-top:1px solid #dce6e8; }
.jp-RenderedHTMLCommon h3 { color:#243e53; }
.jp-InputArea-editor { border:1px solid #dce6e8 !important; border-radius:5px; background:#f7f9fb !important; }
.jp-OutputArea-output img { max-width:100%; height:auto; }
.dataframe { font-size:12px; }
.jp-RenderedHTMLCommon a { color:#953b45; }
@media(max-width:700px) { main { margin:0; padding:12px 6px; } }
@media print { body { background:white; } main { margin:0; padding:0; } .jp-Cell { break-inside:avoid; } }
</style>'''
body = body.replace('</head>', css + '</head>')
notebook_path.with_suffix('.html').write_text(body, encoding='utf-8')
code_cells = [cell for cell in notebook.cells if cell.cell_type == 'code']
errors = [out for cell in code_cells for out in cell.outputs if out.output_type == 'error']
image_count = sum('image/png' in out.get('data', {}) for cell in code_cells for out in cell.outputs)
assert not errors, errors
assert all(cell.execution_count is not None for cell in code_cells)
assert image_count >= 5, f'Hanya {image_count} gambar tertanam.'
print(f'OK: {len(code_cells)} sel kode dijalankan, {image_count} grafik tertanam, tanpa error.')
print('Notebook:', notebook_path.name)
print('HTML:', notebook_path.with_suffix('.html').name)
