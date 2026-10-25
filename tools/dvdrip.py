# dvdrip.py <drive letter> <out.iso>: copy a data DVD sector-by-sector (2048 B) from the raw device.
import sys, time
d, out = sys.argv[1], sys.argv[2]
h = open('\\\\.\\' + d + ':', 'rb', buffering=0)
with open(out, 'wb') as o:
    t = time.time(); n = 0
    while True:
        b = h.read(1 << 20)
        if not b: break
        o.write(b); n += len(b)
        if n % (256 << 20) == 0: print('%d MB %.0fs' % (n >> 20, time.time() - t), flush=True)
print('done', n, 'bytes')
