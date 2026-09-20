const CACHE='bio-estudos-v2';
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE).then(cache => cache.addAll(['./', './index.html', './manifest.webmanifest', './sw.js']))
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
  event.respondWith(
    caches.match(event.request).then(response => response || fetch(event.request).then(network => {
      const copy = network.clone();
      caches.open(CACHE).then(cache => cache.put(event.request, copy));
      return network;
    }).catch(() => caches.match('./index.html'))))
  );
});