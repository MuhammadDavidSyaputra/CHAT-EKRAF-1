from pathlib import Path
import base64
root = Path(__file__).parent
dist = root / 'veloce' / 'dist'
app = dist / 'app.js'
s = app.read_text(encoding='utf-8')
lines = s.splitlines(keepends=True)
removed = [line for line in lines if "id:'pikap'" in line]
assert len(removed) == 1
s = ''.join(line for line in lines if "id:'pikap'" not in line)
s = s.replace(",'Pikap'];", "];")
app.write_text(s, encoding='utf-8')
index = dist / 'index.html'
h = index.read_text(encoding='utf-8').replace('<span id="count">11</span>', '<span id="count">10</span>')
index.write_text(h, encoding='utf-8')
js = s.replace('assets/bmw-i8.jpg', 'data:image/jpeg;base64,' + base64.b64encode((dist/'assets/bmw-i8.jpg').read_bytes()).decode('ascii'))
html = h.replace('<link rel="stylesheet" href="style.css">', '<style>\n' + (dist/'style.css').read_text(encoding='utf-8') + '\n</style>')
html = html.replace('<script src="app.js"></script>', '<script>\n' + js + '\n</script>')
(root/'penjualan-mobil-sport.html').write_text(html, encoding='utf-8')
print('Produk pikap dan filter Pikap dihapus. File HTML diperbarui.')
