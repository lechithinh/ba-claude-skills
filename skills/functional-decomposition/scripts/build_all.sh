#!/bin/sh
# Sinh lại mọi đầu ra của một spec: lint, bảng, Mermaid, SVG, CSV, trang explorer.
#   sh scripts/build_all.sh examples/clinic-booking/spec.json examples/clinic-booking
set -e
SPEC="$1"; OUT="$2"; H="$(dirname "$0")"
[ -n "$SPEC" ] && [ -n "$OUT" ] || { echo "Cách dùng: sh build_all.sh spec.json thu-muc-dau-ra"; exit 2; }
mkdir -p "$OUT"
python3 "$H/fd_lint.py"               "$SPEC" || { echo "Lint có LỖI - sửa spec trước khi giao."; }
python3 "$H/spec_to_table.py"         "$SPEC" "$OUT/hierarchy.md"
python3 "$H/spec_to_mermaid.py"       "$SPEC" "$OUT/diagram.mmd" --split
python3 "$H/spec_to_svg.py"           "$SPEC" "$OUT/diagram.svg"
python3 "$H/spec_to_csv.py"           "$SPEC" "$OUT/tree.csv"
python3 "$H/build_explorer_page.py"   "$SPEC" "$OUT/explorer.html"
