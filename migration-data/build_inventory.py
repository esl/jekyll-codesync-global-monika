#!/usr/bin/env python3
"""Generate INVENTORY.md from the probe data in migration-data/.

Sources (see MIGRATION.md):
  live_tiles.json        - tiles scraped from https://codesync.global/conferences/
  cms_pages.json         - structure probe of the 22 CMS-hosted conference pages
  external_status.json   - link health of external tiles + ESL brand-repo archive listings
  youtube_playlists.json - all 67 playlists on the Code Sync YouTube channel
  erlang_factory.json    - census of the 61 pre-Sonata editions on erlang-factory.com

The modern-brand rows are curated here (cross-source judgment calls are encoded
as data); the Older Conferences table is generated from erlang_factory.json.
Re-run after refreshing any probe: python3 migration-data/build_inventory.py
"""
import json, html, pathlib

D = pathlib.Path(__file__).parent
playlists = json.load(open(D / "youtube_playlists.json"))
factory = json.load(open(D / "erlang_factory.json"))

def norm(t):
    return html.unescape(t or "").strip().lower()

PL = {}
for p in playlists:
    PL.setdefault(norm(p.get("title")), p)

def pl_cell(title):
    if title is None:
        return "none"
    p = PL.get(norm(title))
    if not p:
        return f"NOT FOUND: {title}"
    n = p.get("video_count")
    n = f", {n} videos" if n else ""
    return f"[{html.unescape(p['title'])}]({p['url']}{n and ''}){n}"

# --- curated modern-brand rows -------------------------------------------
# home: where the edition's content lives today
# action: what the migration must do with it
BRANDS = {}

BRANDS["Code BEAM America"] = [
    ("Code BEAM America 2025", "6-7 Mar 2025",
     "codebeamamerica.com root page (live - still serves the 2025 edition; no CBA_2025 in repo archives/ yet)",
     "Code BEAM America 2025",
     "snapshot into esl/code-beam-america archives/CBA_2025 before a future edition replaces the root (a second 2-video 2025 playlist also exists)"),
    ("Code BEAM America 2024", "7-8 Mar 2024",
     "esl/code-beam-america archives/CBA_2024 (codebeamamerica.com/archives/CBA_2024 responds 200)",
     "Code BEAM America 2024", "none - hub links out"),
    ("Code BEAM America 2022", "3-4 Nov 2022",
     "esl/code-beam-america archives/CBA_2022 (alive)",
     "Code BEAM America 2022", "none - hub links out"),
    ("Code BEAM America 2021 (SF)", "3-5 Nov 2021",
     "CMS: /conferences/code-beam-sf-2021/ (63 speakers, cms-native schedule)",
     "Code BEAM America 2021", "extract to esl/code-beam-america archives/"),
    ("Code BEAM V America 2021", "10-12 Mar 2021",
     "CMS: /conferences/code-beam-v-america-2021/ (57 speakers, cms-native schedule)",
     "Code BEAM V America 2021", "extract to esl/code-beam-america archives/"),
    ("Code BEAM SF 2020", "5-6 Mar 2020",
     "CMS: /conferences/code-beam-sf/ (61 speakers, cms-native schedule)",
     "Code BEAM SF 2020", "extract to esl/code-beam-america archives/"),
    ("Code BEAM SF 2019", "28 Feb - 1 Mar 2019",
     "CMS: /conferences/code-beam-sf-2019/ (60 speakers, cms-native schedule)",
     "Code BEAM SF 2019", "extract to esl/code-beam-america archives/"),
    ("Code BEAM SF 2018", "15-17 Mar 2018",
     "CMS: /conferences/code-beam-sf-2018/ (54 speakers); secondary copy live on erlang-factory.com",
     "Code BEAM SF 2018", "extract to esl/code-beam-america archives/"),
]

BRANDS["Code BEAM Europe / STO"] = [
    ("Code BEAM Europe 2025 (Berlin)", "5-6 Nov 2025",
     "esl/code-beam-europe archives/berlin_2025",
     "Code BEAM Europe 2025",
     "hub entry still has past:false - flip it (also: Gleam Talks CBE 2025 playlist exists)"),
    ("Code BEAM Europe 2024 (Berlin)", "14-15 Oct 2024",
     "esl/code-beam-europe archives/berlin_2024",
     "Code BEAM Europe 2024", "add hub entry (missing from _conferences)"),
    ("Code BEAM Europe 2023 (Berlin)", "19-20 Oct 2023",
     "esl/code-beam-europe archives/berlin_2023 (alive)",
     "Code BEAM Europe 2023", "add hub entry"),
    ("Code BEAM Europe 2022 (Stockholm)", "19-20 May 2022",
     "CMS: /conferences/code-beam-sto-2022/ (43 speakers, cms-native schedule)",
     "Code BEAM Europe 2022",
     "extract to esl/code-beam-stockholm archive/ - VERIFY playlist mapping (titled Europe, event branded STO)"),
    ("Code BEAM STO 2021 (virtual)", "19-21 May 2021",
     "CMS: /conferences/code-beam-sto-2021/ (63 speakers)",
     "Code BEAM V Europe 2021",
     "extract to esl/code-beam-stockholm archive/ - VERIFY playlist mapping"),
    ("Code BEAM STO 2020 (virtual)", "10-11 Sep 2020",
     "CMS: /conferences/code-beam-sto/ (55 speakers)",
     "Code BEAM V 2020",
     "extract to esl/code-beam-stockholm archive/ - VERIFY playlist mapping (V 2020 may be a distinct virtual event)"),
    ("Code BEAM STO 2019", "16-17 May 2019",
     "CMS: /conferences/code-beam-sto-2019/ (67 speakers)",
     "Code BEAM STO 2019", "extract to esl/code-beam-stockholm archive/"),
    ("Code BEAM STO 2018", "31 May - 1 Jun 2018 (verify)",
     "erlang-factory.com (live static page); MISSING from codesync.global listing",
     "Code BEAM STO 2018",
     "add edition to hub listing + archive to esl/code-beam-stockholm; verify exact dates from page"),
]

BRANDS["Code BEAM Lite"] = [
    ("Code BEAM Lite Stockholm 2026", "2026 (upcoming/recent - verify)",
     "esl/code-beam-stockholm (current site)",
     "Code BEAM Lite Stockholm 2026", "verify status; hub upcoming/past entry"),
    ("Code BEAM Lite Stockholm 2025", "Jun 2025 (verify)",
     "esl/code-beam-stockholm archive/june_2025",
     "Code BEAM Lite Stockholm 2025", "add hub entry"),
    ("Code BEAM Lite London 2025", "Jan 2025",
     "esl/code-beam-london archive/january_2025",
     None, "add hub entry; no playlist found"),
    ("Code BEAM Lite NYC 2024", "Nov 2024",
     "esl/code-beam-nyc archive/nov_2024",
     None, "add hub entry; no playlist found"),
    ("Code BEAM Lite Stockholm 2024", "May 2024 (verify)",
     "esl/code-beam-stockholm archive/may_2024",
     "Code BEAM Lite Stockholm 2024", "add hub entry"),
    ("Code BEAM Lite Stockholm 2023", "12 May 2023",
     "esl/code-beam-stockholm archive/may_2023 (codebeamstockholm.com alive)",
     "Code BEAM Lite Stockholm 2023", "none - hub links out"),
    # Mexico / A Coruna / Brasil moved to the partner-run section below.
    ("Code BEAM Lite Virtual 2020", "3-4 Apr 2020",
     "CMS: /conferences/code-beam-lite-virtual/ (9 speakers)",
     None, "extract to new esl/code-beam-lite archives/"),
    ("Code BEAM Lite Amsterdam 2019", "28 Nov 2019",
     "CMS: /conferences/code-beam-lite-amsterdam/ (20 speakers)",
     "Code BEAM Lite Amsterdam 19", "extract"),
    ("Code BEAM Lite India 2019", "14 Nov 2019",
     "CMS: /conferences/code-beam-lite-india/ (5 speakers, NO schedule section)",
     None, "extract; page was never fully built - mark partial"),
    ("Code BEAM Lite Berlin 2019", "11 Oct 2019",
     "CMS: /conferences/code-beam-lite-berlin-2019/ (16 speakers)",
     None, "extract"),
    ("Code BEAM Lite Budapest 2019", "20 Sep 2019",
     "CMS: /conferences/code-beam-lite-budapest/ (19 speakers)",
     None, "extract"),
    ("Code BEAM Lite Italy 2019", "22 Mar 2019",
     "CMS: /conferences/code-beam-lite-italy/ (16 speakers)",
     None, "extract"),
    ("Code BEAM Lite Munich 2018", "7 Dec 2018",
     "CMS: /conferences/cbl-munich-2018/ (14 speakers)",
     "Code BEAM Lite Munich 2018", "extract"),
    ("Code BEAM Lite Amsterdam 2018", "30 Nov 2018",
     "CMS: /conferences/cbl-amsterdam-2018/ (18 speakers)",
     None, "extract; hub entry exists but has broken brand ref + missing init date"),
    ("Code BEAM Lite Berlin 2018", "12 Oct 2018",
     "CMS: /conferences/code-beam-lite-berlin-2018/ (14 speakers)",
     "Code BEAM Lite Berlin 2018", "extract"),
]

BRANDS["Partner-run Code BEAM editions"] = [
    # Run under the Code BEAM brand by local partners, not by Code Sync/ESL directly.
    ("Code BEAM Mexico 2023", "3-4 Mar 2023",
     "codebeammexico.com root page (live, partner-run); esl/code-beam-mexico repo holds only 2015-2020 legacy content",
     "Code BEAM Lite Mexico 2023", "hub links out; consider snapshotting since root page will not last forever"),
    ("Code BEAM Lite A Coruna 2022", "10-11 Jun 2022",
     "codebeamcorunha.es (live, partner-run; content is JS-rendered)",
     "Code BEAM Lite A Coruña 2022",
     "hub links out; later partner editions exist (Code BEAM Corunha 2024 CfP on Sessionize) - decide if they belong on the listing"),
    ("Code BEAM Brasil 2020 (virtual)", "6-7 Nov 2020",
     "site possibly codebeambr.com (Cloudflare-blocked to curl - verify in a browser); reported by InfoQ",
     None,
     "OPEN: confirm site and speaker/schedule data; no playlist on the Code Sync channel - talks may be on a Brazilian community channel"),
]

BRANDS["Code Mesh"] = [
    ("Code Mesh V 2020", "5-6 Nov 2020",
     "CMS: /conferences/code-mesh-ldn/ (50 speakers)",
     "Code Mesh V 2020", "extract to new esl/code-mesh archives/"),
    ("Code Mesh LDN 2019", "6-8 Nov 2019",
     "CMS: /conferences/code-mesh-ldn-2019/ (51 speakers)",
     "Code Mesh LDN 2019", "extract"),
    ("Code Mesh LDN 2018", "8-9 Nov 2018",
     "CMS: /conferences/code-mesh-2018/ (45 speakers)",
     "Code Mesh LDN 2018", "extract"),
    ("Code Mesh 2017", "8-9 Nov 2017",
     "codemesh.io/codemesh2017 (alive)", None, "none - hub links out; consider mirroring later"),
    ("Code Mesh 2016", "3-4 Nov 2016",
     "codemesh.io/codemesh2016 (alive)", None, "none - hub links out; consider mirroring later"),
]

BRANDS["Code Elixir LDN / Elixir LDN"] = [
    ("Code Elixir LDN 2019", "18 Jul 2019",
     "CMS: /conferences/code-elixir-ldn-2019/ (15 speakers)",
     "Code Elixir LDN 2019", "extract to new esl/code-elixir-ldn archives/"),
    ("Code Elixir LDN 2018", "16 Aug 2018",
     "NOT on live listing; hub entry exists; check Wayback for codesync.global/conferences/code-elixir-ldn-2018",
     "Code Elixir LDN 2018", "reconstruct from Wayback + playlist (16 videos)"),
    ("Elixir LDN 2017", "17 Aug 2017",
     "LOST - elixir.london DNS dead; Wayback captures exist (verify post-event snapshots); no playlist",
     None, "reconstruct-from-wayback (partial); hub entry exists"),
    ("Elixir.LDN 2016", "22 Sep 2016",
     "LOST - elixir.london/2016 DNS dead; Wayback capture 2016-09-21 is PRE-event; no playlist",
     None, "reconstruct-from-wayback (partial); check for post-event captures"),
]

BRANDS["ElixirConf EU"] = [
    ("ElixirConf EU 2026 (Malaga)", "23-24 Apr 2026",
     "www.elixirconf.eu (current site; not yet in archives/)",
     "ElixirConf EU 2026",
     "add hub entry; archive to elixirconf-eu-jekyll archives/ when the site rolls over"),
    ("ElixirConf EU 2025 (Krakow)", "2025 (verify)",
     "esl/elixirconf-eu-jekyll archives/krakow_2025",
     "ElixirConf EU 2025", "add hub entry (missing from listing); 2026 playlist also already exists"),
    ("ElixirConf EU 2024 (Lisbon)", "18-19 Apr 2024",
     "elixirconf.eu/archives/lisbon_2024 (alive, in repo)",
     "ElixirConf EU 2024", "none - hub links out"),
    ("ElixirConf EU 2023 (Lisbon)", "20-21 Apr 2023",
     "elixirconf.eu/archives/lisbon_2023 (alive, in repo)",
     "ElixirConf EU 2023", "none"),
    ("ElixirConf EU 2022 (London)", "9-10 Jun 2022",
     "elixirconf.eu/archives/london_2022 (alive, in repo)",
     "ElixirConf EU 2022", "none"),
    ("ElixirConf EU 2021 (Warsaw)", "9-10 Sep 2021",
     "elixirconf.eu/archives/warsaw_2021 (alive, in repo)",
     "ElixirConf EU 2021", "none"),
    ("ElixirConf EU Virtual X 2020", "7-8 Oct 2020",
     "elixirconf.eu/archives/virtual_x_2020 (alive, in repo)",
     "ElixirConf EU Virtual October 2020", "none"),
    ("ElixirConf EU Virtual VI 2020", "18-19 Jun 2020",
     "elixirconf.eu/archives/virtual_2020 (alive, in repo)",
     "ElixirConf EU Virtual June 2020", "none"),
    ("ElixirConf EU 2019 (Prague)", "8-9 Apr 2019",
     "archive.elixirconf.eu/elixirconfeu2019 (alive; SEPARATE old host - longevity risk)",
     "ElixirConf EU 2019", "consider mirroring 2015-2019 into elixirconf-eu-jekyll archives/"),
    ("ElixirConf EU 2018 (Warsaw)", "16-17 Apr 2018",
     "archive.elixirconf.eu/elixirconfeu2018 (alive; old host)", None, "as above"),
    ("ElixirConf EU 2017 (Barcelona)", "5 Apr 2017",
     "archive.elixirconf.eu/elixirconf2017 (alive; old host)", None, "as above"),
    ("ElixirConf EU 2016 (Berlin)", "11-12 May 2016",
     "archive.elixirconf.eu/elixirconf2016 (alive; old host)", None, "as above"),
    ("ElixirConf EU 2015 (Krakow)", "23-24 Apr 2015",
     "archive.elixirconf.eu/elixirconf2015 (alive; old host)", None, "as above"),
]

BRANDS["ElixirConf US"] = [
    ("ElixirConf US 2025", "28-29 Aug 2025",
     "esl/elixirconf-us archives/elixirconf_2025",
     None,
     "hub entry has past:false (stale) and references missing brand file elixirconf-us.md - fix both"),
]

BRANDS["Lambda Days"] = [
    ("Lambda Days 2025", "2025 (verify)",
     "lambdadays.org (alive); MISSING from codesync.global listing",
     "Lambda Days 2025", "add hub entry"),
    ("Lambda Days 2024", "27-28 May 2024", "lambdadays.org/lambdadays2024 (alive)",
     "Lambda Days 2024", "none - hub links out"),
    ("Lambda Days 2023", "5-6 Jun 2023", "lambdadays.org/lambdadays2023",
     "Lambda Days 2023", "none"),
    ("Lambda Days 2022", "28-29 Jul 2022", "lambdadays.org/lambdadays2022",
     "Lambda Days 2022", "none"),
    ("Lambda Days 2021", "17-18 Feb 2021", "lambdadays.org/lambdadays2021",
     "Lambda Days 2021", "none"),
    ("Lambda Days 2020", "13-14 Feb 2020", "lambdadays.org/lambdadays2020",
     "Lambda Days 2020", "none"),
    ("Lambda Days 2019", "14-15 Feb 2019", "lambdadays.org/lambdadays2019",
     "Lambda Days 2019", "none"),
    ("Lambda Days 2018", "22-23 Feb 2018", "lambdadays.org/lambdadays2018", None, "none"),
    ("Lambda Days 2017", "9-10 Feb 2017", "lambdadays.org/lambdadays2017", None, "none"),
    ("Lambda Days 2016", "25-26 Feb 2016", "lambdadays.org/lambdadays2016", None, "none"),
    ("Lambda Days 2015", "26-27 Feb 2015", "lambdadays.org/lambdadays2015", None, "none"),
    ("Lambda Days 2014", "27-28 Feb 2014", "lambdadays.org/lambdadays2014", None, "none"),
]

# DECIDED: MQ Summit and RabbitMQ Summit are ONE brand section on the listing.
# The RabbitMQ Summit era ran on another platform: rabbitmqsummit.com is the
# canonical reference (per-year pages /2018 /2019 /2021 /2022 /2023 /2024, all
# alive, served from esl/rabbitmq-summit). Current era: esl/mq-summit-page.
BRANDS["MQ Summit (incl. RabbitMQ Summit)"] = [
    ("MQ Summit 2025 (Berlin)", "6 Nov 2025",
     "esl/mq-summit-page archives/berlin_2025 (mqsummit.com)",
     "MQ Summit 2025", "hub entry has past:false - flip it"),
    ("RabbitMQ Summit 2024", "2024 (verify)",
     "rabbitmqsummit.com/2024 (alive - canonical reference)",
     "RabbitMQ Summit 2024", "add hub entry linking to rabbitmqsummit.com/2024"),
    ("RabbitMQ Summit 2023", "2023 (verify)",
     "rabbitmqsummit.com/2023 (alive - canonical reference); mq-summit-page archives/berlin_2023 may duplicate it",
     "RabbitMQ Summit 2023", "add hub entry linking to rabbitmqsummit.com/2023"),
    ("RabbitMQ Summit 2022", "2022 (verify)",
     "rabbitmqsummit.com/2022 (alive - canonical reference)",
     "RabbitMQ Summit 2022", "add hub entry linking to rabbitmqsummit.com/2022"),
    ("RabbitMQ Summit 2021", "2021 (verify)",
     "rabbitmqsummit.com/2021 (alive - canonical reference)",
     "RabbitMQ Summit 2021", "add hub entry linking to rabbitmqsummit.com/2021"),
    ("RabbitMQ Summit 2019", "2019 (verify)",
     "rabbitmqsummit.com/2019 (alive - canonical reference)",
     None, "add hub entry; no playlist found"),
    ("RabbitMQ Summit 2018", "2018 (verify)",
     "rabbitmqsummit.com/2018 (alive - canonical reference)",
     None, "add hub entry; no playlist found (no 2020 edition exists on the site)"),
]

# Upcoming / in-flight editions spotted during the inventory - feed the hub's
# banner/upcoming section (policy: partner conferences get added as they happen).
BRANDS["Upcoming (for the hub banner)"] = [
    ("ElixirConf Brasil 2026", "Nov 2026 (Curitiba & online)",
     "elixirconf.com.br (partner-run, first edition); NOTE esl/elixirconf-brasil repo is a stale EU fork (CNAME still www.elixirconf.eu)",
     None, "add to hub upcoming/banner; move to ElixirConf section once past"),
    ("Code BEAM Europe 2026 (Haarlem)", "21-22 Oct 2026",
     "codebeameurope.com (live)", None, "add to hub upcoming/banner"),
    ("Code BEAM Lite London 2026", "2026 (verify)",
     "codebeamlondon.com (live)", None, "verify date; add to hub upcoming/banner"),
]

# --- emit ------------------------------------------------------------------
out = []
out.append("# Conference migration inventory")
out.append("")
out.append("Generated 2026-07-06 by `migration-data/build_inventory.py` from the probe data")
out.append("in `migration-data/*.json` (live codesync.global listing, CMS page probes, external")
out.append("link health, ESL brand-repo archives, Code Sync YouTube playlists, and the")
out.append("erlang-factory.com census). See MIGRATION.md for the migration contract.")
out.append("")
out.append("Statuses used in Action: `extract` = pull out of the Sonata CMS into a brand")
out.append("repo; `none - hub links out` = already archived/alive elsewhere, the hub just")
out.append("links to it; `reconstruct-from-wayback` = original site dead, rebuild from")
out.append("Wayback Machine captures; `OPEN` = needs a decision or missing information.")
out.append("")

for brand, rows in BRANDS.items():
    out.append(f"## {brand}")
    out.append("")
    out.append("| Edition | Dates | Where the content lives | YouTube playlist | Action / missing |")
    out.append("|---|---|---|---|---|")
    for (ed, dates, home, pl, action) in rows:
        out.append(f"| {ed} | {dates} | {home} | {pl_cell(pl)} | {action} |")
    out.append("")

# Older Conferences (pre-Sonata, from erlang-factory.com census)
def fbrand(e):
    n = norm(e.get("name")) + " " + norm(e.get("url"))
    if "code beam" in n or "codebeam" in n:
        return None  # already covered in modern sections
    if "user conference" in n or "/euc" in n or "euc2" in n:
        return "Erlang User Conference"
    if "lite" in n:
        return "Factory Lite"
    if "factory" in n or "sfbay" in n or "/london20" in n:
        return "Erlang Factory"
    return "Other"

groups = {"Erlang Factory": [], "Erlang User Conference": [], "Factory Lite": [], "Other": []}
skipped = 0
for e in factory:
    b = fbrand(e)
    if b is None:
        skipped += 1
        continue
    groups[b].append(e)

out.append("## Older Conferences (pre-Sonata, erlang-factory.com era)")
out.append("")
out.append("Per the migration decision these all go into a single \"Older Conferences\"")
out.append("section at the end of /conferences/, not under the modern brands. Live editions")
out.append("(2014-2018) are static single-page sites and can be scraped directly; 2009-2013")
out.append("editions return 403 on the live server and must come from the Wayback Machine")
out.append("(speaker and programme pages are all in the CDX index). Dates below come from")
out.append("the census; `null` year means the archived page does not state one.")
out.append("")
total = 0
for b, es in groups.items():
    if not es:
        continue
    es.sort(key=lambda e: (-(e.get("year") or 0), norm(e.get("name"))))
    out.append(f"### {b}")
    out.append("")
    out.append("| Edition | Year | City | URL | Live? | Speakers/Schedule | Source |")
    out.append("|---|---|---|---|---|---|---|")
    for e in es:
        total += 1
        live = e.get("live_status")
        live = "200" if live == 200 else (str(live) if live else "wayback-only")
        ss = f"{'yes' if e.get('has_speakers') else '?'}/{'yes' if e.get('has_schedule') else '?'}"
        out.append(
            f"| {html.unescape(e.get('name') or '(unnamed)')} | {e.get('year') or 'null'} "
            f"| {e.get('city') or 'null'} | {e.get('url')} | {live} | {ss} "
            f"| {e.get('source_of_info') or 'null'} |")
    out.append("")

# Appendix: thematic playlists
out.append("## Appendix: thematic YouTube playlists (not edition-specific)")
out.append("")
out.append("Kept for the future videos section; may contain talks from lost editions.")
out.append("")
for p in playlists:
    if p.get("mapped_conference") is None:
        n = p.get("video_count")
        out.append(f"- [{html.unescape(p['title'])}]({p['url']})" + (f" ({n} videos)" if n else ""))
out.append("")

out.append("## Hub repo data fixes needed (found during inventory)")
out.append("")
out.append("- Broken `conference_brand` references (point at nonexistent brand files):")
out.append("  `cbl-amsterdam-2018.md` -> cbl.md, `sample-conference-3.md` -> code-beam-v.md,")
out.append("  `elixirconf-us-2025.md` -> elixirconf-us.md. This is why brand sections render empty.")
out.append("- Delete the three `sample-conference*.md` placeholder files.")
out.append("- `cbl-amsterdam-2018.md` has no `conference_init_date` (breaks date sorting).")
out.append("- Stale `past: false` on conferences that have happened (as of 2026-07):")
out.append("  code-beam-europe-2025, elixirconf-us-2025, mq-summit-2025.")
out.append("- Missing brand files needed: older-conferences (new section), elixirconf-us,")
out.append("  elixirconf-eu, lambda-days; rename/align cbl vs code-beam-lite.")
out.append("- Most editions in this inventory have no hub entry yet (~19 real entries vs")
out.append("  ~115 editions); creating them is the bulk of the hub-side listing work.")
out.append("")

out.append("## Open questions")
out.append("")
out.append("1. DECIDED: MQ Summit + RabbitMQ Summit are one brand section on the listing.")
out.append("   The RabbitMQ era ran on another platform - rabbitmqsummit.com is the canonical")
out.append("   reference (per-year pages 2018-2024 all alive); current era is mq-summit-page.")
out.append("2. DECIDED: create esl/code-mesh and esl/code-elixir-ldn on the ESL GitHub for")
out.append("   those brands' archives.")
out.append("3. DECIDED: Code BEAM Lite orphan-city editions go into ONE shared new repo,")
out.append("   esl/code-beam-lite (archives/<city_year>/); Stockholm/NYC/London keep their")
out.append("   own existing repos.")
out.append("4. DECIDED: partner-run editions are listed and added as they happen (upcoming ->")
out.append("   hub banner, then into their brand section once past). Remaining work: add")
out.append("   Code BEAM Corunha 2024 (and verify any other partner editions we have not")
out.append("   spotted), and confirm Code BEAM Brasil 2020's site behind codebeambr.com.")
out.append("5. DECIDED: mirror the five archive.elixirconf.eu editions (2015-2019) into")
out.append("   elixirconf-eu-jekyll archives/ while the legacy host is still up.")
out.append("6. EUC 2016 tile on the live site links to erlang-factory.com/sfbay2016 (wrong")
out.append("   event) - do not carry the link over; the census has the right EUC pages.")
out.append("7. RESOLVED: ElixirConf Brasil 2026 (first edition, Nov 2026, Curitiba & online)")
out.append("   lives at elixirconf.com.br, partner-run. The esl/elixirconf-brasil repo is a")
out.append("   stale EU fork (CNAME still points at www.elixirconf.eu) - clean up or retire it.")
out.append("")

path = D.parent / "INVENTORY.md"
path.write_text("\n".join(out), encoding="utf-8")
print(f"wrote {path} ({len(out)} lines, {total} older-conference rows, {skipped} EF rows skipped as modern)")
