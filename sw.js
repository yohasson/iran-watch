/* Iran watch service worker: offline shell + best-effort background check (periodic sync where supported). */
var SHELL = 'iw-shell-v7', CFG = 'iw-cfg';
var RAW = 'https://raw.githubusercontent.com/yohasson/iran-watch/main/data.json';
self.addEventListener('install', function (e) { e.waitUntil(caches.open(SHELL).then(function (c) { return c.addAll(['./', './index.html', './icon.svg']); }).catch(function () {})); self.skipWaiting(); });
self.addEventListener('activate', function (e) { e.waitUntil(self.clients.claim()); });
self.addEventListener('fetch', function (e) {
  var u = new URL(e.request.url);
  if (e.request.method !== 'GET' || u.origin !== self.location.origin || !/\/(index\.html)?$/.test(u.pathname)) return;
  e.respondWith(fetch(e.request).then(function (r) { var cp = r.clone(); caches.open(SHELL).then(function (c) { c.put(e.request, cp); }); return r; }).catch(function () { return caches.match(e.request).then(function (r) { return r || caches.match('./'); }); }));
});
function getCfg() { return caches.open(CFG).then(function (c) { return c.match('cfg'); }).then(function (r) { return r ? r.json() : { thr: 7, thrR: 25, lastKey: '' }; }).catch(function () { return { thr: 7, thrR: 25, lastKey: '' }; }); }
function setCfg(o) { return caches.open(CFG).then(function (c) { return c.put('cfg', new Response(JSON.stringify(o))); }); }
self.addEventListener('message', function (e) { if (e.data && e.data.type === 'cfg') e.waitUntil(getCfg().then(function (o) { o.thr = e.data.thr; o.thrR = e.data.thrR; return setCfg(o); })); });
function check() {
  return Promise.all([fetch(RAW + '?t=' + Date.now(), { cache: 'no-store' }).then(function (r) { return r.json(); }), getCfg()]).then(function (a) {
    var d = a[0], o = a[1], F = d.major && d.major.F, R = d.flight && d.flight.active ? d.flight.R : null, msgs = [];
    if (F >= o.thr) msgs.push('Main estimate ' + F.toFixed(2) + '% – at or above your ' + o.thr + '% alert line');
    if (R != null && R >= o.thrR) msgs.push('Flight risk ' + R.toFixed(1) + '% – at or above your ' + o.thrR + '% line');
    if (d.alert && d.alert.active) msgs.push('An alert is active');
    var key = d.updated_utc + '|' + msgs.join('|');
    if (!msgs.length || key === o.lastKey) return;
    o.lastKey = key; return setCfg(o).then(function () { return self.registration.showNotification('🚨 Iran watch', { body: msgs.join('\n'), icon: 'icon.svg', tag: 'iw', renotify: true }); });
  }).catch(function () {});
}
self.addEventListener('periodicsync', function (e) { if (e.tag === 'iw-check') e.waitUntil(check()); });
self.addEventListener('notificationclick', function (e) { e.notification.close(); e.waitUntil(self.clients.matchAll({ type: 'window' }).then(function (cs) { if (cs.length) return cs[0].focus(); return self.clients.openWindow('./'); })); });
