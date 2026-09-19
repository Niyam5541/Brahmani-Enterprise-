const SHOP={name:"Brahmani Enterprise",whatsapp:"919824972745",phone1:"+91 98249 72745",phone2:"+91 98249 72845",address:"Opp. Golden Industrial, Near Mahadev Mandir, Sayan–Delad Gam, Surat, Gujarat",maps:"https://maps.app.goo.gl/NhMJjw7vSJwXC8zv6?g_st=ac"};
const expanded=PRODUCTS.map((p,i)=>({id:i+1,name:p[0],category:p[1],page:p[2]}));
const els={grid:document.getElementById('productsGrid'),search:document.getElementById('searchInput'),category:document.getElementById('categoryFilter'),count:document.getElementById('resultCount'),load:document.getElementById('loadMore'),quick:document.getElementById('quickTags')};
let visible=32,filtered=[...expanded],cart=JSON.parse(localStorage.getItem('be_cart')||'[]');
const aliases={lino:'leno',bobbin:'bobin',nozel:'nozzel',nozzle:'nozzel',ceramic:'ciramic',pulley:'pully',tensioner:'tensior',motor:'motar',collar:'coler',clamp:'clemper'};
function norm(s){return (s||'').toLowerCase().replace(/[^a-z0-9]+/g,' ').trim().split(/\s+/).map(w=>aliases[w]||w).join(' ')}
function iconFor(c){c=c.toLowerCase();if(c.includes('pump'))return '💧';if(c.includes('bearing'))return '◎';if(c.includes('nozzle'))return '➤';if(c.includes('cutter'))return '✂';if(c.includes('feeder'))return '↻';if(c.includes('dobby'))return '⚙';if(c.includes('elect'))return '⚡';return '⚙'}
function categories(){return [...new Set(expanded.map(p=>p.category))].sort()}
categories().forEach(c=>{const o=document.createElement('option');o.value=c;o.textContent=c;els.category.appendChild(o)});
['Leno Bobin','Pump Cam','Nozzle','Dobby Bearing','Cutter Lever','Feeder','Bearing','Catchcord'].forEach(q=>{const b=document.createElement('button');b.textContent=q;b.onclick=()=>{els.search.value=q;filterProducts()};els.quick.appendChild(b)});
function filterProducts(){const q=norm(els.search.value),cat=els.category.value;filtered=expanded.filter(p=>{const hay=norm(p.name+' '+p.category);const words=q.split(' ').filter(Boolean);return (!cat||p.category===cat)&&words.every(w=>hay.includes(w))});visible=32;renderProducts()}
function imageSpec(p){
 try{
  const raw=atob(window.IMG_SPEC_B64||'');
  const i=(p.id-1)*2;
  if(i+1>=raw.length)return null;
  const v=(raw.charCodeAt(i)<<8)|raw.charCodeAt(i+1);
  if(v===65535)return null;
  return [v>>7,(v>>3)&15,v&7];
 }catch(e){return null}
}
function productPhoto(p){
 const m=imageSpec(p);
 if(!m)return `<div class="product-photo fallback"><span>${iconFor(p.category)}</span></div>`;
 const [pg,row,col]=m;
 const nano=pg>=11;
 const cw=nano?36:48, ch=nano?24:32, scale=nano?4:3;
 const src=(window.SPRITES||{})[pg]||`sprites/p${String(pg).padStart(2,'0')}.webp`;
 const x=col*cw*scale, y=row*ch*scale;
 return `<div class="product-photo"><div class="sprite-crop" role="img" aria-label="${p.name.replace(/"/g,'&quot;')}" style="background-image:url('${src}');background-size:${cw*5*scale}px auto;background-position:-${x}px -${y}px"></div></div>`;
}
function renderProducts(){
 els.grid.innerHTML='';
 filtered.slice(0,visible).forEach(p=>{
  const card=document.createElement('article');
  card.className='product-card';
  card.innerHTML=`${productPhoto(p)}<div class="product-category">${p.category}</div><h3 class="product-name">${p.name}</h3><div class="product-meta">Catalogue page ${p.page} • Photo from catalogue</div><div class="qty-row"><input type="number" min="1" value="1" aria-label="Quantity"><button type="button">Add to Order</button></div>`;
  const inp=card.querySelector('input');
  card.querySelector('button').onclick=()=>addCart(p,Math.max(1,parseInt(inp.value)||1));
  els.grid.appendChild(card);
 });
 els.count.textContent=`${filtered.length} part${filtered.length===1?'':'s'} found`;
 els.load.style.display=visible>=filtered.length?'none':'block';
}
function addCart(p,qty){const e=cart.find(x=>x.id===p.id);if(e)e.qty+=qty;else cart.push({...p,qty});saveCart();openCart()}
function saveCart(){localStorage.setItem('be_cart',JSON.stringify(cart));renderCart()}
function renderCart(){document.getElementById('cartCount').textContent=cart.reduce((a,b)=>a+b.qty,0);const box=document.getElementById('cartItems');if(!cart.length){box.innerHTML='<div class="empty-cart">Your order cart is empty.<br>Search a part and tap <b>Add to Order</b>.</div>';return}box.innerHTML='';cart.forEach((x,i)=>{const d=document.createElement('div');d.className='cart-line';d.innerHTML=`<div><b>${x.name}</b><small>${x.category}</small></div><div class="cart-controls"><button data-a="minus">−</button><span>${x.qty}</span><button data-a="plus">+</button><button class="remove-btn" data-a="remove">×</button></div>`;d.querySelector('[data-a="minus"]').onclick=()=>{x.qty=Math.max(1,x.qty-1);saveCart()};d.querySelector('[data-a="plus"]').onclick=()=>{x.qty++;saveCart()};d.querySelector('[data-a="remove"]').onclick=()=>{cart.splice(i,1);saveCart()};box.appendChild(d)})}
const drawer=document.getElementById('cartDrawer'),back=document.getElementById('drawerBackdrop');function openCart(){drawer.classList.add('open');back.classList.add('show')}function closeCart(){drawer.classList.remove('open');back.classList.remove('show')}document.getElementById('cartFab').onclick=openCart;document.getElementById('closeCart').onclick=closeCart;back.onclick=closeCart;
document.getElementById('checkoutBtn').onclick=()=>{if(!cart.length){alert('Please add at least one spare part to your order.');return}const customer=document.getElementById('customerName').value.trim(),company=document.getElementById('companyName').value.trim(),addr=document.getElementById('customerAddress').value.trim();let msg=`WATER JET LOOM SPARE PARTS ORDER

Supplier: ${SHOP.name}
Supplier Address: ${SHOP.address}
Google Maps: ${SHOP.maps}

ORDER ITEMS:
`;cart.forEach((x,i)=>msg+=`${i+1}. ${x.name}
   Category: ${x.category}
   Qty: ${x.qty}
`);msg+=`
Customer Name: ${customer||'Not provided'}
Company: ${company||'Not provided'}
Delivery Address/Location: ${addr||'Not provided'}

Please confirm price and availability.`;window.open(`https://wa.me/${SHOP.whatsapp}?text=${encodeURIComponent(msg)}`,'_blank')};
els.search.addEventListener('input',filterProducts);els.category.addEventListener('change',filterProducts);document.getElementById('clearSearch').onclick=()=>{els.search.value='';els.category.value='';filterProducts()};els.load.onclick=()=>{visible+=32;renderProducts()};document.getElementById('year').textContent=new Date().getFullYear();document.getElementById('partCount').textContent=expanded.length+'+';renderProducts();renderCart();