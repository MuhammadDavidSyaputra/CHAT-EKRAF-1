const fs=require('fs'),vm=require('vm'),assert=require('assert/strict');
const s=fs.readFileSync('veloce/dist/app.js','utf8');
const elements=new Map();let renders=0,scrolled=false,focused=false;
function el(id){if(!elements.has(id))elements.set(id,{value:'',hidden:true,events:{},addEventListener(name,fn){this.events[name]=fn},focus(){focused=true},blur(){},setAttribute(){},scrollIntoView(){scrolled=true}});return elements.get(id)}
const context=vm.createContext({document:{getElementById:el},window:{matchMedia:()=>({matches:true})},render(){renders++}});
vm.runInContext(s.slice(s.indexOf('const searchInput'),s.indexOf('function render(){')),context);
const input=el('car-search');input.value='R34';input.events.input();
assert.equal(renders,0);assert.equal(vm.runInContext('submittedQuery',context),'');
let prevented=false;el('car-search-form').events.submit({preventDefault(){prevented=true}});
assert(prevented);assert.equal(renders,1);assert.equal(vm.runInContext('submittedQuery',context),'R34');assert(scrolled);assert(focused);
input.value='BMW';input.events.input();assert.equal(renders,1);assert.equal(vm.runInContext('submittedQuery',context),'R34');
el('clear-search').events.click();assert.equal(vm.runInContext('submittedQuery',context),'');assert.equal(renders,2);
console.log('OK: mengetik tidak memfilter; Enter/Cari menerapkan pencarian dan menuju hasil; hapus mengembalikan katalog.');
