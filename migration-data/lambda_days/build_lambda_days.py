#!/usr/bin/env python3
"""
build_lambda_days.py -- mirror lambdadays.org editions into a self-contained
static site hostable on GitHub Pages (esl/lambda-days), matching how the other
retired brands were migrated.

PURPOSE
    Capture every live Lambda Days edition (/lambdadays<year>, 2014-2025) as a
    faithful static archive: real content (already server-rendered), all local
    /static assets, and S3-hosted images downloaded and localized so the archive
    survives the source site and its S3 bucket being retired.

PHASES (idempotent / resumable -- re-running skips work already done)
    crawl   fetch each edition's raw HTML into mirror/pages/<year>.html
    build   rewrite asset/link URLs, download every referenced asset into site/,
            emit site/lambdadays<year>/index.html + a root archive index
    (default: run both)

LAYOUT
    mirror/pages/<year>.html     raw fetched HTML (re-run build without re-fetch)
    site/                        final static site == future repo root, also the
                                 asset cache (an asset already on disk is skipped)
    site/lambdadays<year>/index.html
    site/static/...              local assets (mirrors source /static paths)
    site/static/s3/...           downloaded S3 images
    site/static/vendor/...       downloaded 3rd-party libs (jquery)

RULES
    - Never invent content. Only mirror what the source serves.
    - Keep original root-absolute /static paths (correct once served at the
      lambdadays.org apex via CNAME; local verify serves site/ at root too).
    - Strip tracking / popup scripts (GTM, GetResponse) and CMS edit-mode
      (/admin_page_elements/edit_block/...) artifacts, recovering the real URL.
    - Leave genuine external links (YouTube, sponsors, socials) absolute.
    - On a dead/unreachable asset: log it, leave the reference, never fail the run.
"""
import os
import re
import sys
import time
import json
import http.client
import unicodedata
import urllib.parse
import urllib.request
import urllib.error

BASE = "https://www.lambdadays.org"
YEARS = list(range(2014, 2026))  # 2014..2025 inclusive (2013 and 2026 serve no content)
HERE = os.path.dirname(os.path.abspath(__file__))
MIRROR = os.path.join(HERE, "mirror")
PAGES = os.path.join(MIRROR, "pages")
SITE = os.path.join(HERE, "site")

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) lambda-days-archive/1.0"

# Third-party hosts whose scripts we STRIP (tracking / popups / analytics).
STRIP_SCRIPT_HOSTS = (
    "googletagmanager.com",
    "google-analytics.com",
    "gr-cdn.com",          # GetResponse popups
    "getresponse",
)

report = {"assets_ok": [], "assets_dead": [], "stripped_scripts": [], "pages": {}}


def log(msg):
    print(msg, flush=True)


# Some source landing pages link speaker pages with diacritics *dropped*
# (e.g. "Jerzy Muller" -> jerzy-mller, 404) while the real page uses proper
# transliteration (jerzy-muller). We recover the real slug from the link's
# display name. SUB_NAMES: mangled path -> display name; SLUG_FIX: mangled -> real.
SPECIAL = {"ł": "l", "Ł": "L", "đ": "d", "Đ": "D", "ø": "o", "Ø": "O",
           "ß": "ss", "æ": "ae", "œ": "oe", "ð": "d", "þ": "th"}
SUB_NAMES = {}
SLUG_FIX = {}


def slugify(name):
    s = "".join(SPECIAL.get(c, c) for c in name)
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def fetch(url, tries=4):
    """Return (bytes, content_type) or (None, None) on failure after retries."""
    # malformed source URLs (stray spaces/control chars) can't be fetched -- skip.
    if url != url.strip() or any(c in url for c in " \t\r\n"):
        log("    ! malformed url, skipped: %r" % url)
        return None, None
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=45) as r:
                return r.read(), r.headers.get_content_type()
        except urllib.error.HTTPError as e:
            # definitive: don't retry a missing/forbidden/gone resource
            if e.code in (404, 403, 410, 401):
                log("    ! dead (%d): %s" % (e.code, url))
                return None, None
            last = e
            time.sleep(1.5 * (i + 1))
        except (urllib.error.URLError, TimeoutError, OSError,
                http.client.HTTPException, ValueError, UnicodeError) as e:
            last = e
            time.sleep(1.5 * (i + 1))
    log("    ! fetch failed: %s (%s)" % (url, last))
    return None, None


# ---------------------------------------------------------------------------
# crawl phase
# ---------------------------------------------------------------------------
def crawl():
    os.makedirs(PAGES, exist_ok=True)
    for y in YEARS:
        dest = os.path.join(PAGES, "%d.html" % y)
        if os.path.exists(dest) and os.path.getsize(dest) > 1000:
            log("  = %d already fetched (%d bytes)" % (y, os.path.getsize(dest)))
            continue
        url = "%s/lambdadays%d" % (BASE, y)
        log("  > fetching %s" % url)
        data, _ = fetch(url)
        if not data:
            log("    ! SKIPPED %d (no data)" % y)
            continue
        with open(dest, "wb") as f:
            f.write(data)
        log("    saved %d bytes" % len(data))
        time.sleep(0.5)


# ---------------------------------------------------------------------------
# build phase -- URL localization
# ---------------------------------------------------------------------------
def local_path_for(url):
    """
    Map a remote asset URL to a site-relative path (rooted at '/'), or return
    None to leave the URL untouched (genuine external link).
    """
    p = urllib.parse.urlparse(url)
    host = p.netloc.lower()
    path = p.path

    # protocol-relative and absolute lambdadays.org /static
    if (host in ("", "www.lambdadays.org", "lambdadays.org")) and path.startswith("/static/"):
        return path  # keep as-is; download to site<path>
    # root-relative /static already handled by caller; here handle S3
    if "lambdadays-prod" in host or (host == "s3.amazonaws.com" and path.startswith("/lambdadays-prod")):
        # normalize both S3 URL shapes to a single local tree
        sub = path
        if host == "s3.amazonaws.com":
            sub = path[len("/lambdadays-prod"):]
        return "/static/s3" + sub
    # jquery on googleapis -> vendor
    if "ajax.googleapis.com" in host and path.endswith(".js"):
        return "/static/vendor/" + os.path.basename(path)
    return None


def abs_url(ref, host_default="https://www.lambdadays.org"):
    if ref.startswith("//"):
        return "https:" + ref
    if ref.startswith("/"):
        return host_default + ref
    if ref.startswith("http"):
        return ref
    return None


_result_cache = {}  # remote_url -> local_rel (success) or None (dead)


def download_to_site(remote_url, local_rel):
    """Download remote_url and return the href to reference it by, or None.

    Encoding-consistent: the file is written under the DECODED path (what an HTTP
    server resolves a request to) and the returned href is that path re-ENCODED,
    so assets whose names contain spaces/parens/plus (e.g. S3 slide decks,
    'CODE SYNC LOGO (RGB).png') resolve correctly when served."""
    decoded = urllib.parse.unquote(local_rel)
    href = urllib.parse.quote(decoded, safe="/")
    dest = os.path.join(SITE, decoded.lstrip("/"))
    if os.path.exists(dest) and os.path.getsize(dest) > 0:
        return href
    if remote_url in _result_cache:
        return _result_cache[remote_url]  # honest cache: None stays None
    data, _ = fetch(remote_url)
    if data is None:
        report["assets_dead"].append(remote_url)
        _result_cache[remote_url] = None
        return None
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "wb") as f:
        f.write(data)
    report["assets_ok"].append(decoded)
    _result_cache[remote_url] = href
    return href


def local_target(remote):
    """Given an absolute URL, return the site-relative path we should host it at,
    or None to leave it as a genuine external link."""
    lp = local_path_for(remote)
    if lp:
        return lp
    pr = urllib.parse.urlparse(remote)
    if pr.path.startswith("/static/") and "lambdadays" in pr.netloc:
        return pr.path
    return None


CSS_URL_RE = re.compile(r"url\(\s*['\"]?([^'\")]+)['\"]?\s*\)")


def localize_css_text(text, source_url):
    """Download every url(...) asset referenced in a CSS string (external file,
    inline style attr, or <style> block) and rewrite it to a local path.
    Returns the possibly-modified string. Resolves relative refs vs source_url."""
    out = text
    for raw in set(CSS_URL_RE.findall(text)):
        ref = raw.strip()
        if not ref or ref.startswith(("data:", "#")):
            continue
        remote = urllib.parse.urljoin(source_url, ref)
        pr = urllib.parse.urlparse(remote)
        lp = local_target(remote) or (pr.path if "lambdadays" in pr.netloc else None)
        if not lp:
            continue
        if download_to_site(remote, lp):
            for pat in ("url(%s)" % raw, "url('%s')" % raw, 'url("%s")' % raw):
                out = out.replace(pat, "url(%s)" % lp)
    return out


def process_css(local_rel, source_url):
    """Download url(...) refs inside a downloaded CSS file and rewrite them."""
    dest = os.path.join(SITE, local_rel.lstrip("/"))
    if not os.path.exists(dest):
        return
    try:
        css = open(dest, "r", encoding="utf-8", errors="replace").read()
    except OSError:
        return
    new = localize_css_text(css, source_url)
    if new != css:
        with open(dest, "w", encoding="utf-8") as f:
            f.write(new)


ADMIN_RE = re.compile(r"^/admin_page_elements/edit_block/page_element-\d+/(.*)$")


def fix_admin_href(href):
    """Recover the real URL mangled by CMS edit-mode links."""
    m = ADMIN_RE.match(href)
    if not m:
        return href
    real = m.group(1)
    # CMS collapsed https:// -> https:/
    real = re.sub(r"^(https?):/(?!/)", r"\1://", real)
    return real


def localize(soup, page_url, label):
    """Strip trackers, download + rewrite every asset/doc under our control.
    Returns the set of /static/*.htm legacy sub-pages linked from this page."""
    # 1. strip tracking / popup scripts
    for s in soup.find_all("script"):
        src_attr = s.get("src", "") or ""
        body = s.string or ""
        if any(h in src_attr.lower() for h in STRIP_SCRIPT_HOSTS) or \
           any(h in body.lower() for h in STRIP_SCRIPT_HOSTS) or \
           "gtag(" in body or "GTM-" in body or "dataLayer" in body:
            report["stripped_scripts"].append("%s:%s" % (label, src_attr or "inline"))
            s.decompose()

    # 2. localize asset-bearing attributes
    for tag, attr in (("img", "src"), ("script", "src"), ("link", "href"),
                      ("source", "src"), ("img", "data-src")):
        for el in soup.find_all(tag):
            ref = el.get(attr)
            if not ref or ref.startswith(("data:", "#", "mailto:", "javascript:")):
                continue
            remote = urllib.parse.urljoin(page_url, ref)
            lp = local_target(remote)
            if not lp:
                continue
            got = download_to_site(remote, lp)
            if got:
                el[attr] = got
                if got.endswith(".css"):
                    process_css(got, remote)

    # 2b. backgrounds set via inline style="...url()..." (speaker photos, logos,
    #     venue/section backgrounds) and via embedded <style> blocks.
    for el in soup.find_all(style=True):
        if "url(" in el["style"]:
            el["style"] = localize_css_text(el["style"], page_url)
    for st in soup.find_all("style"):
        if st.string and "url(" in st.string:
            st.string.replace_with(localize_css_text(st.string, page_url))

    # 3. hrefs: fix CMS edit-mode, download /static docs, normalize + collect
    #    edition landing / detail (speaker & talk) sub-pages.
    legacy_htm = set()     # /static/*.htm microsites
    edition_subs = set()   # /lambdadays<year>/<slug> detail pages (no trailing slash)
    for a in soup.find_all("a", href=True):
        a["href"] = fix_admin_href(a["href"])
        href = a["href"]
        if href.startswith(("#", "mailto:", "tel:", "javascript:")):
            continue
        remote = urllib.parse.urljoin(page_url, href)
        pr = urllib.parse.urlparse(remote)
        if pr.netloc and "lambdadays" not in pr.netloc:
            continue  # genuine external link, leave untouched
        path = pr.path
        if any(c in path for c in " \t\r\n"):
            continue  # malformed source link (stray whitespace) -- leave as-is
        anchor = ("#" + pr.fragment) if pr.fragment else ""
        if path.startswith("/static/"):
            if path.lower().endswith((".htm", ".html")):
                legacy_htm.add(path)               # served in place from /static/
            else:
                got = download_to_site(BASE + path, path)  # pdf, doc, etc.
                if got:
                    a["href"] = got
            continue
        m = re.match(r"^/lambdadays(\d{4})(?:/([^?]*))?$", path)
        if m:
            year, tail = m.group(1), (m.group(2) or "").rstrip("/")
            if not tail:                            # edition landing
                a["href"] = "/lambdadays%s/%s" % (year, anchor)
            elif re.search(r"\.[a-z0-9]{2,5}$", tail, re.I):  # a file under the edition
                got = download_to_site(BASE + path, "/lambdadays%s/%s" % (year, tail))
                if got:
                    a["href"] = got
            else:                                   # speaker / talk detail page
                sub = "/lambdadays%s/%s" % (year, tail)
                edition_subs.add(sub)
                name = a.get_text().strip()
                if name and sub not in SUB_NAMES:
                    SUB_NAMES[sub] = name
                a["href"] = "/lambdadays%s/%s/%s" % (year, tail, anchor)
    return legacy_htm, edition_subs


def get_sub_raw(path):
    """Cached fetch of an edition detail page. Returns HTML text or None."""
    cache = os.path.join(MIRROR, "sub", path.lstrip("/") + ".html")
    if os.path.exists(cache) and os.path.getsize(cache) > 400:
        return open(cache, encoding="utf-8", errors="replace").read()
    data, _ = fetch(BASE + path)
    if data is None:
        return None
    os.makedirs(os.path.dirname(cache), exist_ok=True)
    with open(cache, "wb") as f:
        f.write(data)
    return data.decode("utf-8", "replace")


def crawl_subpages(seed, BeautifulSoup):
    """BFS over /lambdadays<year>/<slug> detail pages, discovering deeper links
    (speaker->talk, 'other speakers') until the set closes."""
    done, queue = set(), list(seed)
    while queue:
        path = queue.pop()
        if path in done:
            continue
        done.add(path)
        raw = get_sub_raw(path)
        real = path
        if raw is None:
            # source landing may link a diacritic-stripped slug; recover the real
            # slug by transliterating the speaker's display name and retrying.
            name = SUB_NAMES.get(path)
            year = path.split("/")[1].replace("lambdadays", "")
            alt = "/lambdadays%s/%s" % (year, slugify(name)) if name else None
            if alt and alt != path:
                alt_built = alt in done or os.path.exists(
                    os.path.join(SITE, alt.lstrip("/"), "index.html"))
                if alt_built:
                    SLUG_FIX[path] = alt   # real page already captured elsewhere
                    log("    ~ slug fix: %s -> %s (already built)" % (path, alt))
                    continue
                raw = get_sub_raw(alt)
                if raw is not None:
                    SLUG_FIX[path] = alt
                    real = alt
                    done.add(alt)
                    log("    ~ slug fix: %s -> %s" % (path, alt))
            if raw is None:
                report["assets_dead"].append(BASE + path)
                continue
        soup = BeautifulSoup(raw, "html.parser")
        _, more = localize(soup, BASE + real, real.strip("/"))
        dest = os.path.join(SITE, real.lstrip("/"), "index.html")
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "w", encoding="utf-8") as f:
            f.write(str(soup))
        report.setdefault("subpages", []).append(real)
        for d in more:
            if d not in done:
                queue.append(d)
        n = len(report["subpages"])
        if n % 25 == 0:
            log("    ... %d detail pages built" % n)
    log("    built %d edition detail pages" % len(report.get("subpages", [])))


def build():
    from bs4 import BeautifulSoup

    os.makedirs(SITE, exist_ok=True)
    legacy, edition_subs = set(), set()
    for y in YEARS:
        src = os.path.join(PAGES, "%d.html" % y)
        if not os.path.exists(src):
            log("  ! no mirror for %d, skipping build" % y)
            continue
        log("  building lambdadays%d ..." % y)
        soup = BeautifulSoup(open(src, encoding="utf-8", errors="replace").read(), "html.parser")
        lg, es = localize(soup, "%s/lambdadays%d" % (BASE, y), str(y))
        legacy |= lg
        edition_subs |= es
        outdir = os.path.join(SITE, "lambdadays%d" % y)
        os.makedirs(outdir, exist_ok=True)
        with open(os.path.join(outdir, "index.html"), "w", encoding="utf-8") as f:
            f.write(str(soup))
        report["pages"][y] = "lambdadays%d/index.html" % y
        log("    wrote lambdadays%d/index.html" % y)

    # edition detail pages: speaker bios + talk details (the bulk of the content)
    log("  crawling %d+ edition detail pages ..." % len(edition_subs))
    crawl_subpages(edition_subs, BeautifulSoup)

    # legacy /static/*.htm microsites (early editions), one level deep
    done = set()
    for path in sorted(legacy):
        if path in done:
            continue
        done.add(path)
        remote = BASE + path
        log("  building legacy %s ..." % path)
        data, _ = fetch(remote)
        if data is None:
            report["assets_dead"].append(remote)
            continue
        soup = BeautifulSoup(data, "html.parser")
        deeper, _ = localize(soup, remote, path)
        dest = os.path.join(SITE, path.lstrip("/"))
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "w", encoding="utf-8") as f:
            f.write(str(soup))
        report.setdefault("legacy_pages", []).append(path)
        for d in deeper - done:
            report.setdefault("legacy_unrecursed", []).append(d)

    # rewrite any links that pointed at diacritic-stripped slugs to the real ones
    if SLUG_FIX:
        pairs = ([(m + "/", r + "/") for m, r in SLUG_FIX.items()] +
                 [(m + '"', r + '"') for m, r in SLUG_FIX.items()])
        fixed = 0
        for root_, _dirs, files in os.walk(SITE):
            for fn in files:
                if not fn.endswith((".htm", ".html")):
                    continue
                hp = os.path.join(root_, fn)
                txt = open(hp, encoding="utf-8", errors="replace").read()
                if not any(m in txt for m in SLUG_FIX):
                    continue
                for a, b in pairs:
                    txt = txt.replace(a, b)
                with open(hp, "w", encoding="utf-8") as f:
                    f.write(txt)
                fixed += 1
        log("  rewrote diacritic slug links in %d files (%d slugs fixed)" % (fixed, len(SLUG_FIX)))

    write_index()
    # dedup report lists for a clean summary
    for k in ("assets_ok", "assets_dead", "stripped_scripts"):
        report[k] = sorted(set(report[k]))
    with open(os.path.join(HERE, "build_report.json"), "w") as f:
        json.dump(report, f, indent=2)
    log("\neditions: %d  detail pages: %d  legacy: %d  assets ok: %d  dead: %d  stripped: %d" %
        (len(report["pages"]), len(report.get("subpages", [])),
         len(report.get("legacy_pages", [])), len(report["assets_ok"]),
         len(report["assets_dead"]), len(report["stripped_scripts"])))
    if report["assets_dead"]:
        log("DEAD ASSETS (gone at source, unrecoverable):")
        for d in report["assets_dead"]:
            log("  - " + d)


def write_index():
    """Root redirects to the latest edition, matching the live site (whose root
    301s to /lambdadays<latest>). Uses the newest edition present on disk."""
    latest = max((y for y in YEARS
                  if os.path.isfile(os.path.join(SITE, "lambdadays%d" % y, "index.html"))),
                 default=max(YEARS))
    target = "/lambdadays%d/" % latest
    html = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta http-equiv="refresh" content="0; url=%(t)s">
  <link rel="canonical" href="%(t)s">
  <title>Lambda Days</title>
  <script>location.replace("%(t)s");</script>
</head>
<body>
  <p>Redirecting to <a href="%(t)s">Lambda Days %(y)d</a>&hellip;</p>
</body>
</html>
""" % {"t": target, "y": latest}
    with open(os.path.join(SITE, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    # custom domain marker for GitHub Pages
    with open(os.path.join(SITE, "CNAME"), "w") as f:
        f.write("lambdadays.org\n")
    log("  wrote root redirect -> %s + CNAME" % target)


# Catch-all: any asset URL in any built page/CSS, whatever tag/attr/encoding.
# Quoted attrs capture the FULL value (so names with parens/spaces aren't cut).
SWEEP_RES = [
    re.compile(r'(?:src|href|content|data-href|data-src|data-bg)\s*=\s*"([^"]+)"', re.I),
    re.compile(r"(?:src|href|content|data-href|data-src|data-bg)\s*=\s*'([^']+)'", re.I),
    re.compile(r"url\(\s*['\"]?([^'\")]+)"),
]
REMOTE_ASSET_RE = re.compile(
    r"^https?://(?:www\.lambdadays\.org/static/"
    r"|lambdadays-prod\.s3\.amazonaws\.com/"
    r"|s3\.amazonaws\.com/lambdadays-prod/)")


def sweep():
    """Final completeness pass: walk every built HTML/CSS file and ensure every
    referenced asset is hosted locally -- remote lambdadays/S3 URLs (any tag,
    incl <a>/<meta>) get downloaded + rewritten; root-relative /static refs that
    are missing on disk get fetched. Encoding-aware. Idempotent."""
    log("== SWEEP (completeness) ==")
    downloaded, rewritten, dead = 0, 0, set()
    for root_, _dirs, files in os.walk(SITE):
        for fn in files:
            if not fn.endswith((".htm", ".html", ".css")):
                continue
            hp = os.path.join(root_, fn)
            txt = open(hp, encoding="utf-8", errors="replace").read()
            orig = txt
            # normalize absolute same-site /static URLs to root-relative (catches
            # legacy data-href / @font-face refs); the loop below fetches any missing.
            txt = re.sub(r"https?://(?:www\.)?lambdadays\.org/static/", "/static/", txt)
            toks = set()
            for rx in SWEEP_RES:
                toks |= set(rx.findall(txt))
            for tok in toks:
                if tok.startswith(("data:", "#", "mailto:", "tel:", "javascript:")):
                    continue
                if REMOTE_ASSET_RE.match(tok):
                    lp = local_target(tok)
                    if not lp:
                        continue
                    got = download_to_site(tok, lp)
                    if got:
                        downloaded += 1
                        txt = txt.replace(tok, got)
                    else:
                        dead.add(tok)
                elif tok.startswith("/static/") and not tok.lower().endswith((".htm", ".html")):
                    decoded = urllib.parse.unquote(tok)
                    if not os.path.isfile(os.path.join(SITE, decoded.lstrip("/"))):
                        got = download_to_site(BASE + tok, tok)
                        if got:
                            downloaded += 1
                            if got != tok:
                                txt = txt.replace(tok, got)
                        else:
                            dead.add(tok)
            if txt != orig:
                open(hp, "w", encoding="utf-8").write(txt)
                rewritten += 1
    log("  swept: downloaded %d assets, rewrote %d files, %d dead-at-source" %
        (downloaded, rewritten, len(dead)))
    for d in sorted(dead):
        log("    dead: " + d)


# Recovered replacement logos for 2017/2018 sponsors whose S3 originals 404'd.
# Maps the original (dead) image basename -> file in recovered_logos/ (None = skip
# the sponsor and remove its tile: site dead/parked or Russian-takeover).
RELOGO_MAP = {
    2017: {
        "unnamed.jpg": "pti.png",
        "gp-logo-orange-poziom-grey-orange (4) (1).png": "williamhill.png",  # Grand Parade = part of William Hill
        "logo-red.jpg": "codegram.png",
        "is-logoblue.png": "ironsource.svg",
        "microsoft-logo_cmyk_c-gray.png": "microsoft.png",
        "avatar_logo_thumb.jpg": "sphere-engine.svg",   # Sphere Research (2017)
        "gcc_logo.png": "ggc.svg",
        "logo_vertical.png": "it-leaders.png",
        "f(by) logo.png": None,                          # fby.by -> Russian takeover: skip
    },
    2018: {
        "uswitch-logo-vertical-rgb-v1.1.png": "uswitch.png",
        "zimpler_logo_original@1x.png": "zimpler.png",
        "vertical-logo.png": "subvisual.svg",
        "ihsm_logo.jpg": "ihs-markit.png",
        "1.png": "slidemight.png",
        "elixirfountain-logo-2.png": "elixirfountain.png",
        "logo_01.png": None,                             # fby.by -> Russian takeover: skip
        "confengine_square_thumb.png": "confengine.png",
        "avatar_logo_thumb.jpg": "spoj.png",             # SPOJ (2018)
        "witistacked.png": "witi.png",
        "krakowjs.png": None,                            # domain parked/for sale: skip
        "unnamed.jpg": "pti.png",
    },
}


def relogo():
    """Restore 2017/2018 sponsor logos (S3 originals 404'd). Regenerates the two
    landing pages from the raw mirror (so every tile is present), then rewrites each
    sponsor <img> to a recovered logo in /static/logos/, removing tiles for sponsors
    we skip (dead/parked/Russian-takeover). Reproducible + idempotent."""
    from bs4 import BeautifulSoup
    import shutil
    log("== RELOGO (restore sponsor logos) ==")
    rl = os.path.join(HERE, "recovered_logos")
    dst = os.path.join(SITE, "static", "logos")
    os.makedirs(dst, exist_ok=True)
    if os.path.isdir(rl):
        for f in os.listdir(rl):
            shutil.copy(os.path.join(rl, f), dst)
    for year, m in RELOGO_MAP.items():
        raw = os.path.join(PAGES, "%d.html" % year)
        if not os.path.exists(raw):
            continue
        soup = BeautifulSoup(open(raw, encoding="utf-8", errors="replace").read(), "html.parser")
        localize(soup, "%s/lambdadays%d" % (BASE, year), str(year))
        rep = rm = 0
        for img in list(soup.find_all("img")):
            base = urllib.parse.unquote((img.get("src") or "").split("?")[0]).split("/")[-1].lower()
            if base in m:
                tgt = m[base]
                if tgt:
                    img["src"] = "/static/logos/" + tgt
                    st = img.get("style") or ""
                    img["style"] = st + (";" if st and not st.endswith(";") else "") + "max-width:100%;max-height:100%;"
                    rep += 1
                else:
                    t = img.find_parent(class_="sp-tile")
                    (t or img).decompose()
                    rm += 1
        # drop remaining dead decorative (non-tile) S3 images so nothing is broken
        for img in list(soup.find_all("img")):
            if "lambdadays-prod/img" in (img.get("src") or "") and not img.find_parent(class_="sp-tile"):
                a = img.find_parent("a")
                img.decompose()
                if a and not a.get_text(strip=True) and not a.find("img"):
                    a.decompose()
        with open(os.path.join(SITE, "lambdadays%d" % year, "index.html"), "w", encoding="utf-8") as f:
            f.write(str(soup))
        log("  %d: %d logos set, %d tiles removed" % (year, rep, rm))


def menufix():
    """The nav 'Other events' dropdown only opened via Bootstrap's click-JS (which
    isn't reliable in the static archive), so its edition links were unreachable.
    Rename it to 'Past events' and make it open on hover/focus with pure CSS -- no
    JS needed. Idempotent."""
    log("== MENU FIX (Past events dropdown) ==")
    css_path = os.path.join(SITE, "static/css/theme.css")
    if os.path.exists(css_path):
        c = open(css_path, encoding="utf-8", errors="replace").read()
        if "focus-within>.dropdown-menu" not in c:
            rule = (".dropdown:hover>.dropdown-menu,"
                    ".dropdown:focus-within>.dropdown-menu{display:block}")
            open(css_path, "a", encoding="utf-8").write(
                "\n/* archive: open the Past events dropdown without JS */\n" + rule + "\n")
            log("  added hover/focus dropdown CSS to theme.css")
    # The cross-page nav links (other editions + Code Sync) originally had
    # class="external" so the onePageNav smooth-scroll plugin (filter ':not(.external)')
    # would let them navigate. A duplicate class attr in the source meant 'external'
    # was lost in parsing, so onePageNav swallowed the click (preventDefault, no scroll
    # target) and nothing happened. Restore 'external' on the target="_blank" nav links.
    ext_re = re.compile(r'<a class="menu-item"((?:(?!</a>)[^>])*?\btarget="_blank")')
    n = pages_ext = 0
    for root_, _d, files in os.walk(SITE):
        for fn in files:
            if not fn.endswith((".htm", ".html")):
                continue
            hp = os.path.join(root_, fn)
            t = open(hp, encoding="utf-8", errors="replace").read()
            orig = t
            if ">Other events<" in t:
                t = t.replace(">Other events<", ">Past events<")
            t2 = ext_re.sub(r'<a class="external menu-item"\1', t)
            if t2 != t:
                pages_ext += 1
            t = t2
            if t != orig:
                open(hp, "w", encoding="utf-8").write(t)
                n += 1
    log("  menu pages updated: %d (external-class restored on %d)" % (n, pages_ext))


def strip_cookie_consent():
    """Remove the live site's cookie-consent popup from the archive (theme.js
    loads it via $.getScript). Pointless on a retired static archive."""
    p = os.path.join(SITE, "static/js/theme.js")
    if os.path.exists(p):
        t = open(p, encoding="utf-8", errors="replace").read()
        t2 = re.sub(r'(?m)^\s*//\s*load cookie consent\s*\n?', '', t)
        t2 = re.sub(r'\$\.getScript\(\s*["\']/static/upload/media/cookie-consent\.js["\']\s*\)\s*;?', '', t2)
        if t2 != t:
            open(p, "w", encoding="utf-8").write(t2)
            log("  stripped cookie-consent loader from theme.js")
    cc = os.path.join(SITE, "static/upload/media/cookie-consent.js")
    if os.path.exists(cc):
        os.remove(cc)
        log("  removed cookie-consent.js")


def _add_style(el, prop, val):
    cur = (el.get("style") or "").strip()
    if cur and not cur.endswith(";"):
        cur += ";"
    el["style"] = cur + "%s:%s;" % (prop, val)


def bake_edition_styles():
    """The per-edition theme-<n>.js applies section backgrounds/colors at runtime
    via jQuery (.parent().css(...)). Relying on that JS is fragile for an archive,
    so we BAKE those rules into the static HTML: set the backgrounds/colors as
    inline styles + a <style> block, exactly as the JS would. No JS needed."""
    from bs4 import BeautifulSoup
    log("== BAKE edition styles into static HTML ==")

    def edition(year):  # theme.js loadAssets mapping: 2015-2022 own, else 2023
        return year if 2015 <= year <= 2022 else 2023

    # parse a theme-<n>.js into rule buckets (cached per edition)
    cache = {}
    def rules_for(n):
        if n in cache:
            return cache[n]
        p = os.path.join(SITE, "static/upload/media/theme-%d.js" % n)
        js = open(p, encoding="utf-8", errors="replace").read() if os.path.exists(p) else ""
        V = r'"([^"]*)"'
        r = {
            "parent":   re.findall(r'\$\(\s*"#([\w-]+)"\s*\)\.parent\(\)\.css\(\s*%s\s*,\s*%s\s*\)' % (V, V), js),
            "find":     re.findall(r'\$\(\s*"#([\w-]+)"\s*\)\.parent\(\)\.find\(\s*"(\w+)"\s*\)\.css\(\s*%s\s*,\s*%s\s*\)' % (V, V), js),
            "children": re.findall(r'\$\(\s*"#([\w-]+)"\s*\)\.parent\(\)\.children\(\s*"(\w+)"\s*\)\.css\(\s*%s\s*,\s*%s\s*\)' % (V, V), js),
            "cls":      re.findall(r'\$\(\s*"\.([\w-]+)"\s*\)\.css\(\s*%s\s*,\s*%s\s*\)' % (V, V), js),
        }
        cache[n] = r
        return r

    n_pages = 0
    for y in YEARS:
        n = edition(y)
        r = rules_for(n)
        pages = [os.path.join(SITE, "lambdadays%d" % y, "index.html")]
        pages += [os.path.join(dp, "index.html")
                  for dp, _d, fs in os.walk(os.path.join(SITE, "lambdadays%d" % y))
                  if "index.html" in fs]
        for hp in sorted(set(pages)):
            if not os.path.exists(hp):
                continue
            html = open(hp, encoding="utf-8", errors="replace").read()
            if "edition-styles-baked" in html:
                continue  # idempotent: already baked
            soup = BeautifulSoup(html, "html.parser")
            soup.append(BeautifulSoup("<!--edition-styles-baked-->", "html.parser"))
            changed = False
            for aid, prop, val in r["parent"]:
                a = soup.find(id=aid)
                if a and a.parent:
                    _add_style(a.parent, prop, val); changed = True
            for aid, tag, prop, val in r["find"]:
                a = soup.find(id=aid)
                if a and a.parent:
                    for e in a.parent.find_all(tag):
                        _add_style(e, prop, val); changed = True
            for aid, tag, prop, val in r["children"]:
                a = soup.find(id=aid)
                if a and a.parent:
                    for e in a.parent.find_all(tag, recursive=False):
                        _add_style(e, prop, val); changed = True
            # class rules -> a single injected <style> block
            if r["cls"]:
                css = "".join(".%s{%s:%s !important}" % (c, p, v) for c, p, v in r["cls"])
                tag = soup.new_tag("style"); tag.string = css
                (soup.head or soup).append(tag); changed = True
            if changed:
                open(hp, "w", encoding="utf-8").write(str(soup))
                n_pages += 1
    log("  baked edition styles into %d pages" % n_pages)


def capture_edition_themes():
    """/static/js/theme.js loads per-edition CSS+JS at runtime
    (/static/upload/media/theme-<edition>.{css,js}); that JS applies the section
    backgrounds (e.g. the pink sponsor banner), colors and card frames via jQuery.
    Static crawling misses them, so fetch them + the assets they reference here so
    theme.js applies the real styling in the browser."""
    log("== EDITION THEMES (JS-injected per-edition css/js) ==")
    files = ["/static/upload/media/cookie-consent.js"]
    for n in range(2015, 2024):  # theme.js maps 2014/2023/2024/2025 -> 2023
        files += ["/static/upload/media/theme-%d.css" % n,
                  "/static/upload/media/theme-%d.js" % n]
    for path in files:
        if not download_to_site(BASE + path, path):
            continue
        dest = os.path.join(SITE, path.lstrip("/"))
        if path.endswith(".css"):
            process_css(path, BASE + path)
        elif path.endswith(".js"):
            txt = open(dest, encoding="utf-8", errors="replace").read()
            orig = txt
            # asset URLs embedded in JS strings (backgrounds, <img> the JS injects)
            for u in set(re.findall(r"https?://[^\s'\"()]+|/static/[^\s'\"()]+", txt)):
                if u.startswith("http"):
                    if "lambdadays" not in u:
                        continue
                    lt = local_target(u)
                    if not lt:
                        continue
                    href = download_to_site(u, lt)
                    if href:
                        txt = txt.replace(u, href)   # rewrite remote -> local
                elif u.startswith("/static/") and not u.lower().endswith((".css", ".js")):
                    download_to_site(BASE + u, u)     # ensure asset present locally
            if txt != orig:
                open(dest, "w", encoding="utf-8").write(txt)
    log("  edition themes + their assets captured")


def _video_embed_src(href):
    """Map a talk 'Video' link (YouTube or Vimeo) to a privacy-friendly embed URL.
    Returns (embed_src, provider) or None if the href isn't an embeddable video.
    Handles youtu.be/<id>, youtube.com/watch?v=<id>[&list=..], /embed/<id>, and
    vimeo.com/<id> -- plus a stray leading space some source hrefs carry."""
    href = (href or "").strip().replace("&amp;", "&")
    u = urllib.parse.urlparse(href)
    host = u.netloc.lower()
    if "youtu.be" in host:
        vid = u.path.strip("/").split("/")[0]
        return ("https://www.youtube-nocookie.com/embed/" + vid, "youtube") if vid else None
    if "youtube.com" in host:
        vid = (urllib.parse.parse_qs(u.query).get("v") or [None])[0]
        if not vid and u.path.startswith("/embed/"):
            vid = u.path.split("/embed/", 1)[1].strip("/")
        return ("https://www.youtube-nocookie.com/embed/" + vid, "youtube") if vid else None
    if "vimeo.com" in host:
        vid = u.path.strip("/").split("/")[0]
        return ("https://player.vimeo.com/video/" + vid, "vimeo") if vid.isdigit() else None
    return None


_VIDEO_ALLOW = {
    "youtube": ("accelerometer; autoplay; clipboard-write; encrypted-media; "
                "gyroscope; picture-in-picture; web-share"),
    "vimeo": "autoplay; fullscreen; picture-in-picture; clipboard-write",
}


def _talk_video_div(soup, src, provider, title):
    """Build the responsive 16:9 <div class="talk-video"><iframe>...</div> node."""
    wrap = soup.new_tag("div"); wrap["class"] = "talk-video"
    iframe = soup.new_tag(
        "iframe", src=src, title=title, loading="lazy",
        referrerpolicy="strict-origin-when-cross-origin")
    iframe["allow"] = _VIDEO_ALLOW[provider]
    iframe["allowfullscreen"] = ""
    wrap.append(iframe)
    return wrap


def embed_talk_videos():
    """Turn each speaker's outbound 'Video' link into an inline embedded player.

    Paulina's request: play talk videos inside the speaker profile instead of
    linking out. The per-talk video URL already lives in every profile as the
    '<span class="glyphicon-film"> Video' link, so we parse that, resolve it to a
    YouTube/Vimeo embed, and REPLACE the link with a responsive 16:9 iframe (styled
    by the .talk-video class added to theme.css). The text link is dropped per the
    design decision -- the player has its own 'Watch on YouTube'/Vimeo affordance.

    Scope: speaker DETAIL pages only (lambdadays<year>/<slug>/index.html), never the
    edition landing pages. Idempotent via a 'talk-video-embedded' marker; pages with
    no video link or an unrecognised provider are left untouched (logged)."""
    from bs4 import BeautifulSoup
    log("== EMBED talk videos into speaker profiles ==")

    # responsive 16:9 wrapper -- added once to theme.css (DRY, no inline styles)
    css_path = os.path.join(SITE, "static/css/theme.css")
    if os.path.exists(css_path):
        c = open(css_path, encoding="utf-8", errors="replace").read()
        if ".talk-video{" not in c:
            open(css_path, "a", encoding="utf-8").write(
                "\n/* archive: embedded talk video (responsive 16:9) */\n"
                ".talk-video{position:relative;width:100%;max-width:720px;"
                "margin:18px 0 10px;padding-bottom:56.25%;height:0;overflow:hidden;"
                "border-radius:8px;background:#000}\n"
                ".talk-video iframe{position:absolute;top:0;left:0;width:100%;"
                "height:100%;border:0}\n")
            log("  added .talk-video CSS to theme.css")

    n_embed = n_skip = 0
    for y in YEARS:
        base = os.path.join(SITE, "lambdadays%d" % y)
        if not os.path.isdir(base):
            continue
        for slug in sorted(os.listdir(base)):
            hp = os.path.join(base, slug, "index.html")  # detail pages only
            if not os.path.isfile(hp):
                continue
            html = open(hp, encoding="utf-8", errors="replace").read()
            soup = BeautifulSoup(html, "html.parser")
            # Handle EVERY video link on the page -- some speakers gave multiple
            # talks, so a profile can carry more than one. Idempotent per-link:
            # embedding removes the 'Video' link, so a re-run finds nothing to do.
            spans = soup.find_all("span", class_="glyphicon-film")
            if not spans:
                continue  # this speaker has no recorded video -- leave as-is
            name = soup.find("h3")
            name = name.get_text(strip=True) if name else slug.replace("-", " ").title()
            changed = False
            for span in spans:
                a = span.find_parent("a")
                info = _video_embed_src(a.get("href") if a else None)
                if not info:
                    n_skip += 1
                    log("  SKIP (unrecognised video href): lambdadays%d/%s" % (y, slug))
                    continue
                src, provider = info
                h4 = a.find_previous("h4", class_="modal-title")  # this talk's title
                talk = h4.get_text(strip=True) if h4 else ""
                title = " — ".join(x for x in (name, talk, "Lambda Days %d" % y) if x)
                wrap = _talk_video_div(soup, src, provider, title)
                a.replace_with(wrap)  # drop the text link, keep only the player
                changed = True
                n_embed += 1
            if changed:
                if "talk-video-embedded" not in html:
                    soup.append(BeautifulSoup("<!--talk-video-embedded-->", "html.parser"))
                open(hp, "w", encoding="utf-8").write(str(soup))
    log("  embedded %d talk videos (%d skipped, unrecognised href)" % (n_embed, n_skip))


def fill_missing_videos():
    """Inject embeds for speaker profiles whose talk had NO 'Video' link at the
    source, so embed_talk_videos() couldn't reach them. Reads gap_videos.json
    (mapping 'lambdadays<year>/<slug>' -> a YouTube/Vimeo id or URL, hand-matched
    from the official Code Sync per-edition playlists) and inserts the same
    .talk-video player just before the '←Back' link. Idempotent: a page that
    already carries a .talk-video is left untouched."""
    from bs4 import BeautifulSoup
    log("== FILL missing talk videos (gap pages, from playlist matches) ==")
    mp = os.path.join(HERE, "gap_videos.json")
    if not os.path.exists(mp):
        log("  no gap_videos.json -- nothing to fill"); return
    mapping = json.load(open(mp, encoding="utf-8"))
    n = miss = 0
    for key, ref in mapping.items():
        if key.startswith("_"):
            continue  # comment fields
        y = int(key.split("/")[0].replace("lambdadays", ""))
        hp = os.path.join(SITE, key, "index.html")
        if not os.path.isfile(hp):
            log("  MISSING page: %s" % key); miss += 1; continue
        html = open(hp, encoding="utf-8", errors="replace").read()
        if 'class="talk-video"' in html:
            continue  # already embedded
        # bare 11-char token => YouTube id; anything with '/' or '.' => full URL
        if "/" not in ref and "." not in ref:
            src, provider = "https://www.youtube-nocookie.com/embed/" + ref, "youtube"
        else:
            info = _video_embed_src(ref)
            if not info:
                log("  SKIP (bad ref %r): %s" % (ref, key)); miss += 1; continue
            src, provider = info
        soup = BeautifulSoup(html, "html.parser")
        back = soup.find("a", href="/lambdadays%d/" % y)  # the '←Back' link
        if back is None:
            log("  SKIP (no back-link anchor): %s" % key); miss += 1; continue
        name = soup.find("h3")
        name = name.get_text(strip=True) if name else ""
        h4 = back.find_previous("h4", class_="modal-title")
        talk = h4.get_text(strip=True) if h4 else ""
        title = " — ".join(x for x in (name, talk, "Lambda Days %d" % y) if x)
        back.insert_before(_talk_video_div(soup, src, provider, title))
        if "talk-video-embedded" not in html:
            soup.append(BeautifulSoup("<!--talk-video-embedded-->", "html.parser"))
        open(hp, "w", encoding="utf-8").write(str(soup))
        n += 1
    log("  filled %d gap videos (%d unresolved)" % (n, miss))


if __name__ == "__main__":
    phase = sys.argv[1] if len(sys.argv) > 1 else "all"
    if phase in ("crawl", "all"):
        log("== CRAWL ==")
        crawl()
    if phase in ("build", "all"):
        log("== BUILD ==")
        build()
    if phase in ("themes", "build", "all"):
        capture_edition_themes()
    if phase in ("relogo", "build", "all"):
        relogo()
    if phase in ("bake", "relogo", "themes", "build", "all"):
        bake_edition_styles()
    if phase in ("cookie", "themes", "build", "all"):
        strip_cookie_consent()
    if phase in ("menufix", "themes", "build", "all"):
        menufix()
    if phase in ("embed", "build", "all"):
        embed_talk_videos()
    if phase in ("fillgaps", "embed", "build", "all"):
        fill_missing_videos()
    if phase in ("sweep", "all"):
        sweep()
    log("done.")
