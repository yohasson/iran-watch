"""Apply tools/page_patch.json to index.html.
Footer-proof: any pgVer footer text is ignored. Never fails the job:
- already patched (all replacements present) -> no change, exit 0
- page differs from the tested base (e.g. a newer build was published) -> skip with a notice, exit 0
- otherwise apply, verify the tested result, and stamp the real publish time."""
import hashlib, json, re, sys, datetime, zoneinfo
p = json.load(open(sys.argv[1], encoding='utf-8'))
path = sys.argv[2]
a = open(path, encoding='utf-8').read()
h = lambda s: hashlib.sha256(s.encode('utf-8')).hexdigest()
FOOT = re.compile(r'<span id="pgVer"[^>]*>[^<]*</span>')
norm = lambda s, label: FOOT.sub('<span id="pgVer">' + label + '</span>', s, count=1)
reps = [(o, n) for o, n in p['reps'] if 'pgVer' not in o and 'gVer' not in o]
def note(msg, warn=False):
    print(('::warning::' if warn else '') + msg); sys.exit(0)
if all(n in a for o, n in reps) and not any(o in a and o not in n for o, n in reps):
    note('already patched – nothing to do')
b = norm(a, 'Page version 8 \u00b7 25 Nov 2026')
if h(b) != p['base_sha256']:
    note('page is not the tested base build (a newer page was probably published) – patch skipped, page left as is', True)
for old, new in reversed(p['reps']):
    if b.count(old) != 1:
        note('patch anchor not unique – patch skipped, page left as is', True)
    b = b.replace(old, new)
if h(b) != p['sha256']:
    note('patched result does not match the tested build – patch skipped, page left as is', True)
now = datetime.datetime.now(zoneinfo.ZoneInfo('Asia/Jerusalem'))
b = norm(b, 'Page version 8.1 \u00b7 published ' + now.strftime('%a %-d %b %Y, %H:%M') + ' Israel time')
open(path, 'w', encoding='utf-8').write(b)
print('patched OK')
