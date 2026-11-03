/* Brahmani Enterprise premium progressive enhancements.
   No changes to existing products array or WhatsApp checkout. */
(()=>{
"use strict";
const reduced=window.matchMedia&&window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const nav=document.querySelector(".nav");
const links=nav&&nav.querySelector("nav");
if(nav&&links&&!nav.querySelector(".be-mobile-toggle")){
  const toggle=document.createElement("button");
  toggle.type="button";toggle.className="be-mobile-toggle";
  toggle.setAttribute("aria-label","Open navigation menu");
  toggle.setAttribute("aria-controls","be-mobile-links");
  toggle.setAttribute("aria-expanded","false");
  toggle.textContent="☰";
  links.id="be-mobile-links";nav.appendChild(toggle);
  const close=()=>{links.classList.remove("be-menu-open");toggle.setAttribute("aria-expanded","false");toggle.setAttribute("aria-label","Open navigation menu");toggle.textContent="☰";};
  toggle.addEventListener("click",()=>{
    const show=!links.classList.contains("be-menu-open");
    if(show){links.classList.add("be-menu-open");toggle.textContent="×";toggle.setAttribute("aria-expanded","true");toggle.setAttribute("aria-label","Close navigation menu");}
    else close();
  });
  links.querySelectorAll("a").forEach(a=>a.addEventListener("click",close));
  document.addEventListener("keydown",e=>{if(e.key==="Escape")close()});
}
const hero=document.querySelector(".hero");
if(hero&&!document.querySelector(".be-marquee")){
 const bar=document.createElement("div");bar.className="be-marquee";bar.setAttribute("aria-hidden","true");
 const track=document.createElement("div");track.className="be-marquee-track";
 const words=["WATER JET WEAVING","PRECISION COMPONENTS","LOOM SPARE PARTS","SURAT, GUJARAT","BRAHMANI ENTERPRISE"];
 for(let i=0;i<2;i++)for(const word of words){const s=document.createElement("span");s.textContent=word;track.appendChild(s);const star=document.createElement("i");star.textContent="✦";track.appendChild(star);}
 bar.appendChild(track);hero.insertAdjacentElement("afterend",bar);
}
const grid=document.getElementById("productsGrid");
function upgradePhotos(){
 if(!grid)return;
 const photos=window.ENHANCED_PRODUCT_IMAGES||{};
 for(const card of grid.querySelectorAll(".product-card:not([data-be-photo-checked])")){
    card.setAttribute("data-be-photo-checked","true");
    const name=card.querySelector(".product-name")?.textContent?.trim()||"";
    const key=name.toUpperCase().replace(/\s+/g," ");
    const src=photos[key]||photos[name]||photos[key.replace(/\s*&\s*/g," & ")];
    const icon=card.querySelector(".product-icon");
    if(!src||!icon||!(src.startsWith("data:image/")||src.startsWith("https://")))continue;
    const pic=document.createElement("img");
    pic.alt=name+" — reference product image";
    pic.loading="lazy";pic.decoding="async";pic.src=src;
    icon.textContent="";icon.classList.add("product-photo");icon.appendChild(pic);
 }
}
upgradePhotos();
if(grid){const observer=new MutationObserver(()=>upgradePhotos());observer.observe(grid,{childList:true});}
if(!reduced && "IntersectionObserver" in window){
 const sections=document.querySelectorAll(".section-head,.hero-grid>div,.about-grid>div,.business-card,.shop-info,.trust-grid>div");
 const io=new IntersectionObserver(entries=>{
  entries.forEach(entry=>{if(entry.isIntersecting){entry.target.classList.add("be-visible");io.unobserve(entry.target);}});
 },{threshold:.08,rootMargin:"0px 0px -25px 0px"});
 sections.forEach(el=>{el.classList.add("be-fade-in");io.observe(el)});
}
const imgs=[...document.querySelectorAll(".feature-media img,.hero-media img")];
imgs.forEach(im=>{im.addEventListener("error",()=>{im.style.objectFit="contain";im.style.background="linear-gradient(130deg,#10283a,#21394c)";});});
})();