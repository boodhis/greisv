/* Service Worker: офлайн-режим.
   Стратегия network-first (свежесть важнее кэша), offline — из кэша.
   ВАЖНО: ASSETS должен покрывать все страницы сайта — проверка в tests/test_site.py
   (test_sw_precache_covers_all_pages). После добавления страницы пересобери список
   (git ls-files '*.html') и подними версию CACHE, чтобы старый кэш обновился. */
var CACHE = "fortress-v16";
var ASSETS = [
  "./",
  "index.html",
  "manifest.html",
  "style.css",
  "favicon.svg",
  "icon-192.png",
  "icon-512.png",
  "manifest.webmanifest",
  "sitemap.xml",
  "robots.txt",
  "js/notes.js",
  "study/data/srs.js",
  "study/data/wordday.js",
  "study/data/widget.js",
  "study/index.html",
  "study/cheatsheets.html",
  "electric/index.html",
  "electric/panels.html",
  "electric/safety.html",
  "electric/smart.html",
  "electric/wiring.html",
  "getting-started/bootable-usb.html",
  "getting-started/first-steps.html",
  "getting-started/index.html",
  "getting-started/install-ubuntu.html",
  "guides/auto-setup.html",
  "guides/auto-shutdown.html",
  "guides/backup.html",
  "guides/diagnostics.html",
  "guides/disk-health.html",
  "guides/index.html",
  "guides/journalctl.html",
  "guides/ssh.html",
  "guides/terminal.html",
  "guides/wifi-fix.html",
  "hobbies/esp32.html",
  "hobbies/guitar.html",
  "hobbies/index.html",
  "homelab/hardware.html",
  "homelab/index.html",
  "homelab/network.html",
  "homelab/server-reference.html",
  "homelab/sopds-web.html",
  "resources/git-commands.html",
  "resources/index.html",
  "resources/inxi.html",
  "resources/links.html",
  "resources/opencode-windows.html",
  "services/docker.html",
  "services/immich.html",
  "services/index.html",
  "services/jellyfin.html",
  "services/minidlna.html",
  "services/mqtt.html",
  "services/navidrome.html",
  "services/open-webui.html",
  "services/samba.html",
  "services/sopds.html",
  "services/transmission.html",
  "guides/publish.html",
  "guides/about.html",
  "guides/obsidian-github.html",
];

self.addEventListener("install", function (e) {
  e.waitUntil(
    caches.open(CACHE).then(function (c) {
      return Promise.all(ASSETS.map(function (a) {
        return c.add(a).catch(function () {});
      }));
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