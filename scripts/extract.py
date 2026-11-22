#!/usr/bin/env python3
"""Turn EntropyLoop raw dumps (little-endian uint16, 12-bit ADC values) into
SP 800-90B input files (one symbol per byte).

Usage: extract.py RAW_FILE OUT_PREFIX [--offset N] [--count N]
Writes:
  OUT_PREFIX_low8.bin   low 8 bits of each 12-bit sample (bits_per_symbol=8)
  OUT_PREFIX_high4.bin  top 4 bits of each 12-bit sample (bits_per_symbol=4)
  OUT_PREFIX_q8.bin     12-bit sample >> 4, i.e. the 8 most significant bits (bits_per_symbol=8)
  OUT_PREFIX_stats.txt  min, max, mean, out-of-range count
"""
import argparse, struct, sys
import numpy as np

p = argparse.ArgumentParser()
p.add_argument("raw"); p.add_argument("out")
p.add_argument("--offset", type=int, default=0, help="first sample index")
p.add_argument("--count", type=int, default=1_000_000, help="samples to take (>= 1,000,000 for 90B)")
a = p.parse_args()

x = np.fromfile(a.raw, dtype="<u2", count=a.count, offset=a.offset * 2)
if x.size < a.count:
    sys.exit(f"only {x.size} samples read")
bad = int((x > 4095).sum())
x12 = x & 0x0FFF
(x12 & 0xFF).astype(np.uint8).tofile(f"{a.out}_low8.bin")
(x12 >> 8).astype(np.uint8).tofile(f"{a.out}_high4.bin")
(x12 >> 4).astype(np.uint8).tofile(f"{a.out}_q8.bin")
with open(f"{a.out}_stats.txt", "w") as f:
    f.write(f"samples={x.size} offset={a.offset}\nmin={x12.min()} max={x12.max()} "
            f"mean={x12.mean():.2f} std={x12.std():.2f}\nvalues_above_4095={bad}\n"
            f"distinct_12bit_values={np.unique(x12).size}\n")
print(open(f"{a.out}_stats.txt").read())
