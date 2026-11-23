const {chromium}=require('playwright');
const fs=require('fs');
const OUT='public/shots', URL='https://zylo.video/';
const boxes={};
(async()=>{
 const b=await chromium.launch();
 async function page(opts){const ctx=await b.newContext(opts);const p=await ctx.newPage();
   await p.addInitScript(()=>{window.__si=window.setInterval;window.setInterval=(f,t)=>t===420?0:window.__si(f,t);});
   await p.goto(URL,{waitUntil:'networkidle'});await p.waitForFunction(()=>document.querySelectorAll('.card:not(.skel)').length>10);
   await p.waitForTimeout(1500);return p;}
 const rect=async(p,sel)=>p.$eval(sel,e=>{const r=e.getBoundingClientRect();return {x:r.x,y:r.y,w:r.width,h:r.height}});
 async function snap(p,name,sels={}){await p.waitForTimeout(500);await p.screenshot({path:`${OUT}/${name}.jpg`,type:'jpeg',quality:92});
   boxes[name]={};for(const [k,s] of Object.entries(sels)){try{boxes[name][k]=await rect(p,s)}catch(e){console.log('nobox',name,k)}}}
 async function scrollTo(p,sel,off=90){await p.evaluate(([s,o])=>{const e=document.querySelector(s);window.scrollTo(0,e.getBoundingClientRect().top+scrollY-o)},[sel,off]);await p.waitForTimeout(700);}
 const desk={viewport:{width:1600,height:900},deviceScaleFactor:2,colorScheme:'dark'};
 let p=await page(desk);
 // hero caption stop-motion
 const n=await p.$$eval('#hl .cap',c=>c.length);
 for(let i=-1;i<n;i++){await p.evaluate(i=>{document.querySelectorAll('#hl .cap').forEach((c,j)=>{c.classList.remove('on','done','todo');if(i>=0){c.classList.toggle('on',j===i);c.classList.toggle('done',j<i);c.classList.toggle('todo',j>i);}})},i);
   await snap(p,`hero_${i+1}`,i===-1?{stats:'.stats',phones:'#frontPhone',cta:'.cta .btn-hi',subscribe:'.bar .btn-hi'}:{});}
 // archive
 await scrollTo(p,'#videos',70); await snap(p,'archive',{head:'#videos .shead h2',chips:'#chips',grid:'#grid',first:'#grid .card:first-child',firstThumb:'#grid .card:first-child .thumb',newtag:'#grid .card:first-child .tag-new'});
 await scrollTo(p,'#grid',120); await snap(p,'cards',{first:'#grid .card:first-child',newtag:'#grid .card:first-child .tag-new',long:'#grid .card:has(.pill:not(:empty)) .pill'});
 const longIdx=await p.$$eval('#grid .card',cs=>cs.findIndex(c=>/Full story/.test(c.textContent)));
 if(longIdx>=0){boxes.cards.long=await p.$$eval('#grid .card',(cs,i)=>{const r=cs[i].querySelector('.pill').getBoundingClientRect();return{x:r.x,y:r.y,w:r.width,h:r.height}},longIdx);}
 await scrollTo(p,'#videos .tools',110);
 await snap(p,'filters_all',{chips:'#chips',history:'#chips [data-k=history]',science:'#chips [data-k=science]'});
 await p.click('#chips [data-k=history]'); await snap(p,'filters_history',{history:'#chips [data-k=history]',grid:'#grid'});
 await p.click('#chips [data-k=all]');
 await p.click('#q'); await p.keyboard.type('zombie',{delay:60}); await p.waitForTimeout(400);
 await snap(p,'search_zombie',{q:'#q',grid:'#grid',sort:'#sort'});
 await p.fill('#q',''); await p.selectOption('#sort','views'); await snap(p,'sort_views',{sort:'#sort',grid:'#grid'});
 await p.selectOption('#sort','new');
 await scrollTo(p,'#moreBtn',600); await snap(p,'more',{more:'#moreBtn'});
 // player
 await scrollTo(p,'#grid',120); const card=await rect(p,'#grid .card:nth-child(2) .thumb'); boxes.player_before={card};
 await snap(p,'player_before',{card:'#grid .card:nth-child(2) .thumb'});
 await p.click('#grid .card:nth-child(2)'); await p.waitForTimeout(6000);
 await snap(p,'player',{player:'#player',open:'#plink',close:'#closeBtn'});
 await p.click('#closeBtn');
 // suggest
 await scrollTo(p,'#suggest',100);
 await snap(p,'suggest_empty',{panel:'#suggest',idea:'#idea'});
 await p.click('#idea'); await p.keyboard.type('What if the Moon disappeared for one night?',{delay:20});
 await p.selectOption('#topic','history'); await p.fill('#name','Sam');
 await snap(p,'suggest_filled',{idea:'#idea',topic:'#topic',name:'#name',email:'#email',send:'#ideaBtn'});
 // ask
 await scrollTo(p,'#ask',100);
 await snap(p,'ask_empty',{panel:'#ask',q:'#question',samples:'#samples',ask:'#askBtn'});
 await p.click('#question'); await p.keyboard.type('Why was Krakatoa so loud?',{delay:20});
 await snap(p,'ask_typed',{q:'#question',ask:'#askBtn',samples:'#samples'});
 // faq
 await scrollTo(p,'#faq',100); await p.click('#faq details:nth-of-type(2) summary'); await snap(p,'faq',{qa:'#faq .qa',open:'#faq details:nth-of-type(2)'});
 await scrollTo(p,'.band',60); await snap(p,'band',{btn:'.band .btn'});
 // light theme
 p=await page({...desk,colorScheme:'light'});
 await p.evaluate(()=>{const c=document.querySelectorAll('#hl .cap');c.forEach(x=>x.classList.remove('on','done','todo'));c[4].classList.add('on')});
 await snap(p,'light_hero'); await scrollTo(p,'#videos',70); await snap(p,'light_archive');
 await scrollTo(p,'#suggest',100); await snap(p,'light_suggest');
 // mobile
 const mob={viewport:{width:390,height:844},deviceScaleFactor:3,isMobile:true,hasTouch:true};
 for(const scheme of ['dark','light']){p=await page({...mob,colorScheme:scheme});
   await p.evaluate(()=>{const c=document.querySelectorAll('#hl .cap');c.forEach(x=>x.classList.remove('on','done','todo'));c[1].classList.add('on')});
   await snap(p,`m_${scheme}_hero`); await scrollTo(p,'#grid',130); await snap(p,`m_${scheme}_grid`);
   await scrollTo(p,'#ask',80); await snap(p,`m_${scheme}_ask`);}
 fs.writeFileSync('public/shots/boxes.json',JSON.stringify(boxes,null,1));
 await b.close();
})();
