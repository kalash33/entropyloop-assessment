#!/usr/bin/env bash
# Run NIST SP 800-90B (non-IID + IID check) on prepared symbol files.
# Usage: run_90b.sh /path/to/SP800-90B_EntropyAssessment/cpp PREFIX
set -euo pipefail
EA="$1"; P="$2"; OUT=results
mkdir -p "$OUT"
for v in low8:8 q8:8 high4:4; do
  name=${v%%:*}; bits=${v##*:}
  echo "== $name ($bits bits/symbol) =="
  "$EA/ea_non_iid" -i -a -v "${P}_${name}.bin" "$bits" | tee "$OUT/${name}_non_iid.txt"
  "$EA/ea_iid"     -i -a -v "${P}_${name}.bin" "$bits" | tee "$OUT/${name}_iid.txt"
done
