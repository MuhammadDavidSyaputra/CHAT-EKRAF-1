const fs=require('fs'),vm=require('vm'),assert=require('assert/strict');
const source=fs.readFileSync('veloce/dist/app.js','utf8');
const context=vm.createContext({});
vm.runInContext(source.split('const waSvg')[0],context);
vm.runInContext(source.slice(source.indexOf('const normalizeSearch'),source.indexOf("searchInput.addEventListener")),context);
function matches(query,brand='Semua merek'){
 context.query=query;context.brand=brand;
 return vm.runInContext("cars.filter(c=>(brand==='Semua merek'||c.brand===brand)&&matchesSearch(c,query)).map(c=>c.id).join(',')",context);
}
assert.equal(matches('r34'),'skyline-r34');
assert.equal(matches(' BMW '),'bmw');
assert.equal(matches('gtr'),'skyline-r34,nissan');
assert.equal(matches('Toyota Supra'),'supra-a80,supra');
assert.equal(matches('Supra','Nissan'),'');
assert.equal(matches('tidak ada mobil ini'),'');
assert.equal(matches('').split(',').length,10);
assert.equal(matches('<script>alert(1)</script>'),'');
const html=fs.readFileSync('penjualan-mobil-sport.html','utf8');
new vm.Script(html.split('<script>')[1].split('</script>')[0]);
assert(html.includes('id="car-search"'));
assert(html.includes('empty-results'));
console.log('OK: pencarian merek/model, kapital, GT-R, gabungan filter, hasil kosong, reset kosong, dan HTML tunggal.');
