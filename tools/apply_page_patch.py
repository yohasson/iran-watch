"""Apply tools/page_patch.json to index.html; publish only if the result matches the tested build exactly."""
import hashlib, json, sys
p = json.load(open(sys.argv[1], encoding='utf-8'))
path = sys.argv[2]
a = open(path, encoding='utf-8').read()
h = lambda s: hashlib.sha256(s.encode('utf-8')).hexdigest()
if h(a) == p['sha256']:
    print('already up to date'); sys.exit(0)
if h(a) != p['base_sha256']:
    print('base mismatch – not applying'); sys.exit(2)
for old, new in reversed(p['reps']):
    if a.count(old) != 1:
        print('anchor not unique – not applying'); sys.exit(3)
    a = a.replace(old, new)
if h(a) != p['sha256']:
    print('result hash mismatch – not applying'); sys.exit(4)
open(path, 'w', encoding='utf-8').write(a)
print('patched OK')
