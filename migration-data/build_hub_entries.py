#!/usr/bin/env python3
"""Generate hub _conferences/*.md link-out entries for past editions that are
archived on stable external URLs (Lambda Days, ElixirConf EU, Code Mesh, and the
already-archived Code BEAM Europe editions).

Scope (deliberately conservative): only editions with BOTH a confirmed date and
a verified-live stable URL are emitted here. Editions whose dates still need
verifying (RabbitMQ Summit, 2025+ editions) or whose archive URL depends on
pending new-repo/domain decisions (the CMS-extracted editions) are NOT emitted
by this script — add them once those are settled.

Idempotent: never overwrites an existing _conferences/*.md; creates the two new
brand files (lambda-days, elixirconf-eu) only if missing. Re-run safely:
    python3 migration-data/build_hub_entries.py
Data provenance: dates/locations from INVENTORY.md (sourced from the live
codesync.global listing); URLs verified live 2026-07-06.
"""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONF = ROOT / "_conferences"
BRANDS = ROOT / "_conference_brands"

NEW_BRANDS = {
    "lambda-days": ("Lambda Days",
        "Lambda Days is the functional programming conference for the Erlang, "
        "Elixir and wider FP community, held annually in Kraków."),
    "elixirconf-eu": ("ElixirConf EU",
        "ElixirConf EU is the major European conference for the Elixir language "
        "and the Phoenix framework."),
}

# (slug, brand, title, init_date YYYY-MM-DD, display dates, location, external_url)
EDITIONS = [
    # Lambda Days — all Kraków; 2025 at root URL is deferred (date unverified)
    ("lambda-days-2024", "lambda-days", "Lambda Days 2024", "2024-05-27", "27-28 MAY 2024", "Kraków", "https://www.lambdadays.org/lambdadays2024"),
    ("lambda-days-2023", "lambda-days", "Lambda Days 2023", "2023-06-05", "5-6 JUNE 2023", "Kraków", "https://www.lambdadays.org/lambdadays2023"),
    ("lambda-days-2022", "lambda-days", "Lambda Days 2022", "2022-07-28", "28-29 JULY 2022", "Kraków", "https://www.lambdadays.org/lambdadays2022"),
    ("lambda-days-2021", "lambda-days", "Lambda Days 2021", "2021-02-17", "17-18 FEBRUARY 2021", "Kraków", "https://www.lambdadays.org/lambdadays2021"),
    ("lambda-days-2020", "lambda-days", "Lambda Days 2020", "2020-02-13", "13-14 FEBRUARY 2020", "Kraków", "https://www.lambdadays.org/lambdadays2020"),
    ("lambda-days-2019", "lambda-days", "Lambda Days 2019", "2019-02-14", "14-15 FEBRUARY 2019", "Kraków", "https://www.lambdadays.org/lambdadays2019"),
    ("lambda-days-2018", "lambda-days", "Lambda Days 2018", "2018-02-22", "22-23 FEBRUARY 2018", "Kraków", "https://www.lambdadays.org/lambdadays2018"),
    ("lambda-days-2017", "lambda-days", "Lambda Days 2017", "2017-02-09", "9-10 FEBRUARY 2017", "Kraków", "https://www.lambdadays.org/lambdadays2017"),
    ("lambda-days-2016", "lambda-days", "Lambda Days 2016", "2016-02-25", "25-26 FEBRUARY 2016", "Kraków", "https://www.lambdadays.org/lambdadays2016"),
    ("lambda-days-2015", "lambda-days", "Lambda Days 2015", "2015-02-26", "26-27 FEBRUARY 2015", "Kraków", "https://www.lambdadays.org/lambdadays2015"),
    ("lambda-days-2014", "lambda-days", "Lambda Days 2014", "2014-02-27", "27-28 FEBRUARY 2014", "Kraków", "https://www.lambdadays.org/lambdadays2014"),
    # ElixirConf EU
    ("elixirconf-eu-2024", "elixirconf-eu", "ElixirConf EU 2024", "2024-04-18", "18-19 APRIL 2024", "Lisbon", "https://www.elixirconf.eu/archives/lisbon_2024/index.html"),
    ("elixirconf-eu-2023", "elixirconf-eu", "ElixirConf EU 2023", "2023-04-20", "20-21 APRIL 2023", "Lisbon", "https://www.elixirconf.eu/archives/lisbon_2023/index.html"),
    ("elixirconf-eu-2022", "elixirconf-eu", "ElixirConf EU 2022", "2022-06-09", "9-10 JUNE 2022", "London", "https://www.elixirconf.eu/archives/london_2022/index.html"),
    ("elixirconf-eu-2021", "elixirconf-eu", "ElixirConf EU 2021", "2021-09-09", "9-10 SEPTEMBER 2021", "Warsaw", "https://www.elixirconf.eu/archives/warsaw_2021/index.html"),
    ("elixirconf-eu-virtual-x-2020", "elixirconf-eu", "ElixirConf EU Virtual X 2020", "2020-10-07", "7-8 OCTOBER 2020", "Virtual", "https://www.elixirconf.eu/archives/virtual_x_2020/index.html"),
    ("elixirconf-eu-virtual-2020", "elixirconf-eu", "ElixirConf EU Virtual VI 2020", "2020-06-18", "18-19 JUNE 2020", "Virtual", "https://www.elixirconf.eu/archives/virtual_2020/index.html"),
    ("elixirconf-eu-2019", "elixirconf-eu", "ElixirConf EU 2019", "2019-04-08", "8-9 APRIL 2019", "Prague", "http://www.archive.elixirconf.eu/elixirconfeu2019"),
    ("elixirconf-eu-2018", "elixirconf-eu", "ElixirConf EU 2018", "2018-04-16", "16-17 APRIL 2018", "Warsaw", "http://www.archive.elixirconf.eu/elixirconfeu2018"),
    ("elixirconf-eu-2017", "elixirconf-eu", "ElixirConf EU 2017", "2017-04-05", "5 APRIL 2017", "Barcelona", "http://www.archive.elixirconf.eu/elixirconf2017"),
    ("elixirconf-eu-2016", "elixirconf-eu", "ElixirConf EU 2016", "2016-05-11", "11-12 MAY 2016", "Berlin", "http://www.archive.elixirconf.eu/elixirconf2016"),
    ("elixirconf-eu-2015", "elixirconf-eu", "ElixirConf EU 2015", "2015-04-23", "23-24 APRIL 2015", "Kraków", "http://www.archive.elixirconf.eu/elixirconf2015"),
    # Code Mesh (older editions still hosted on codemesh.io)
    ("code-mesh-2017", "code-mesh", "Code Mesh LDN 2017", "2017-11-08", "8-9 NOVEMBER 2017", "London", "http://www.codemesh.io/codemesh2017"),
    ("code-mesh-2016", "code-mesh", "Code Mesh LDN 2016", "2016-11-03", "3-4 NOVEMBER 2016", "London", "http://www.codemesh.io/codemesh2016"),
    # Code BEAM Europe editions already archived in esl/code-beam-europe
    ("code-beam-europe-2024", "code-beam-europe", "Code BEAM Europe 2024", "2024-10-14", "14-15 OCTOBER 2024", "Berlin", "https://codebeameurope.com/archives/berlin_2024/index.html"),
    ("code-beam-europe-2023", "code-beam-europe", "Code BEAM Europe 2023", "2023-10-19", "19-20 OCTOBER 2023", "Berlin", "https://codebeameurope.com/archives/berlin_2023/index.html"),
]

ENTRY = """---
conference_brand: _conference_brands/{brand}.md
title: {title}
conference_past_conferences: false
past: true
external_url: "{url}"
bg_image: ''
logo_img: ''
conference_location: "{loc}"
conference_init_date: {date}T09:00:00.000+00:00
conference_dates: "{dates}"
head_title: {title}
---

Archived edition. Full details on the conference site linked above.
"""

BRAND_TMPL = "---\ntitle: {title}\n---\n\n{desc}\n"


def main():
    created_brands, created, skipped = [], [], []
    for slug, (title, desc) in NEW_BRANDS.items():
        f = BRANDS / f"{slug}.md"
        if not f.exists():
            f.write_text(BRAND_TMPL.format(title=title, desc=desc), "utf-8")
            created_brands.append(slug)
    for slug, brand, title, date, dates, loc, url in EDITIONS:
        f = CONF / f"{slug}.md"
        if f.exists():
            skipped.append(slug)
            continue
        f.write_text(ENTRY.format(brand=brand, title=title, url=url,
                                  loc=loc, date=date, dates=dates), "utf-8")
        created.append(slug)
    print(f"brand files created: {created_brands or 'none (all existed)'}")
    print(f"entries created ({len(created)}): {', '.join(created)}")
    if skipped:
        print(f"skipped (already exist) ({len(skipped)}): {', '.join(skipped)}")


if __name__ == "__main__":
    main()
