#!/usr/bin/env python3
"""Collect min-entropy figures from 90B output files into a markdown table."""
import re, sys, pathlib
root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "results")
print("| window | mapping | test | H_original | H_bitstring | min-entropy per symbol | IID? |")
print("|---|---|---|---|---|---|---|")
for f in sorted(root.rglob("*_*.txt")):
    if not (f.stem.endswith("_iid") or f.stem.endswith("_non_iid")):
        continue
    t = f.read_text(errors="ignore")
    ho = re.search(r"H_original:\s*([\d.]+)", t); hb = re.search(r"H_bitstring:\s*([\d.]+)", t)
    mn = re.search(r"min\(H_original, \d+ X H_bitstring\):\s*([\d.]+)", t)
    iid = ""
    if "_iid" in f.name and "non_iid" not in f.name:
        iid = "fail" if re.search(r"Failed", t) else ("pass" if t.count("** Passed") >= 3 else "?")
    mapping, test = f.stem.split("_", 1)
    print(f"| {f.parent.name} | {mapping} | {test} | {ho.group(1) if ho else ''} | {hb.group(1) if hb else ''} | {mn.group(1) if mn else ''} | {iid} |")
