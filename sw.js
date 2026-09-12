/* Service Worker: офлайн-режим.
   Стратегия network-first (свежесть важнее кэша), offline — из кэша. */
var CACHE = "fortress-v2";
var ASSETS = [
  "./",
  "index.html",
  "manifest.html",
  "style.css",
  "favicon.svg",
  "manifest.webmanifest",
  "js/wall.js",
  "study/index.html",
  "study/words.html",
  "study/cheatsheets.html",
  "study/data/deck.js",
  "study/data/srs.js",
  "study/data/wordday.js",
  "study/data/widget.js",
  "electric/index.html",
  "electric/safety.html",
  "electric/panels.html",
  "electric/wiring.html",
  "electric/smart.html"
];

self.addEventListener("install", function (e) {
  e.waitUntil(
    caches.open(CACHE).then(function (c) {
      return c.addAll(ASSETS);
    }).then(function () { return self.skipWaiting(); })
  );
});

self.addEventListener("activate", function (e) {
  e.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(keys.filter(function (k) { return k !== CACHE; }).map(function (k) { return caches.delete(k); }));
    }).then(function () { return self.clients.claim(); })
  );
});

self.addEventListener("fetch", function (e) {
  var url = new URL(e.request.url);
  if (e.request.method !== "GET") return;
  if (url.origin !== location.origin) return;
  e.respondWith(
    fetch(e.request).then(function (res) {
      if (res.ok) {
        var copy = res.clone();
        caches.open(CACHE).then(function (c) { c.put(e.request, copy); });
      }
      return res;
    }).catch(function () {
      return caches.match(e.request).then(function (hit) {
        return hit || caches.match("./index.html");
      });
    })
  );
});