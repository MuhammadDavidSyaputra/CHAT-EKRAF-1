from pathlib import Path
import base64
root = Path(__file__).parent
dist = root/'veloce'/'dist'
index = dist/'index.html'
h = index.read_text(encoding='utf-8')
h = h.replace('<div class="search-row" role="search"', '<form id="car-search-form" class="search-row" role="search"', 1)
h = h.replace('aria-controls="catalog"><button', 'aria-controls="catalog" aria-describedby="search-hint" enterkeyhint="search"><button', 1)
h = h.replace('hidden>✕</button></div></div><div class="catalog-tools">', 'hidden>✕</button><button class="search-submit" type="submit">Cari <span aria-hidden="true">↗</span></button></div><p class="search-hint" id="search-hint">Ketik merek atau model, lalu tekan Enter atau tombol Cari.</p></form><div class="catalog-tools">', 1)
assert 'id="car-search-form"' in h and 'type="submit"' in h
index.write_text(h,encoding='utf-8')
app = dist/'app.js'
s = app.read_text(encoding='utf-8')
s = s.replace("const searchInput = document.getElementById('car-search');", "const searchInput = document.getElementById('car-search');\nlet submittedQuery = '';",1)
s = s.replace("searchInput.addEventListener('input',()=>{clearSearch.hidden=!searchInput.value;render()});", "searchInput.addEventListener('input',()=>{clearSearch.hidden=!searchInput.value});\ndocument.getElementById('car-search-form').addEventListener('submit',e=>{e.preventDefault();submittedQuery=searchInput.value.trim();render();searchInput.blur();const results=document.getElementById('catalog');results.setAttribute('tabindex','-1');results.focus({preventScroll:true});results.scrollIntoView({behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth',block:'start'})});",1)
s = s.replace("searchInput.value='';clearSearch.hidden=true;", "searchInput.value='';submittedQuery='';clearSearch.hidden=true;")
s = s.replace('matchesSearch(c,searchInput.value)', 'matchesSearch(c,submittedQuery)',1)
app.write_text(s,encoding='utf-8')
css = dist/'style.css'
style = css.read_text(encoding='utf-8') + '''
.search-hint{font-size:10px;color:#8c9393;margin:9px 0 0;line-height:1.7}.search-field .search-submit{background:var(--red);color:white;padding:10px 17px;font-size:12px;font-weight:600;white-space:nowrap;display:flex;align-items:center;justify-content:center;gap:16px;min-height:38px}.search-field .search-submit:hover{background:#d9342a;color:white}#catalog{scroll-margin-top:30px}#catalog:focus{outline:none}@media(max-width:520px){.search-field .search-submit{padding:9px 12px;gap:9px;min-height:38px}.search-hint{font-size:9px}.search-field{padding-right:7px}}
'''
css.write_text(style,encoding='utf-8')
js = s.replace('assets/bmw-i8.jpg','data:image/jpeg;base64,' + base64.b64encode((dist/'assets/bmw-i8.jpg').read_bytes()).decode('ascii'))
html = h.replace('<link rel="stylesheet" href="style.css">','<style>\n'+style+'\n</style>').replace('<script src="app.js"></script>','<script>\n'+js+'\n</script>')
(root/'penjualan-mobil-sport.html').write_text(html,encoding='utf-8')
print('Pencarian kini dijalankan saat formulir dikirim dengan Enter atau tombol Cari.')
