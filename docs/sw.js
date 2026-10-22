/* Trade Nova service worker — makes the web app work offline and updates it in the background. */
const VERSION='2.0.0';
const CORE='tn-core-'+VERSION, PDFS='tn-pdf-v1';
const ASSETS=['./','index.html','hsdata.js','prices.js','manifest.webmanifest','icons/icon-192.png','icons/icon-512.png','icons/favicon-32.png','pdf/pdf.js','pdf/pdf.worker.js'];
self.addEventListener('install',e=>{ e.waitUntil(caches.open(CORE).then(c=>c.addAll(ASSETS.map(u=>new Request(u,{cache:'reload'}))))) });
self.addEventListener('activate',e=>{ e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k.startsWith('tn-core-')&&k!==CORE).map(k=>caches.delete(k)))).then(()=>self.clients.claim())) });
self.addEventListener('message',e=>{ if(e.data==='skip') self.skipWaiting() });
self.addEventListener('fetch',e=>{
  const u=new URL(e.request.url);
  if(e.request.method!=='GET'||u.origin!==location.origin) return;
  if(u.pathname.includes('/ota/')||u.pathname.includes('/download/')) return;            // always from the network
  if(e.request.mode==='navigate'){ e.respondWith(caches.match('index.html').then(r=>r||fetch(e.request))); return }
  if(u.pathname.includes('/pdf/')&&u.pathname.endsWith('.pdf')){                          // documents: cache after first view
    e.respondWith(caches.open(PDFS).then(c=>c.match(e.request).then(r=>r||fetch(e.request).then(n=>{ if(n.ok) c.put(e.request,n.clone()); return n })))); return }
  e.respondWith(caches.match(e.request,{ignoreSearch:true}).then(r=>r||fetch(e.request)));
});
