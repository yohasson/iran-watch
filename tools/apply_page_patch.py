"""Apply tools/page_patch.json to index.html; publish only if the result matches the tested build exactly."""
import hashlib, json, re, sys
p = json.load(open(sys.argv[1], encoding='utf-8'))
path = sys.argv[2]
a = open(path, encoding='utf-8').read()
h = lambda s: hashlib.sha256(s.encode('utf-8')).hexdigest()
if h(a) == p['sha256']:
    print('already up to date'); sys.exit(0)
a = re.sub(r'<span id="pgVer"[^>]*>[^<]*</span>', '<span id="pgVer">Page version 8 \u00b7 25 Nov 2026</span>', a, count=1)
if h(a) != p['base_sha256']:
    print('base mismatch – not applying'); sys.exit(2)
for old, new in reversed(p['reps']):
    if a.count(old) != 1:
        print('anchor not unique – not applying'); sys.exit(3)
    a = a.replace(old, new)
if h(a) != p['sha256']:
    print('result hash mismatch – not applying'); sys.exit(4)
import datetime, zoneinfo
now = datetime.datetime.now(zoneinfo.ZoneInfo('Asia/Jerusalem'))
a = re.sub(r'<span id="pgVer"[^>]*>[^<]*</span>', '<span id="pgVer">Page version 8.1 \u00b7 published ' + now.strftime('%a %-d %b %Y, %H:%M') + ' Israel time</span>', a, count=1)
open(path, 'w', encoding='utf-8').write(a)
print('patched OK')
