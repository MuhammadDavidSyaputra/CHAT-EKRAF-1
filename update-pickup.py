from pathlib import Path
import base64
root = Path(__file__).parent
dist = root / 'veloce' / 'dist'
p = dist / 'app.js'
s = p.read_text(encoding='utf-8')
product = """ {id:'pikap',brand:'Pikap',name:'Bak Terbuka',price:null,type:'Mobil niaga',energy:'Perlu konfirmasi',personality:'Kendaraan usaha',badge:'PRODUK BARU',description:'Mobil pikap berwarna gelap dengan bak terbuka, sesuai foto yang Anda kirim. Merek, model, tahun, spesifikasi, kondisi, dan kapasitas angkut belum dikonfirmasi. Hubungi penjual untuk informasi unit dan harga.',photos:['assets/pikap.jpg'],sources:[['Foto dari Anda',null]]},
"""
assert "id:'pikap'" not in s
s = s.replace('const cars = [\n', 'const cars = [\n' + product, 1)
s = s.replace("const money = value => new Intl", "const money = value => value == null ? 'Hubungi penjual' : new Intl")
s = s.replace("'BMW','Mercedes-Benz'];", "'BMW','Mercedes-Benz','Pikap'];")
s = s.replace("if(sort==='low')list.sort((a,b)=>a.price-b.price);if(sort==='high')list.sort((a,b)=>b.price-a.price);", "if(sort==='low')list.sort((a,b)=>(a.price??Infinity)-(b.price??Infinity));if(sort==='high')list.sort((a,b)=>(b.price??-Infinity)-(a.price??-Infinity));")
s = s.replace('▧ &nbsp; 3 foto', '▧ &nbsp; ${c.photos.length} foto')
s = s.replace('<span class="price-label">Harga simulasi</span>', '<span class="price-label">${c.price == null ? \'Harga belum tersedia\' : \'Harga simulasi\'}</span>')
s = s.replace('>1 / 3</span>', '>1 / ${car.photos.length}</span>')
s = s.replace('`${currentPhoto+1} / 3`', '`${currentPhoto+1} / ${currentCar.photos.length}`')
s = s.replace('<span class="price-label">Harga simulasi · bukan penawaran aktual</span>', '<span class="price-label">${car.price == null ? \'Harga belum tersedia · tanyakan kepada penjual\' : \'Harga simulasi · bukan penawaran aktual\'}</span>')
s = s.replace('Geser foto atau gunakan tombol panah.', '${car.photos.length > 1 ? \'Geser foto atau gunakan tombol panah.\' : \'Saat ini tersedia satu foto dari Anda.\'}')
s = s.replace("detail.querySelector('.prev').onclick=", "detail.querySelectorAll('.gallery-arrow').forEach(b=>b.hidden=car.photos.length<2);detail.querySelector('.prev').onclick=")
p.write_text(s, encoding='utf-8')
index = dist / 'index.html'
h = index.read_text(encoding='utf-8').replace('<span id="count">7</span>', '<span id="count">8</span>')
index.write_text(h, encoding='utf-8')
js = s
for name in ['bmw-i8.jpg', 'pikap.jpg']:
    encoded = base64.b64encode((dist / 'assets' / name).read_bytes()).decode('ascii')
    js = js.replace('assets/' + name, 'data:image/jpeg;base64,' + encoded)
standalone = h.replace('<link rel="stylesheet" href="style.css">', '<style>\n' + (dist / 'style.css').read_text(encoding='utf-8') + '\n</style>')
standalone = standalone.replace('<script src="app.js"></script>', '<script>\n' + js + '\n</script>')
(root / 'penjualan-mobil-sport.html').write_text(standalone, encoding='utf-8')
print('Produk pikap ditambahkan; HTML tunggal diperbarui dengan foto tertanam.')
