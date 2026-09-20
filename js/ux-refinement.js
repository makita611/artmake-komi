(() => {
 const box=document.getElementById('lightbox');
 if(!box || typeof window.openLightbox!=='function')return;
 box.setAttribute('role','dialog');box.setAttribute('aria-modal','true');box.setAttribute('aria-label','症例写真と施術の説明');
 const close=box.querySelector('.lightbox-close');close.setAttribute('aria-label','症例写真を閉じる');
 box.querySelectorAll('img,dl,p').forEach(el=>el.addEventListener('click',e=>e.stopPropagation()));
 const note=document.createElement('div');note.className='case-consult-note';
 const text=document.createElement('p'),copy=document.createElement('button'),status=document.createElement('span');
 copy.type='button';copy.textContent='相談文をコピー';status.className='case-consult-status';status.setAttribute('role','status');
 note.append(text,copy,status);note.addEventListener('click',e=>e.stopPropagation());
 box.insertBefore(note,document.getElementById('lightboxConsultBtn'));
 let trigger,previousOpen=window.openLightbox,previousClose=window.closeLightbox,message='';
 copy.addEventListener('click',async()=>{try{await navigator.clipboard.writeText(message);status.textContent='コピーしました。LINEを開いて貼り付けてください。';}catch{status.textContent='コピーできませんでした。上の相談文を選択してコピーしてください。';}});
 window.openLightbox=function(el){trigger=el;previousOpen(el);box.scrollTop=0;const img=el.querySelector('img');const filename=new URL(img.src).pathname.split('/').pop();message='サイトの症例「'+filename+'」について相談したいです。希望地域：／希望部位：\nhttps://artmake-komi.com'+new URL(img.src).pathname;text.textContent=message;status.textContent='相談文をコピーして、LINEに貼り付けて送信できます。';close.focus();};
 window.closeLightbox=function(){previousClose();if(trigger)trigger.focus();};
 document.querySelectorAll('[onclick="openLightbox(this)"]').forEach(el=>{el.tabIndex=0;el.setAttribute('role','button');el.setAttribute('aria-label',(el.querySelector('img')?.alt||'症例写真')+'を拡大');el.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();window.openLightbox(el);}});});
 box.addEventListener('keydown',e=>{if(e.key!=='Tab')return;const items=[...box.querySelectorAll('button,a[href]')].filter(el=>el.getClientRects().length);const first=items[0],last=items[items.length-1];if(e.shiftKey&&document.activeElement===first){e.preventDefault();last.focus();}else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus();}});
})();
