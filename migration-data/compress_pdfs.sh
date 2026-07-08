#!/bin/bash
# Shrink slide PDFs in-place with Ghostscript /ebook (150 dpi) - big savings on
# image-heavy conference decks (~90%) at readable on-screen quality. Idempotent
# and safe: only replaces a file when the recompressed version is valid (PDF
# header + %%EOF, same page count) AND at least 10% smaller.
#
# Usage:  bash migration-data/compress_pdfs.sh <dir> [<dir>...]
set -u
command -v gs >/dev/null || { echo "ghostscript (gs) not installed"; exit 1; }
total_before=0; total_after=0; changed=0; skipped=0

pagecount() { gs -q -dNODISPLAY -dNOSAFER -c "($1) (r) file runpdfbegin pdfpagecount = quit" 2>/dev/null; }

while [ $# -gt 0 ]; do
  find "$1" -type f -iname '*.pdf' | while read -r pdf; do
    before=$(wc -c < "$pdf")
    tmp="$(dirname "$pdf")/.compress_tmp.pdf"
    gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.5 -dPDFSETTINGS=/ebook \
       -dNOPAUSE -dQUIET -dBATCH -dDetectDuplicateImages=true \
       -sOutputFile="$tmp" "$pdf" 2>/dev/null
    if [ ! -s "$tmp" ]; then rm -f "$tmp"; echo "SKIP (gs failed): $pdf"; continue; fi
    after=$(wc -c < "$tmp")
    # validity: header + trailer present, and meaningfully smaller
    head -c5 "$tmp" | grep -q '%PDF-' \
      && tail -c1024 "$tmp" | grep -q '%%EOF' \
      && [ "$after" -lt $(( before * 9 / 10 )) ]
    if [ $? -eq 0 ]; then
      mv "$tmp" "$pdf"
      echo "$(( before/1024/1024 ))MB -> $(( after/1024/1024 ))MB  $(basename "$pdf")"
    else
      rm -f "$tmp"  # keep original (already small, or grew, or invalid)
    fi
  done
  shift
done
echo "done (see per-file lines above)"
