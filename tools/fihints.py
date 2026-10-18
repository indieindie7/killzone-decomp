# fihints.py <funcinfo.tsv> <hints.txt> : one hint line per function from an ExportFuncInfo TSV
# (F addr name src size / C callee / S string lines under each F): size, callee count, strings.
# Output line: "<addr> size=N calls=N str=\"a\" | \"b\" ..." for injecthints.py.
import sys
out = []
cur = None
calls = 0
strs = []
size = 0


def flush():
    if cur is None:
        return
    s = ' | '.join('"%s"' % t[:48] for t in strs[:8])
    if len(strs) > 8:
        s += ' +%d more' % (len(strs) - 8)
    out.append('%s size=%s calls=%d%s' % (cur, size, calls, (' str=' + s) if strs else ''))


for l in open(sys.argv[1], encoding='utf-8', errors='replace'):
    l = l.rstrip('\r\n')
    p = l.split('\t')
    if len(p) < 2:
        p = l.split(' ', 4) if l.startswith('F ') else l.split(' ', 1)
    if p[0] == 'F':
        flush()
        cur = p[1]
        size = p[4] if len(p) > 4 else '?'
        calls = 0
        strs = []
    elif p[0] == 'C':
        calls += 1
    elif p[0] == 'S':
        t = p[1].strip() if len(p) > 1 else ''
        if len(t) >= 3:
            strs.append(t)
flush()
with open(sys.argv[2], 'w', encoding='utf-8') as w:
    w.write('\n'.join(out) + '\n')
print(len(out), 'hints,', sum(1 for o in out if 'str=' in o), 'with strings')
