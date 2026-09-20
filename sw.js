const CACHE='bio-estudos-v3';
const APP_ASSETS = [
  './',
  './index.html',
  './questions.json',
  './manifest.webmanifest',
  './sw.js',
  './catalogo_questoes_zoologia/imagens/Q001_figura.png',
  './catalogo_questoes_zoologia/imagens/Q002_figura.png',
  './catalogo_questoes_zoologia/imagens/Q008_figura.png',
  './catalogo_questoes_zoologia/imagens/Q009_figura.png',
  './catalogo_questoes_zoologia/imagens/Q010_figura.png',
  './catalogo_questoes_zoologia/imagens/Q012_figura.png',
  './catalogo_questoes_zoologia/imagens/Q017_figura.png',
  './catalogo_questoes_zoologia/imagens/Q018_figura.png',
  './catalogo_questoes_zoologia/imagens/Q022_figura.png',
  './catalogo_questoes_zoologia/imagens/Q024_figura.png',
  './catalogo_questoes_zoologia/imagens/gabarito_zoologia_9.png',
  './catalogo_questoes_zoologia/imagens/gabarito_zoologia_10.png'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE).then(cache => cache.addAll(APP_ASSETS))
  );
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys => Promise.all(keys.filter(key => key !== CACHE).map(key => caches.delete(key))))
  );
  self.clients.claim();
});

self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;
  const url = new URL(event.request.url);
  if (url.origin !== self.location.origin) return;
  event.respondWith(
    caches.match(event.request).then(response => {
      if (response) return response;
      return fetch(event.request).then(network => {
        const copy = network.clone();
        caches.open(CACHE).then(cache => cache.put(event.request, copy));
        return network;
      }).catch(() => caches.match('./index.html'));
    })
  );
});