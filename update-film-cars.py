from pathlib import Path
import json, base64
root = Path(__file__).parent
dist = root / 'veloce' / 'dist'
items = [
 dict(id='eclipse-1995',brand='Mitsubishi',name='Eclipse 1995 · Hijau',price=650000000,type='Sport coupé',energy='Bensin',personality='Neon green statement',badge='MOVIE INSPIRED',description='Mitsubishi Eclipse 1995 dengan inspirasi tampilan hijau khas The Fast and the Furious. Katalog ini menampilkan referensi gaya film, bukan klaim penjualan mobil asli yang dipakai dalam produksi. Tahun, modifikasi, kondisi, dan legalitas unit aktual perlu dikonfirmasi kepada penjual.',photos=[
 'https://res.cloudinary.com/mecum/image/upload/v1659679361/auctions/fl22/fl0122-487286/1666320_27.jpg',
 'https://hagerty-media-prod.imgix.net/2022/01/TFATF-Mitsubishi-Eclipse.png?auto=format%2Ccompress&ixlib=php-3.3.0',
 'https://media.loom-app.com/bi/dist/images/2021/04/21/58eec93385086820008b4df6.jpg?w=1200'],sources=[
 ['Mecum Auctions','https://www.mecum.com/lots/487286/1995-mitsubishi-eclipse/'],
 ['Hagerty','https://www.hagerty.com/media/news/this-mitsubishi-eclipse-sold-fast-for-a-furious-170500/'],
 ['Business Insider Japan','https://www.businessinsider.jp/article/233563/']]),
 dict(id='supra-a80',brand='Toyota',name='Supra A80 · Oranye',price=2800000000,type='Sport coupé',energy='Bensin',personality='Orange street icon',badge='MOVIE INSPIRED',description='Toyota Supra A80 dengan inspirasi warna oranye dan grafis ikonik dari film pertama The Fast and the Furious. Ditampilkan sebagai konsep koleksi terinspirasi film. Foto bukan bukti ketersediaan unit atau keaslian kendaraan produksi film. Konfirmasi detail unit bersama penjual.',photos=[
 'https://www.topgear.com/sites/default/files/news-listicle/image/supraff_0.jpg',
 'https://i.blogs.es/327b54/mj/1366_2000.jpg',
 'https://matome.response.jp/uploads/content/image/234397/1645246.jpg'],sources=[
 ['Top Gear','https://www.topgear.com/car-news/retro/eight-reasons-why-old-toyota-supra-was-so-cool'],
 ['Motorpasión México','https://www.motorpasion.com.mx/industria/toyota-supra-fast-and-furious-a-subasta'],
 ['Response','https://matome.response.jp/articles/5615']]),
 dict(id='skyline-r34',brand='Nissan',name='Skyline GT-R R34',price=4500000000,type='Sport coupé',energy='Bensin',personality='Silver and blue legend',badge='MOVIE INSPIRED',description='Nissan Skyline GT-R R34 dengan inspirasi tampilan perak dan biru dari 2 Fast 2 Furious. Karakter visual yang kuat untuk penggemar kultur otomotif Jepang. Koleksi ini merupakan referensi bergaya film; unit, spesifikasi, modifikasi, dan harga aktual perlu dikonfirmasi.',photos=[
 'https://petersen.org/cdn/shop/files/Add_Images_to_New_Pages_5000_x_3000_px.png?v=1782836948&width=1200',
 'https://acnews.blob.core.windows.net/imggallery/1024x768/GAZ_15226448ed004208aadf4a861989eaec.jpg',
 'https://images.everyeye.it/img-notizie/la-skyline-paul-walker-2-fast-2-furious-rispunta-all-improvviso-18-anni-v3-866143.jpg'],sources=[
 ['Petersen Automotive Museum','https://petersen.org/pages/petersen-exhibit/a-fast-furious-legacy-25-years-of-automotive-icons'],
 ['Autocosmos','https://galerias.autocosmos.com.pe/2013/05/17/top-10-rapido-y-furioso-nissan-skyline-gtr-r34'],
 ['Everyeye','https://auto.everyeye.it/notizie/skyline-paul-walker-2-fast-2-furious-rispunta-improvviso-18-anni-866143.html']])
]
p = dist / 'app.js'
s = p.read_text(encoding='utf-8')
assert all(item['id'] not in s for item in items)
data = ',\n'.join(json.dumps(item, ensure_ascii=False, separators=(',', ':')) for item in items)
s = s.replace('const cars = [\n', 'const cars = [\n' + data + ',\n', 1)
s = s.replace("'Mercedes-Benz','Pikap'];", "'Mercedes-Benz','Mitsubishi','Pikap'];")
s = s.replace("${b==='Toyota'?'Toyota Supra':b}", "${b}")
p.write_text(s, encoding='utf-8')
index = dist / 'index.html'
h = index.read_text(encoding='utf-8').replace('<span id="count">8</span>', '<span id="count">11</span>')
index.write_text(h, encoding='utf-8')
js = s
for name in ['bmw-i8.jpg', 'pikap.jpg']:
    js = js.replace('assets/' + name, 'data:image/jpeg;base64,' + base64.b64encode((dist/'assets'/name).read_bytes()).decode('ascii'))
html = h.replace('<link rel="stylesheet" href="style.css">', '<style>\n' + (dist/'style.css').read_text(encoding='utf-8') + '\n</style>')
html = html.replace('<script src="app.js"></script>', '<script>\n' + js + '\n</script>')
(root/'penjualan-mobil-sport.html').write_text(html, encoding='utf-8')
print('Tiga produk ditambahkan; HTML tunggal diperbarui.')
