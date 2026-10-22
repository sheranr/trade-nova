/* Trade Nova service worker — makes the web app work offline and updates it in the background. */
const VERSION='2.2.2';
const CORE='tn-core-'+VERSION, PDFS='tn-pdf-v1';
const ASSETS=['./','index.html','hsdata.js','prices.js','manifest.webmanifest','icons/icon-192.png','icons/icon-512.png','icons/favicon-32.png','icon.png','splash-web.jpg','pdf/pdf.js','pdf/pdf.worker.js'];
self.addEventListener('install',e=>{ self.skipWaiting(); e.waitUntil(caches.open(CORE).then(c=>c.addAll(ASSETS.map(u=>new Request(u,{cache:'reload'}))))) });
self.addEventListener('activate',e=>{ e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k.startsWith('tn-core-')&&k!==CORE).map(k=>caches.delete(k)))).then(()=>self.clients.claim())) });
self.addEventListener('message',e=>{ if(e.data==='skip') self.skipWaiting() });
self.addEventListener('fetch',e=>{
  const u=new URL(e.request.url);
  if(e.request.method!=='GET'||u.origin!==location.origin) return;
  if(u.pathname.includes('/ota/')||u.pathname.includes('/download/')||u.pathname.includes('/content/')||u.pathname.includes('/admin/')) return;            // always from the network
  // the app page and its data: newest from the network when online (4 s limit), the saved copy when offline
  const core=e.request.mode==='navigate'?'index.html':(/\/(hsdata|prices)\.js$/.exec(u.pathname)||[])[0];
  if(core){ const key=core.replace(/^\//,'');
    e.respondWith(caches.open(CORE).then(c=>new Promise(res=>{ let done=false;
      const fall=()=>{ if(!done){ done=true; c.match(key).then(r=>res(r||fetch(e.request))) } };
      const t=setTimeout(fall,4000);
      fetch(e.request.mode==='navigate'?new Request('index.html',{cache:'no-cache'}):new Request(e.request,{cache:'no-cache'})).then(n=>{ clearTimeout(t); if(n.ok){ c.put(key,n.clone()); if(!done){ done=true; res(n) } } else fall() }).catch(()=>{ clearTimeout(t); fall() });
    }))); return }
  if(u.pathname.includes('/pdf/')&&u.pathname.endsWith('.pdf')){                          // documents: cache after first view
    e.respondWith(caches.open(PDFS).then(c=>c.match(e.request).then(r=>r||fetch(e.request).then(n=>{ if(n.ok) c.put(e.request,n.clone()); return n })))); return }
  e.respondWith(caches.match(e.request,{ignoreSearch:true}).then(r=>r||fetch(e.request)));
});
