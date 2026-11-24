const {chromium}=require('playwright');const fs=require('fs');
const OUT='public/mshots',URL='https://zylo.video/';const boxes={};
(async()=>{const b=await chromium.launch();
 async function page(scheme){const ctx=await b.newContext({viewport:{width:390,height:844},deviceScaleFactor:3,isMobile:true,hasTouch:true,colorScheme:scheme});const p=await ctx.newPage();
  await p.addInitScript(()=>{window.__si=window.setInterval;window.setInterval=(f,t)=>t===420?0:window.__si(f,t);});
  await p.goto(URL,{waitUntil:'networkidle'});await p.waitForFunction(()=>document.querySelectorAll('.card:not(.skel)').length>10);await p.waitForTimeout(1500);return p;}
 const rect=(p,s)=>p.$eval(s,e=>{const r=e.getBoundingClientRect();return{x:r.x,y:r.y,w:r.width,h:r.height}});
 async function snap(p,name,sels={}){await p.waitForTimeout(450);await p.screenshot({path:`${OUT}/${name}.jpg`,type:'jpeg',quality:92});boxes[name]={};
  for(const [k,s] of Object.entries(sels)){try{boxes[name][k]=await rect(p,s)}catch{console.log('nobox',name,k)}}}
 async function sc(p,sel,off){await p.evaluate(([s,o])=>{const e=document.querySelector(s);window.scrollTo(0,e.getBoundingClientRect().top+scrollY-o)},[sel,off]);await p.waitForTimeout(600);}
 let p=await page('dark');
 const n=await p.$$eval('#hl .cap',c=>c.length);
 for(let i=-1;i<n;i++){await p.evaluate(i=>{document.querySelectorAll('#hl .cap').forEach((c,j)=>{c.classList.remove('on','done','todo');if(i>=0){c.classList.toggle('on',j===i);c.classList.toggle('done',j<i);c.classList.toggle('todo',j>i);}})},i);
   await snap(p,`hero_${i+1}`,i===-1?{h1:'#hl',stats:'.stats',cta:'.cta'}:{});}
 await sc(p,'#videos',90);await snap(p,'archive',{head:'#videos .shead h2',chips:'#chips'});
 await sc(p,'#grid',100);await snap(p,'grid',{first:'#grid .card:first-child',second:'#grid .card:nth-child(2)',newtag:'#grid .card:first-child .tag-new'});
 await sc(p,'#chips',100);await snap(p,'chips',{chips:'#chips',history:'#chips [data-k=history]',q:'#q'});
 await p.click('#chips [data-k=history]');await snap(p,'chips_history',{history:'#chips [data-k=history]',grid:'#grid'});
 await p.click('#chips [data-k=all]');await sc(p,'#chips',100);await p.click('#q');await p.keyboard.type('zombie',{delay:40});await p.evaluate(()=>document.activeElement.blur());
 await sc(p,'#q',100);await snap(p,'search',{q:'#q',grid:'#grid'});
 await p.fill('#q','');await p.evaluate(()=>document.querySelector('#q').dispatchEvent(new Event('input')));await p.waitForTimeout(300);
 await sc(p,'#grid',100);await snap(p,'player_before',{card:'#grid .card:nth-child(2) .thumb'});
 await p.click('#grid .card:nth-child(2)');await p.waitForTimeout(5000);await snap(p,'player',{player:'#player',open:'#plink'});await p.click('#closeBtn');
 await sc(p,'#suggest',80);await p.click('#idea');await p.keyboard.type('What if the Moon disappeared for one night?',{delay:10});await p.evaluate(()=>document.activeElement.blur());
 await p.selectOption('#topic','history');await sc(p,'#suggest',80);await snap(p,'suggest',{panel:'#suggest',idea:'#idea',topic:'#topic',send:'#ideaBtn'});
 await sc(p,'#ask',80);await p.click('#question');await p.keyboard.type('Why was Krakatoa so loud?',{delay:10});await p.evaluate(()=>document.activeElement.blur());
 await sc(p,'#ask',80);await snap(p,'ask',{panel:'#ask',q:'#question',ask:'#askBtn',samples:'#samples'});
 p=await page('light');await p.evaluate(()=>{const c=document.querySelectorAll('#hl .cap');c.forEach(x=>x.classList.remove('on','done','todo'));c[1].classList.add('on')});
 await sc(p,'#grid',100);await snap(p,'light_grid');
 p=await page('dark');await p.evaluate(()=>{const c=document.querySelectorAll('#hl .cap');c.forEach(x=>x.classList.remove('on','done','todo'));c[1].classList.add('on')});
 await sc(p,'#grid',100);await snap(p,'dark_grid');
 fs.writeFileSync(`${OUT}/boxes.json`,JSON.stringify(boxes,null,1));await b.close();})();
