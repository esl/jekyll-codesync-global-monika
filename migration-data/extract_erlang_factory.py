#!/usr/bin/env python3
"""Extract pre-Sonata erlang-factory.com conference editions into
self-contained static folders for the hub's /older-conferences/ section.

Usage:
    python3 migration-data/extract_erlang_factory.py --list
    python3 migration-data/extract_erlang_factory.py <slug> [<slug>...]
    python3 migration-data/extract_erlang_factory.py --all
    (default --out: <repo>/older-conferences)

Editions come from migration-data/erlang_factory.json (the census).  The two
modern Code BEAM entries are excluded (they belong to their brand repos).
Two modes, chosen per edition:

  LIVE     live_status == 200: crawl the live site (BFS within the edition's
           URL prefix), download assets directly.
  WAYBACK  everything else (403 / never-probed): enumerate the edition's page
           tree from the Wayback CDX index, take the LATEST 200 capture per
           urlkey, fetch original bytes via the `id_` raw-mode URL (no toolbar
           to strip), fetch assets via `id_` too (Wayback redirects to the
           nearest capture of that asset).

Output per edition:  <out>/<slug>/index.html, subpages mirroring the original
path structure (pretty-URL dirs with index.html), assets/ (localized css/js/
images/pdfs, one level of url(...) resolution inside CSS), REPORT.txt.

Rules (mirroring extract_cms.py):
  - content is never modified, only removed per the strip rules (analytics /
    tracking / share-widget scripts, <base> tags); everything logged
  - same-edition links -> relative local paths (matched case-insensitively:
    CDX urlkeys are lowercased and GitHub Pages is case-sensitive)
  - links to erlang-factory.com OUTSIDE the edition -> absolute Wayback URLs
    (the host is dying; in live mode too)
  - a failed asset keeps a Wayback URL and is logged, nothing vanishes silently
  - assets > 50 MB skipped and logged
  - idempotent: existing asset files are skipped, pages are re-fetched (cheap)

A wayback-reconstructed edition gets a provenance comment in every page and a
PARTIAL marker in REPORT.txt when archived coverage is thin.
"""
import json
import pathlib
import posixpath
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

from bs4 import BeautifulSoup

ROOT = pathlib.Path(__file__).resolve().parent.parent
CENSUS = ROOT / "migration-data" / "erlang_factory.json"
DEFAULT_OUT = ROOT / "older-conferences"

HOST = "www.erlang-factory.com"
# External hosts whose assets we DOWNLOAD (not hotlink) - ESL-owned conference
# asset buckets used by the codemesh.io-era sites for speaker photos/logos.
# Per MIGRATION.md, committed assets beat hotlinks to a source that may vanish.
ASSET_HOSTS = {"esl-conf-static.s3.eu-central-1.amazonaws.com",
               "esl-conf-staging.s3.eu-central-1.amazonaws.com",
               "s3.amazonaws.com"}
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (codesync-archive-migration)"}
CDX = "https://web.archive.org/cdx/search/cdx"
WB_RAW = "https://web.archive.org/web/{ts}id_/{url}"   # original bytes
WB_VIEW = "https://web.archive.org/web/{ts}/{url}"     # human view

SCRIPT_BLOCKLIST = ("google-analytics", "googletagmanager", "gtag", "urchin",
                    "_gat", "_gaq", "quantserve", "statcounter", "addthis",
                    "sharethis", "facebook", "fbevents", "twitter",
                    "doubleclick", "scorecardresearch",
                    "www2.erlang-solutions")  # Pardot marketing-form iframes
ASSET_EXT = (".css", ".js", ".png", ".jpg", ".jpeg", ".gif", ".ico", ".svg",
             ".pdf", ".woff", ".woff2", ".ttf", ".eot", ".otf", ".swf",
             ".mp4", ".webp", ".bmp")
MAX_ASSET = 50 * 1024 * 1024
MAX_PAGES = 500

# throttle state
_last_hit = {"wayback": 0.0, "live": 0.0}
_MIN_GAP = {"wayback": 0.7, "live": 0.3}


def throttle(kind):
    gap = time.time() - _last_hit[kind]
    if gap < _MIN_GAP[kind]:
        time.sleep(_MIN_GAP[kind] - gap)
    _last_hit[kind] = time.time()


def fetch(url, kind, retries=4, max_bytes=None):
    """GET url -> bytes. Follows redirects. Raises on final failure."""
    # encode stray spaces/control chars in the path (some original filenames,
    # e.g. "Rich Hickey_tumbnail.jpg", contain raw spaces urllib rejects)
    url = url.replace(" ", "%20")
    for i in range(retries):
        throttle(kind)
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=60) as r:
                if max_bytes:
                    length = r.headers.get("Content-Length")
                    if length and int(length) > max_bytes:
                        raise ValueError(f"too large ({length} bytes)")
                    data = r.read(max_bytes + 1)
                    if len(data) > max_bytes:
                        raise ValueError("too large (streamed)")
                    return data
                return r.read()
        except ValueError:
            raise
        except urllib.error.HTTPError as e:
            if e.code == 404:
                raise
            if e.code in (429, 503):
                time.sleep(120)
            elif i == retries - 1:
                raise
            else:
                time.sleep(5 * (3 ** i))
        except Exception:
            if i == retries - 1:
                raise
            time.sleep(5 * (3 ** i))


# ---------------------------------------------------------------- editions

# Editions whose live page still returns 200 but whose assets are GONE from
# the live server (verified: /assets 404, /<slug>/assets 404) -> reconstruct
# from Wayback instead, which holds the complete healthy site.
FORCE_WAYBACK = {"sfbay_2017", "techmesh_2012"}

# Editions that lived on their own dedicated domain: extract from THAT host's
# Wayback captures instead of erlang-factory.com when the capture is richer.
# sfbay_2017 = erlangelixir.com (site root; live host answers 503 now; its
# Wayback tree has 146 urlkeys vs 77 under erlang-factory.com/sfbay2017).
ALT_SOURCE = {
    "sfbay_2017": {"host": "www.erlangelixir.com", "prefix": "/"},
    # Tech Mesh 2012's live site (gotocon.com) hangs on JSP endpoints and links
    # speakers off to techmeshconf.com, which is now squatter spam. Reconstruct
    # from techmeshconf.com's LEGIT-era Wayback captures (63 speaker pages,
    # 2012-2013); ts_ceiling drops the 2021+ squat snapshots.
    "techmesh_2012": {"host": "techmeshconf.com",
                      "prefix": "/techmesh-london-2012", "ts_ceiling": "2015"},
}

# Per-edition asset remap: some referenced assets are dead at the host in the
# page markup but ALIVE on another (the platform) host. Fetch those live from
# the replacement host and localize. techmesh_2012's speaker headshots are dead
# on techmeshconf.com (squatted) but live on gotocon.com/dl/photos/speakers/.
ASSET_REMAP = {
    "techmesh_2012": {"techmeshconf.com": "gotocon.com"},
}

# Editions whose sites are dynamic apps with meaningful query-string pages
# (e.g. gotocon's show_track.jsp?trackOID=...) - crawl those too. (Tech Mesh
# 2012 is reconstructed from techmeshconf.com Wayback, whose pages are
# path-based - /speaker/Name, /presentation/... - so no query crawl needed.)
QUERY_PAGES = set()

SLUG_OVERRIDES = {
    # /conference/<Slug> path-segment (lowercased) -> local dir name
    "erlanguserconference2009": "euc_2009",
    "erlanguserconference2010": "euc_2010",
    "erlanguserconference2011": "euc_2011",
    "erlanguserconference2012": "euc_2012",
    "erlanguserconference2013": "euc_2013",
    "sfbayareaerlangfactory2009": "sfbay_2009",
    "2009erlangworkshop": "erlang_workshop_2009",
    "testingtutorialworkshop2010": "testing_workshop_2010",
    "erlangfactorylitela": "lite_la_2010",
    "erlangfactorylitemunich": "lite_munich",
    "krakow2010": "lite_krakow_2010",
    "standrews": "lite_standrews_2012",
    "edinburgh": "lite_edinburgh_2011",
    "amsterdam": "lite_amsterdam",
    "brussels": "lite_brussels",
    "paris": "lite_paris_2011",   # year confirmed from archived page body
    "techmesh-london-2012": "techmesh_2012",
}


def edition_slug(seg, year):
    """Local directory name for an edition, from its URL path segment."""
    low = seg.lower()
    if low in SLUG_OVERRIDES:
        return SLUG_OVERRIDES[low]
    m = re.match(r"^([a-z]+?)(\d{4})$", low)
    if m:
        return f"{m.group(1)}_{m.group(2)}"
    if year:
        return f"{low}_{year}"
    return low


def load_editions(census=None):
    """census -> [{name, year, city, url, prefix, slug, mode, host}].
    Host comes from each entry's url (so a census may span domains)."""
    out = []
    for e in json.load(open(census or CENSUS)):
        blob = ((e.get("name") or "") + " " + (e.get("url") or "")).lower()
        if "code beam" in blob or "codebeam" in blob:
            continue  # modern brand, lives in its own repo
        p = urllib.parse.urlparse(e["url"])
        parts = [x for x in p.path.split("/") if x]
        if parts[0] == "conference":
            prefix = f"/conference/{parts[1]}"
            seg = parts[1]
        else:
            prefix = f"/{parts[0]}"          # strip trailing /home
            seg = parts[0]
        slug = edition_slug(seg, e.get("year"))
        mode = "live" if e.get("live_status") == 200 else "wayback"
        if slug in FORCE_WAYBACK:
            mode = "wayback"
        host = p.netloc or HOST
        ts_ceiling = None
        if slug in ALT_SOURCE:
            host = ALT_SOURCE[slug]["host"]
            prefix = ALT_SOURCE[slug]["prefix"]
            ts_ceiling = ALT_SOURCE[slug].get("ts_ceiling")
        out.append({
            "name": e.get("name"), "year": e.get("year"),
            "city": e.get("city"), "url": e["url"], "prefix": prefix,
            "slug": slug, "mode": mode, "host": host, "ts_ceiling": ts_ceiling,
        })
    slugs = [e["slug"] for e in out]
    dupes = {s for s in slugs if slugs.count(s) > 1}
    if dupes:
        sys.exit(f"FATAL: slug collision(s): {dupes}")
    return out


# ------------------------------------------------------------- path mapping

def norm_key(path, query=""):
    """Case-insensitive, slash-normalized lookup key for an original path.
    Query participates in the key so dynamic pages (?trackOID=709) stay
    distinct; editions without query pages always pass query=""."""
    key = posixpath.normpath(urllib.parse.unquote(path)).rstrip("/").lower()
    return f"{key}?{query.lower()}" if query else key


def local_page_path(prefix, orig_path, query=""):
    """Original URL path (+query) -> local file path in the edition dir."""
    rel = posixpath.normpath(urllib.parse.unquote(orig_path)).rstrip("/")
    pfx = posixpath.normpath(prefix)
    if pfx == "/":  # edition lives at a domain root (ALT_SOURCE)
        tail = rel.lstrip("/")
        if not tail and not query:
            return "index.html"
    else:
        if rel.lower() == pfx.lower() and not query:
            return "index.html"
        assert rel.lower().startswith(pfx.lower() + "/"), (rel, pfx)
        tail = rel[len(pfx) + 1:]
    if query:  # dynamic page -> self-describing dir per query variant
        q = re.sub(r"[^A-Za-z0-9]+", "_", urllib.parse.unquote(query)).strip("_")
        tail = f"{tail}__{q}"
    if tail.lower() in ("home", "home/index.html", "index.html", "index.htm"):
        return "index.html"
    tail = re.sub(r"[^A-Za-z0-9/._-]", "_", tail)
    if tail.lower().endswith((".html", ".htm")):
        return tail
    return tail + "/index.html"


def local_asset_path(url, page_hosts=None):
    """Absolute original asset URL -> local path under assets/. Assets from a
    host other than the page's own are namespaced under assets/ext/<host>/ so
    two sources can't collide. (Dir name must NOT start with '_' - Jekyll drops
    '_'-prefixed paths from the build output, 404ing every cross-host asset.)"""
    p = urllib.parse.urlparse(url)
    host = p.netloc.replace(":80", "")
    path = urllib.parse.unquote(p.path).lstrip("/")
    path = re.sub(r"[^A-Za-z0-9/._-]", "_", path) or "asset"
    if p.query:
        h = format(abs(hash(p.query)) % 16 ** 8, "08x")
        stem, dot, ext = path.rpartition(".")
        path = f"{stem}.{h}.{ext}" if dot else f"{path}.{h}"
    if page_hosts and host not in page_hosts:
        safe_host = re.sub(r"[^A-Za-z0-9.-]", "_", host)
        return f"assets/ext/{safe_host}/{path}"
    return "assets/" + path


def relhref(from_local, to_local):
    """Relative href from page file to target file (pretty-URL aware)."""
    src_dir = posixpath.dirname(from_local)
    rel = posixpath.relpath(to_local, src_dir or ".")
    if rel.endswith("/index.html"):
        rel = rel[: -len("index.html")]
    elif rel == "index.html":
        rel = "./"
    return rel


# ------------------------------------------------------------------ wayback

def cdx_pages(host, prefix, ts_ceiling=None):
    """CDX -> {norm_key: (original_url, best_ts)} of archived 200 HTML pages
    under prefix, plus the same map for ALL archived 200 captures (any type).
    ts_ceiling (YYYY or YYYYMMDDhhmmss prefix): ignore captures newer than it -
    needed when a domain was later re-registered by squatters (techmeshconf.com
    turned to spam ~2021), so we keep only the legit-era snapshots."""
    q = urllib.parse.urlencode({
        "url": f"{host}{prefix.rstrip('/')}*", "output": "json",
        "fl": "urlkey,original,timestamp,statuscode,mimetype",
        "filter": "statuscode:200", "limit": "8000",
    })
    data = fetch(f"{CDX}?{q}", "wayback")
    rows = json.loads(data.decode("utf-8", "replace") or "[]")
    best = {}  # urlkey -> (original, ts, mimetype)
    for row in rows[1:]:
        urlkey, original, ts, _st, mime = row
        if ts_ceiling and ts[:len(ts_ceiling)] > ts_ceiling:
            continue  # post-squat capture - skip
        cur = best.get(urlkey)
        if not cur or ts > cur[1]:
            best[urlkey] = (original, ts, mime)
    pages, everything = {}, {}
    for original, ts, mime in best.values():
        p = urllib.parse.urlparse(original)
        if p.query:          # dynamic-app noise (login, print views)
            continue
        key = norm_key(p.path)
        everything[key] = (original, ts)
        looks_html = (mime in ("text/html", "unk", "warc/revisit")
                      and not p.path.lower().endswith(ASSET_EXT))
        if looks_html:
            pages[key] = (original, ts)
    return pages, everything


# ----------------------------------------------------------- page rewriting

def strip_junk(soup, report, page_name):
    for tag in soup.find_all("base"):
        report.append(f"[{page_name}] STRIPPED <base href>")
        tag.decompose()
    for s in soup.find_all("script"):
        target = ((s.get("src") or "") + (s.string or "")).lower()
        if any(w in target for w in SCRIPT_BLOCKLIST):
            report.append(f"[{page_name}] STRIPPED script: "
                          f"{(s.get('src') or 'inline')[:100]}")
            s.decompose()
    for f in soup.find_all("iframe"):
        src = (f.get("src") or "").lower()
        if any(w in src for w in SCRIPT_BLOCKLIST):
            report.append(f"[{page_name}] STRIPPED iframe: {src[:100]}")
            f.decompose()


def rewrite_page(soup, ed, page_local, page_map, assets, report, wb_ts,
                 page_url):
    """Rewrite links/asset refs in one page. Mutates soup; fills assets dict
    {abs_url: local_path}. Relative refs resolve against page_url (the page's
    own original URL) exactly as a browser would - NOT against the edition
    prefix (pages served without a trailing slash resolve to their parent)."""
    pfx_low = posixpath.normpath(ed["prefix"]).lower()
    page_hosts = {ed["host"], ed["host"].replace("www.", "")}
    family_hosts = page_hosts | {HOST, HOST.replace("www.", "")}
    dl_hosts = page_hosts | ASSET_HOSTS  # hosts whose assets we localize

    def absolutize(val):
        return urllib.parse.urljoin(page_url, val.strip())

    def handle_asset(el, attr):
        val = el.get(attr)
        if not val or val.startswith(("data:", "#", "mailto:", "javascript:")):
            return
        absu = absolutize(val)
        p = urllib.parse.urlparse(absu)
        if p.netloc.replace(":80", "") not in dl_hosts:
            return  # external CDN (dead googlecode shim, placehold.it) - keep
        local = assets.setdefault(absu.split("#")[0],
                                  local_asset_path(absu, page_hosts))
        el[attr] = relhref(page_local, local)

    # assets first
    for tag, attr in (("img", "src"), ("script", "src"),
                      ("link", "href"), ("source", "src"),
                      ("embed", "src"), ("object", "data"),
                      ("input", "src")):
        for el in soup.find_all(tag):
            if tag == "link":
                rels = " ".join(el.get("rel") or []).lower()
                if rels and "stylesheet" not in rels and "icon" not in rels:
                    continue
            handle_asset(el, attr)
    # inline style url(...)
    for el in soup.find_all(style=True):
        el["style"] = re.sub(
            r"url\(\s*['\"]?([^'\")]+)['\"]?\s*\)",
            lambda m: "url(%s)" % _css_url(m.group(1), page_local,
                                           absolutize, assets, page_hosts),
            el["style"])

    # now <a href>
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if href.startswith(("#", "mailto:", "javascript:")):
            continue
        absu = absolutize(href)
        p = urllib.parse.urlparse(absu)
        host = p.netloc.replace(":80", "")
        is_asset = p.path.lower().split("#")[0].endswith(ASSET_EXT)
        # a link straight to a downloadable asset (e.g. slide PDF on S3) -> localize
        if is_asset and host in dl_hosts:
            local = assets.setdefault(absu.split("#")[0],
                                      local_asset_path(absu, page_hosts))
            a["href"] = relhref(page_local, local)
            continue
        if host not in family_hosts:
            continue  # genuinely external - keep
        frag = ("#" + p.fragment) if p.fragment else ""
        key = norm_key(p.path, p.query if ed["slug"] in QUERY_PAGES else "")
        if host in page_hosts and key.startswith(pfx_low):
            hit = page_map.get(key)
            if hit:
                a["href"] = relhref(page_local, hit) + frag
                continue
            report.append(f"[{page_local}] MISSING subpage (-> wayback): "
                          f"{p.path}")
        # off-edition or missing -> wayback absolute
        a["href"] = WB_VIEW.format(ts=wb_ts, url=absu) + frag


def _css_url(raw, page_local, absolutize, assets, page_hosts):
    raw = raw.strip()
    if raw.startswith(("data:", "#")):
        return raw
    absu = absolutize(raw)
    p = urllib.parse.urlparse(absu)
    if p.netloc.replace(":80", "") not in page_hosts:
        return raw
    local = assets.setdefault(absu.split("#")[0], local_asset_path(absu))
    return relhref(page_local, local)


def localize_css(data, css_local, css_orig_url, assets, page_hosts):
    """One level of url(...) inside downloaded CSS -> queue + rewrite."""
    text = data.decode("utf-8", "replace")

    def repl(m):
        raw = m.group(1).strip().strip("'\"")
        if raw.startswith(("data:", "#")):
            return m.group(0)
        absu = urllib.parse.urljoin(css_orig_url, raw)
        p = urllib.parse.urlparse(absu)
        if p.netloc.replace(":80", "") not in page_hosts:
            return m.group(0)
        local = assets.setdefault(absu.split("#")[0], local_asset_path(absu))
        return "url(%s)" % posixpath.relpath(local,
                                             posixpath.dirname(css_local))
    return re.sub(r"url\(\s*([^)]+?)\s*\)", repl, text).encode("utf-8")


# ---------------------------------------------------------------- extraction

def snapshot(ed, outroot):
    outdir = outroot / ed["slug"]
    outdir.mkdir(parents=True, exist_ok=True)
    report = [f"edition: {ed['name'] or ed['slug']}",
              f"source:  {ed['url']}  (mode: {ed['mode']})",
              f"date:    {time.strftime('%Y-%m-%d %H:%M')}", ""]
    t0 = time.time()

    if ed["mode"] == "wayback":
        pages, everything = cdx_pages(ed["host"], ed["prefix"],
                                      ed.get("ts_ceiling"))
        if not pages:
            report.append("PARTIAL: no archived HTML pages found in CDX")
            (outdir / "REPORT.txt").write_text("\n".join(report), "utf-8")
            return {"slug": ed["slug"], "pages": 0, "assets": 0,
                    "missing": 0, "partial": True}
        fetch_page = lambda orig, ts: fetch(WB_RAW.format(ts=ts, url=orig),
                                            "wayback")
        # asset fetch: nearest capture around the root page's timestamp
        root_ts = next((ts for k, (o, ts) in pages.items()
                        if local_page_path(ed["prefix"],
                                           urllib.parse.urlparse(o).path)
                        == "index.html"), None) \
            or max(ts for _o, ts in pages.values())
        remap = ASSET_REMAP.get(ed["slug"], {})

        def fetch_asset(url, _rt=root_ts, _remap=remap):
            host = urllib.parse.urlparse(url).netloc.replace(":80", "")
            if host in _remap:  # try the live platform host first
                live = url.replace(host, _remap[host], 1)
                if not live.startswith("http"):
                    live = "http://" + live
                try:
                    return fetch(live, "live", max_bytes=MAX_ASSET)
                except Exception:
                    pass  # fall through to wayback of the original
            return fetch(WB_RAW.format(ts=_rt, url=url), "wayback",
                         max_bytes=MAX_ASSET)
        wb_ts = root_ts
        page_items = sorted(pages.items())[:MAX_PAGES]
        if len(pages) > MAX_PAGES:
            report.append(f"CAPPED: {len(pages)} archived pages, "
                          f"kept first {MAX_PAGES}")
    else:
        # LIVE: BFS within prefix
        wb_ts = "2019"  # for off-edition wayback rewrites: healthy-site era
        fetch_page = lambda orig, ts: fetch(orig, "live")
        fetch_asset = lambda url: fetch(url, "live", max_bytes=MAX_ASSET)
        page_items = None  # discovered below

    # --- collect raw pages ---------------------------------------------
    raw = {}          # norm_key -> (original_url, bytes)
    if ed["mode"] == "wayback":
        for key, (orig, ts) in page_items:
            try:
                raw[key] = (orig, fetch_page(orig, ts))
            except Exception as ex:
                report.append(f"FAILED page {orig}: {ex}")
    else:
        seen, queue = set(), [ed["url"], f"http://{ed['host']}{ed['prefix']}"]
        pfx_low = posixpath.normpath(ed["prefix"]).lower()
        bfs_hosts = {ed["host"], ed["host"].replace("www.", "")}
        allow_query = ed["slug"] in QUERY_PAGES
        while queue and len(raw) < MAX_PAGES:
            url = queue.pop(0)
            pu = urllib.parse.urlparse(url)
            key = norm_key(pu.path, pu.query if allow_query else "")
            if key in seen:
                continue
            seen.add(key)
            try:
                data = fetch_page(url, None)
            except Exception as ex:
                report.append(f"FAILED page {url}: {ex}")
                continue
            raw[key] = (url, data)
            soup = BeautifulSoup(data, "html.parser")
            for a in soup.find_all("a", href=True):
                absu = urllib.parse.urljoin(url, a["href"].split("#")[0])
                p = urllib.parse.urlparse(absu)
                if p.netloc.replace(":80", "") not in bfs_hosts:
                    continue
                k2 = norm_key(p.path, p.query if allow_query else "")
                if k2.startswith(pfx_low) and k2 not in seen \
                        and not p.path.lower().endswith(ASSET_EXT) \
                        and (not p.query or allow_query):
                    queue.append(absu)

    # --- map pages to local paths ---------------------------------------
    page_map = {}
    for key, (orig, _d) in raw.items():
        po = urllib.parse.urlparse(orig)
        try:
            page_map[key] = local_page_path(
                ed["prefix"], po.path,
                po.query if ed["slug"] in QUERY_PAGES else "")
        except AssertionError:
            report.append(f"SKIPPED out-of-prefix page: {po.path}")
    # live mode: alias bare prefix and /home to index
    page_map[norm_key(ed["prefix"])] = "index.html"
    page_map[norm_key(ed["prefix"] + "/home")] = "index.html"

    # --- rewrite + write pages ------------------------------------------
    assets = {}
    n_pages = 0
    for key, (orig, data) in raw.items():
        local = page_map.get(key)
        if not local:
            continue
        soup = BeautifulSoup(data, "html.parser")
        strip_junk(soup, report, local)
        # wayback mode: extensionless page paths on these old servers were
        # directories (redirect-to-slash) - the CDX asset locations prove it -
        # so relative refs resolve against <path>/ (root-relative refs, the
        # overwhelming majority, are unaffected either way)
        base_url = orig
        if ed["mode"] == "wayback":
            last_seg = urllib.parse.urlparse(orig).path.rsplit("/", 1)[-1]
            if last_seg and "." not in last_seg:
                base_url = orig.rstrip("/") + "/"
        rewrite_page(soup, ed, local, page_map, assets, report, wb_ts,
                     base_url)
        if ed["mode"] == "wayback" and soup.html:
            soup.html.insert(0, BeautifulSoup(
                f"<!-- Reconstructed from Wayback Machine captures of {orig} "
                f"(codesync.global migration, {time.strftime('%Y-%m-%d')}) -->",
                "html.parser"))
        dest = outdir / local
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(str(soup), "utf-8")
        n_pages += 1

    # --- download assets (skip existing = resumable) ---------------------
    n_assets, n_missing = 0, 0
    css_todo = []
    for absu, local in sorted(assets.items()):
        dest = outdir / local
        if dest.exists():
            n_assets += 1
            if local.endswith(".css"):
                css_todo.append((absu, local))
            continue
        try:
            data = fetch_asset(absu)
        except Exception as ex:
            n_missing += 1
            report.append(f"MISSING asset {absu}: {ex}")
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        if local.endswith(".css"):
            data = localize_css(data, local, absu, assets,
                                {ed["host"], ed["host"].replace("www.", "")})
            css_todo.append((absu, None))  # url() targets appended to assets
        dest.write_bytes(data)
        n_assets += 1
    # second pass: assets discovered inside CSS
    for absu, local in sorted(assets.items()):
        dest = outdir / local
        if dest.exists():
            continue
        try:
            data = fetch_asset(absu)
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
            n_assets += 1
        except Exception as ex:
            n_missing += 1
            report.append(f"MISSING asset (css) {absu}: {ex}")

    # repair pass: refs to assets that failed to download would be broken
    # local paths -> point them at Wayback instead (nothing vanishes silently)
    failed = {absu: local for absu, local in assets.items()
              if not (outdir / local).exists()}
    if failed:
        for page_local in set(page_map.values()):
            f = outdir / page_local
            if not f.exists():
                continue
            text = f.read_text("utf-8", "replace")
            orig = text
            for absu, local in failed.items():
                rel = relhref(page_local, local)
                text = text.replace(rel, WB_VIEW.format(ts=wb_ts, url=absu))
            if text != orig:
                f.write_text(text, "utf-8")
        report.append(f"REWROTE {len(failed)} never-archived asset ref(s) "
                      f"to Wayback URLs")

    partial = n_pages <= 1 or (ed["mode"] == "wayback" and n_missing > n_assets)
    report.insert(3, f"pages: {n_pages}   assets: {n_assets}   "
                     f"missing: {n_missing}   "
                     f"elapsed: {int(time.time() - t0)}s"
                     + ("   ** PARTIAL **" if partial else ""))
    seen_lines = set()
    report = [ln for ln in report
              if not (ln in seen_lines or seen_lines.add(ln))]
    (outdir / "REPORT.txt").write_text("\n".join(report) + "\n", "utf-8")
    return {"slug": ed["slug"], "pages": n_pages, "assets": n_assets,
            "missing": n_missing, "partial": partial}


# --------------------------------------------------------------------- main

def main():
    args = [a for a in sys.argv[1:]]
    out = DEFAULT_OUT
    if "--out" in args:
        i = args.index("--out")
        out = pathlib.Path(args[i + 1])
        del args[i:i + 2]
    census = None
    if "--census" in args:
        i = args.index("--census")
        census = args[i + 1]
        del args[i:i + 2]
    editions = load_editions(census)
    if "--list" in args:
        for e in editions:
            print(f"{e['slug']:28} {e['mode']:8} {e['prefix']:44} "
                  f"{e['name'] or ''}")
        print(f"\n{len(editions)} editions "
              f"({sum(1 for e in editions if e['mode'] == 'live')} live, "
              f"{sum(1 for e in editions if e['mode'] == 'wayback')} wayback)")
        return
    if "--all" in args:
        todo = editions
    else:
        want = set(args)
        todo = [e for e in editions if e["slug"] in want]
        missing = want - {e["slug"] for e in todo}
        if missing:
            sys.exit(f"unknown slug(s): {missing} (use --list)")
        if not todo:
            sys.exit("nothing to do (pass slugs, --all, or --list)")
    results = []
    for i, e in enumerate(todo, 1):
        print(f"[{i}/{len(todo)}] {e['slug']} ({e['mode']}) ...", flush=True)
        try:
            r = snapshot(e, out)
        except Exception as ex:
            r = {"slug": e["slug"], "error": str(ex)}
            print(f"    ERROR: {ex}", flush=True)
        results.append(r)
        print(f"    {r}", flush=True)
    # merge into any existing summary (targeted re-runs must not clobber it)
    summary_file = out / "_extract_summary.json"
    merged = {}
    if summary_file.exists():
        merged = {r["slug"]: r for r in json.loads(summary_file.read_text())}
    merged.update({r["slug"]: r for r in results})
    summary_file.write_text(json.dumps(list(merged.values()), indent=2),
                            "utf-8")
    bad = [r for r in results if r.get("error")]
    print(f"\ndone: {len(results)} editions, {len(bad)} errored")
    if bad:
        sys.exit(1)


if __name__ == "__main__":
    main()
