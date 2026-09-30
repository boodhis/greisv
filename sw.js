/* Service Worker: офлайн-режим.
   Стратегия network-first (свежесть важнее кэша), offline — из кэша.
   ВАЖНО: ASSETS должен покрывать все страницы сайта — проверка в tests/test_site.py
   (test_sw_precache_covers_all_pages). После добавления страницы пересобери список
   (git ls-files '*.html') и подними версию CACHE, чтобы старый кэш обновился. */
var CACHE = "fortress-v28";
var ASSETS = [
  "articles/books.html",
  "articles/esp32.html",
  "articles/guitar.html",
  "articles/index.html",
  "articles/protivofaza.html",
  "articles/quest3.html",
  "electric/components.html",
  "electric/index.html",
  "electric/panels.html",
  "electric/safety.html",
  "electric/smart.html",
  "electric/standards.html",
  "electric/tools.html",
  "electric/wiring.html",
  "getting-started/bootable-usb.html",
  "getting-started/first-steps.html",
  "getting-started/index.html",
  "getting-started/install-ubuntu.html",
  "homelab/auto-setup.html",
  "homelab/auto-shutdown.html",
  "homelab/backup.html",
  "homelab/diagnostics.html",
  "homelab/disk-health.html",
  "homelab/docker.html",
  "homelab/hardware.html",
  "homelab/homelab-kit.html",
  "homelab/immich.html",
  "homelab/index.html",
  "homelab/inxi.html",
  "homelab/jellyfin.html",
  "homelab/journalctl.html",
  "homelab/minidlna.html",
  "homelab/mqtt.html",
  "homelab/navidrome.html",
  "homelab/network.html",
  "homelab/samba.html",
  "homelab/server-reference.html",
  "homelab/sopds-web.html",
  "homelab/sopds.html",
  "homelab/transmission.html",
  "homelab/wifi-fix.html",
  "index.html",
  "manifest.html",
  "study/cheatsheets.html",
  "study/devops.html",
  "study/git-commands.html",
  "study/index.html",
  "study/links.html",
  "study/linux-app-dev.html",
  "study/obsidian-github.html",
  "study/opencode-windows.html",
  "study/powershell.html",
  "study/python.html",
  "study/ssh.html",
  "study/terminal.html",
  "study/web-dev.html",
  "favicon.svg",
  "manifest.webmanifest",
  "style.css"
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