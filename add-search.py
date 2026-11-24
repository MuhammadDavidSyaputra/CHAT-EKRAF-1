from pathlib import Path
import base64
root = Path(__file__).parent
dist = root / 'veloce' / 'dist'
index = dist / 'index.html'
h = index.read_text(encoding='utf-8')
assert 'id="car-search"' not in h
search = '''<div class="search-row" role="search" aria-label="Cari mobil dalam koleksi"><label for="car-search">Cari mobil impian Anda</label><div class="search-field"><svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5" stroke="currentColor" stroke-width="1.6"/><path d="m15.5 15.5 5 5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg><input type="search" id="car-search" placeholder="Cari merek atau model, misalnya Porsche, Supra, R34…" autocomplete="off" aria-controls="catalog"><button type="button" id="clear-search" aria-label="Hapus pencarian" hidden>✕</button></div></div>'''
h = h.replace('<div class="catalog-tools">', search + '<div class="catalog-tools">', 1)
h = h.replace('<div class="result-row"><p>', '<div class="result-row"><p role="status" aria-live="polite" aria-atomic="true">', 1)
index.write_text(h, encoding='utf-8')
app = dist / 'app.js'
s = app.read_text(encoding='utf-8')
insert = '''const searchInput = document.getElementById('car-search');
const clearSearch = document.getElementById('clear-search');
const normalizeSearch = text => text.normalize('NFKD').replace(/[\\u0300-\\u036f]/g,'').toLowerCase().replace(/[^a-z0-9]/g,'');
function matchesSearch(car, query){const text=normalizeSearch([car.brand,car.name,car.type,car.energy].join(' '));return query.trim().split(/\\s+/).filter(Boolean).every(word=>text.includes(normalizeSearch(word)))}
searchInput.addEventListener('input',()=>{clearSearch.hidden=!searchInput.value;render()});
clearSearch.addEventListener('click',()=>{searchInput.value='';clearSearch.hidden=true;render();searchInput.focus()});
function resetCatalog(){searchInput.value='';clearSearch.hidden=true;activeBrand='Semua merek';filters.querySelectorAll('button').forEach(b=>{const active=b.dataset.brand===activeBrand;b.classList.toggle('active',active);b.setAttribute('aria-pressed',String(active))});render();searchInput.focus()}
document.getElementById('catalog').addEventListener('click',e=>{if(e.target.closest('[data-reset-catalog]'))resetCatalog()});
'''
s = s.replace('function render(){', insert + 'function render(){', 1)
s = s.replace("cars.filter(c=>activeBrand==='Semua merek'||c.brand===activeBrand)", "cars.filter(c=>(activeBrand==='Semua merek'||c.brand===activeBrand)&&matchesSearch(c,searchInput.value))", 1)
s = s.replace(".join('');setupImageFallbacks(document.getElementById('catalog'))}", ".join('')||'<div class=\"empty-results\"><span aria-hidden=\"true\">⌕</span><h3>Mobil belum ditemukan</h3><p>Coba nama model lain atau atur ulang pencarian dan filter merek.</p><button class=\"btn red\" type=\"button\" data-reset-catalog>Lihat semua mobil <span>↗</span></button></div>';setupImageFallbacks(document.getElementById('catalog'))}", 1)
app.write_text(s, encoding='utf-8')
css = dist / 'style.css'
style = css.read_text(encoding='utf-8')
style += '''
.search-row{margin:0 0 23px}.search-row>label{display:block;font-size:11px;color:#b4b9b9;margin-bottom:10px}.search-field{display:flex;align-items:center;gap:13px;background:#181a1b;border:1px solid #3b3e3f;padding:0 17px;min-height:54px;transition:border-color .2s}.search-field:focus-within{border-color:var(--red);box-shadow:0 0 0 1px var(--red)}.search-field>svg{width:20px;height:20px;color:#a0a6a6;flex-shrink:0}.search-field input{font:inherit;font-size:13px;color:var(--white);background:transparent;border:0;outline:none;min-width:0;width:100%;padding:17px 0}.search-field input:focus-visible{outline:none}.search-field input::placeholder{color:#828989}.search-field input::-webkit-search-cancel-button{display:none}.search-field button{border:0;color:#c4c9c9;background:transparent;min-width:40px;min-height:40px;font-size:16px}.search-field button:hover{color:var(--red)}.empty-results{grid-column:1/-1;border:1px solid var(--line);padding:52px 20px;text-align:center;background:#151717}.empty-results>span{display:block;color:var(--red);font-size:35px;margin-bottom:15px}.empty-results h3{font:500 24px Manrope;margin-bottom:13px}.empty-results p{font-size:12px;color:#9ca3a3;line-height:1.8;margin-bottom:24px}.empty-results .btn{gap:20px}
@media(max-width:520px){.search-row{margin-bottom:20px}.search-field{padding:0 12px;gap:9px;min-height:52px}.search-field input{font-size:16px;padding:14px 0}.search-field input::placeholder{font-size:12px}.empty-results{padding:38px 17px}.empty-results h3{font-size:22px}}
'''
css.write_text(style, encoding='utf-8')
js = s.replace('assets/bmw-i8.jpg', 'data:image/jpeg;base64,' + base64.b64encode((dist/'assets/bmw-i8.jpg').read_bytes()).decode('ascii'))
standalone = h.replace('<link rel="stylesheet" href="style.css">','<style>\n'+style+'\n</style>').replace('<script src="app.js"></script>','<script>\n'+js+'\n</script>')
(root/'penjualan-mobil-sport.html').write_text(standalone,encoding='utf-8')
print('Kolom pencarian ditambahkan ke situs dan HTML tunggal.')
