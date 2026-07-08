#!/usr/bin/env python3
"""Integrity check for extracted older-conference editions.

For every HTML page in each edition dir, verify that every href/src/url(...)
either resolves to an existing local file (pretty-URL aware) or is an
absolute/external URL. Prints per-edition: pages checked, broken local refs.

Usage: python3 migration-data/verify_older_snapshot.py [slug ...]   (default: all)
"""
import pathlib
import posixpath
import re
import sys
import urllib.parse

from bs4 import BeautifulSoup

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = ROOT / "older-conferences"


def check_edition(ed_dir):
    broken = []
    pages = list(ed_dir.rglob("*.html"))
    for page in pages:
        rel_dir = page.parent
        soup = BeautifulSoup(page.read_text("utf-8", "replace"), "html.parser")
        refs = []
        for tag, attr in (("a", "href"), ("img", "src"), ("script", "src"),
                          ("link", "href"), ("source", "src"),
                          ("embed", "src"), ("object", "data")):
            for el in soup.find_all(tag):
                v = el.get(attr)
                if v:
                    refs.append(v)
        for el in soup.find_all(style=True):
            refs += re.findall(r"url\(\s*['\"]?([^'\")]+)['\"]?\s*\)",
                               el["style"])
        for v in refs:
            v = v.strip()
            if not v or v.startswith(("#", "//")) or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", v):
                # any scheme-qualified ref (incl. original-content quirks like
                # file:///C:\... Word-paste refs and httt:// typos) is source
                # material, not something we rewrote - out of scope
                continue
            path = urllib.parse.unquote(v.split("#")[0].split("?")[0])
            if not path:
                continue
            target = (rel_dir / path).resolve()
            ok = (target.exists() or
                  (target / "index.html").exists() or
                  pathlib.Path(str(target) + "/index.html").exists())
            if not ok:
                broken.append(f"{page.relative_to(ed_dir)} -> {v}")
    return len(pages), broken


def main():
    args = sys.argv[1:]
    base = BASE
    if "--dir" in args:
        i = args.index("--dir")
        base = pathlib.Path(args[i + 1])
        del args[i:i + 2]
    want = args
    dirs = sorted(d for d in base.iterdir()
                  if d.is_dir() and (not want or d.name in want))
    total_broken = 0
    for d in dirs:
        n_pages, broken = check_edition(d)
        total_broken += len(broken)
        status = "OK " if not broken else f"{len(broken)} BROKEN"
        print(f"{d.name:28} {n_pages:4} pages   {status}")
        for b in broken[:10]:
            print(f"    {b}")
        if len(broken) > 10:
            print(f"    ... and {len(broken) - 10} more")
    sys.exit(1 if total_broken else 0)


if __name__ == "__main__":
    main()
