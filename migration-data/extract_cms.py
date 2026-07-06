#!/usr/bin/env python3
"""Snapshot a Sonata-CMS conference page into a self-contained static folder.

Usage:  python3 extract_cms.py <slug> [<slug>...] [--out DIR]

For each slug it fetches https://codesync.global/conferences/<slug>/ and writes
    DIR/<slug>/index.html            cleaned page
    DIR/<slug>/speaker/<x>/index.html  per-speaker pages (bios) linked from it
    DIR/<slug>/media/<x>/index.html    slides pages linked from it
    DIR/<slug>/assets/...            every referenced local asset (speaker
                                     photos, slide PDFs, css, js, fonts)
    DIR/<slug>/REPORT.txt            what was stripped / downloaded / failed

Cleaning rules (per MIGRATION.md: keep speakers + native schedule, drop
registration):
  - remove <script> tags loading eventbrite / analytics / tracking
  - remove elements whose id/class mentions register, ticket, eventbrite,
    newsletter, cookie (logged in REPORT.txt for review)
  - convert lazy-loaded images (data-src / data-bg) to plain src / inline
    style so pages work without the CMS JavaScript
  - download assets referenced from codesync.global (/uploads, /assets,
    /media files, /bundles) incl. slide PDFs; one level of url(...)
    resolution inside downloaded CSS
  - links to this conference's speaker/media pages become relative; other
    codesync.global links stay absolute (the domain persists and will point
    at the new hub)

Constraint: content is never modified, only removed per the rules above; a
failed asset download keeps the original absolute URL and is logged, so
nothing silently disappears.
"""
import re, sys, time, pathlib, urllib.parse, urllib.request
from bs4 import BeautifulSoup

BASE = "https://codesync.global"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}
STRIP_WORDS = ("register", "ticket", "eventbrite", "newsletter", "cookie")
SCRIPT_BLOCKLIST = ("eventbrite", "googletagmanager", "google-analytics",
                    "gtag", "hotjar", "facebook", "fbevents", "twitter",
                    "linkedin.com/px", "doubleclick")
ASSET_PREFIXES = ("/uploads", "/assets", "/bundles", "/build", "/favicon")
SUBPAGE_RE = re.compile(r"^/(speaker/[^/#?]+|media/[^/#?]+)/?$")


def fetch(url, binary=False, retries=3):
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=60) as r:
                data = r.read()
            return data if binary else data.decode("utf-8", "replace")
        except Exception:
            if i == retries - 1:
                raise
            time.sleep(2 * (i + 1))


def asset_path(url):
    """Local relative path for a codesync asset URL, or None."""
    if not url:
        return None
    url = url.strip()
    if url.startswith(("data:", "#")):
        return None
    p = urllib.parse.urlparse(url)
    if p.netloc and "codesync.global" not in p.netloc:
        return None
    if not any(p.path.startswith(x) for x in ASSET_PREFIXES):
        return None
    return p.path.lstrip("/")


def clean_page(soup, report, page_name):
    for s in soup.find_all("script"):
        target = (s.get("src") or "") + (s.string or "")
        if any(w in target.lower() for w in SCRIPT_BLOCKLIST):
            report.append(f"[{page_name}] STRIPPED script: {(s.get('src') or 'inline')[:100]}")
            s.decompose()
    for el in soup.find_all(attrs={"id": True}) + soup.find_all(attrs={"class": True}):
        if not el.parent:          # already decomposed
            continue
        ident = " ".join([el.get("id") or ""] + (el.get("class") or [])).lower()
        if any(w in ident for w in STRIP_WORDS):
            if el.name in ("body", "main", "html"):
                continue
            report.append(f"[{page_name}] STRIPPED <{el.name} id/class='{ident.strip()[:80]}'>")
            el.decompose()
    for a in soup.find_all("a", href=True):
        frag = urllib.parse.urlparse(a["href"]).fragment.lower()
        if frag and any(w in frag for w in STRIP_WORDS):
            report.append(f"[{page_name}] STRIPPED anchor link: {a['href'][:80]}")
            a.decompose()


def rewrite_page(soup, prefix, downloads, subpages, report, page_name):
    """prefix: relative path from this page's dir to the snapshot root."""
    def claim(el, attr):
        local = asset_path(el.get(attr))
        if local:
            downloads[local] = urllib.parse.urljoin(BASE, "/" + local)
            el[attr] = f"{prefix}assets/{local}"

    for img in soup.find_all(["img", "source"]):
        if img.get("data-src"):
            local = asset_path(img["data-src"])
            if local:
                downloads[local] = urllib.parse.urljoin(BASE, "/" + local)
                img["src"] = f"{prefix}assets/{local}"
            else:
                img["src"] = img["data-src"]
            del img["data-src"]
            if img.get("class"):
                img["class"] = [c for c in img["class"] if c != "lazy"]
        else:
            claim(img, "src")
        if img.get("srcset"):
            del img["srcset"]
    for el in soup.find_all(attrs={"data-bg": True}):
        m = re.search(r"url\(['\"]?([^'\")]+)", el["data-bg"])
        u = m.group(1) if m else None
        local = asset_path(u)
        if local:
            downloads[local] = urllib.parse.urljoin(BASE, "/" + local)
            el["style"] = f"background-image:url('{prefix}assets/{local}')"
        elif u:
            el["style"] = f"background-image:url('{u}')"
        del el["data-bg"]
        if el.get("class"):
            el["class"] = [c for c in el["class"] if c != "lazy"]
    for link in soup.find_all("link", href=True):
        claim(link, "href")
    for s in soup.find_all("script", src=True):
        claim(s, "src")
    for v in soup.find_all("video"):
        claim(v, "poster")
    # <a href>: slide PDFs and other uploaded files become local assets;
    # this conference's speaker/media pages become relative links
    external = 0
    for a in soup.find_all("a", href=True):
        href = a["href"]
        p = urllib.parse.urlparse(href)
        if p.netloc and "codesync.global" not in p.netloc:
            continue
        local = asset_path(href)
        if local and "." in local.rsplit("/", 1)[-1]:      # looks like a file
            downloads[local] = urllib.parse.urljoin(BASE, "/" + local)
            a["href"] = f"{prefix}assets/{local}"
            continue
        norm = p.path if p.path.endswith("/") else p.path + "/"
        m = SUBPAGE_RE.match(p.path) or SUBPAGE_RE.match(norm.rstrip("/") and norm[:-1] or norm)
        key = norm.strip("/")
        if key in subpages:
            frag = f"#{p.fragment}" if p.fragment else ""
            a["href"] = f"{prefix}{key}/index.html{frag}"
        elif p.netloc or p.path.startswith("/"):
            external += 1
    if external:
        report.append(f"[{page_name}] {external} codesync.global links left absolute")


def snapshot(slug, outroot):
    out = outroot / slug
    (out / "assets").mkdir(parents=True, exist_ok=True)
    report, downloads = [], {}
    main_html = fetch(f"{BASE}/conferences/{slug}/")
    main = BeautifulSoup(main_html, "html.parser")

    # discover this conference's speaker/media subpages from the raw page
    subpages = {}
    for a in main.find_all("a", href=True):
        p = urllib.parse.urlparse(a["href"])
        if p.netloc and "codesync.global" not in p.netloc:
            continue
        m = SUBPAGE_RE.match(p.path.rstrip("/") or "/")
        if m:
            subpages[m.group(1)] = urllib.parse.urljoin(BASE, "/" + m.group(1) + "/")

    clean_page(main, report, "main")
    rewrite_page(main, "", downloads, subpages, report, "main")
    (out / "index.html").write_text(str(main), "utf-8")

    sub_fail = []
    for key, url in sorted(subpages.items()):
        try:
            soup = BeautifulSoup(fetch(url), "html.parser")
        except Exception as e:
            sub_fail.append(key)
            report.append(f"FAILED subpage {url}: {e}")
            continue
        clean_page(soup, report, key)
        depth = key.count("/") + 1
        rewrite_page(soup, "../" * depth, downloads, subpages, report, key)
        dest = out / key / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(str(soup), "utf-8")

    ok = fail = 0
    css_queue = []
    for local, remote in sorted(downloads.items()):
        dest = out / "assets" / local
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.exists():
            continue
        try:
            data = fetch(remote, binary=True)
            dest.write_bytes(data)
            ok += 1
            if local.endswith(".css"):
                css_queue.append((local, dest))
        except Exception as e:
            fail += 1
            report.append(f"FAILED download {remote}: {e}")
    for local, dest in css_queue:
        css = dest.read_text("utf-8", errors="replace")
        base_dir = "/" + str(pathlib.PurePosixPath(local).parent)
        for m in set(re.findall(r"url\(['\"]?([^'\")]+?)['\"]?\)", css)):
            if m.startswith(("data:", "http")):
                continue
            resolved = urllib.parse.urljoin(base_dir + "/", m.split("?")[0].split("#")[0])
            sub_local = resolved.lstrip("/") if any(
                resolved.startswith(x) for x in ASSET_PREFIXES) else None
            if not sub_local:
                continue
            sub_dest = out / "assets" / sub_local
            sub_dest.parent.mkdir(parents=True, exist_ok=True)
            if not sub_dest.exists():
                try:
                    sub_dest.write_bytes(fetch(urllib.parse.urljoin(BASE, "/" + sub_local), binary=True))
                    ok += 1
                except Exception as e:
                    fail += 1
                    report.append(f"FAILED css asset {sub_local}: {e}")
            depth = len(pathlib.PurePosixPath(local).parent.parts)
            css = css.replace(m, "../" * depth + sub_local)
        dest.write_text(css, "utf-8")

    stripped = len([r for r in report if "STRIPPED" in r])
    report.insert(0, f"{slug}: {len(subpages)} subpages ({len(sub_fail)} failed), "
                     f"{ok} assets downloaded ({fail} failed), {stripped} elements stripped")
    (out / "REPORT.txt").write_text("\n".join(report) + "\n", "utf-8")
    print(report[0])
    return fail == 0 and not sub_fail


if __name__ == "__main__":
    argv = sys.argv[1:]
    if "--out" in argv:
        i = argv.index("--out")
        outdir = pathlib.Path(argv[i + 1])
        argv = argv[:i] + argv[i + 2:]
    else:
        outdir = pathlib.Path(__file__).parent / "snapshots"
    if not argv:
        sys.exit("usage: extract_cms.py <slug> [...] [--out DIR]")
    bad = [s for s in argv if not snapshot(s, outdir)]
    if bad:
        print("with failures:", ", ".join(bad))
