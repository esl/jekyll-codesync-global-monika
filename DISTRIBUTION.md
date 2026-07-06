# CMS snapshot distribution plan

Companion to MIGRATION.md and INVENTORY.md. Covers moving the 22 extracted
CMS conference snapshots into their target ESL repos. All 22 are extracted,
audited, and content-complete (0 download failures, 0 missing local assets);
see the CMS-extraction audit summary at the bottom.

## Status: new repos created; new-repo push scripted & dry-run-verified

UPDATE 2026-07-06: the three new repos exist and are empty
(esl/code-beam-lite, esl/code-mesh, esl/code-elixir-ldn). Their 13 editions are
scripted in `migration-data/distribute_new_repos.sh` (dry-run verified: correct
repo/dir mapping, all snapshot sources present). RUN IT IN AN AUTHENTICATED
TERMINAL:  `bash migration-data/distribute_new_repos.sh`  (or `DRY_RUN=1 bash
...` to preview). The 9 editions for the existing repos (code-beam-america,
code-beam-stockholm) still go via the PR flow below. CNAME/DNS still pending
sysadmin.

## Status: PREPARED, blocked on GitHub write access

This automation session has **no GitHub write access**: no `gh` CLI, and the
macOS keychain is unreadable headlessly (`git push` → "could not read
Username ... Device not configured"). So it cannot create the new repos or push
branches. Everything below is prepared so an authenticated user (or session)
can execute it mechanically. Per MIGRATION.md: PRs only, never push to a
brand-repo default branch.

## Where the snapshots are

Session scratchpad: `<scratchpad>/snapshots/<slug>/` (temporary, git-ignored,
regenerable). Each is a self-contained static folder: `index.html`,
`speaker/<name>/index.html`, `media/<slides>/index.html`, `assets/...`,
`REPORT.txt`. **Regenerate at distribution time** with the current
`migration-data/extract_cms.py` (now includes nav-hardening — see below) on a
stable connection:

```
python3 migration-data/extract_cms.py <all 22 slugs> --out <dir>
```

The tool is idempotent (skips already-downloaded assets), so an interrupted run
resumes safely by re-invoking with the same args.

## Convention finding (how existing archives are built)

Existing archives — `code-beam-europe/archives/berlin_2023`,
`code-beam-america/archives/CBA_2024` — are **full-site wget-style mirrors**:
the entire site chrome (participants/, talks/, keynotes/, nav pages) duplicated
per edition, with root-relative links and the repo's own CNAME.

These snapshots are **leaner and self-contained** instead: the conference page
plus its speaker and slide subpages, assets localized to relative `assets/`
paths (works offline), and cross-site hub nav links (`/about-us/`,
`/sponsorship/`, etc.) rewritten to absolute `https://codesync.global/...` so
they still resolve when served from a different domain. Internal folder names
follow the CMS URL structure (`speaker/`, `media/`) rather than the Jekyll
site's (`participants/`, `talks/`).

DECISION NEEDED: accept the leaner self-contained format (recommended — renders
anywhere, no dependence on a live CMS), or re-capture as full-site mirrors to
match the existing archives exactly.

## Target mapping

Existing repos — drop each snapshot into the repo's archive dir (note:
`code-beam-america` uses `archives/`, `code-beam-stockholm` uses `archive/`
singular). Proposed edition dir names follow each repo's existing scheme;
**confirm naming before pushing.**

| Snapshot slug | Real edition | Target repo | Proposed archive dir |
|---|---|---|---|
| code-beam-sf-2018 | Code BEAM SF 2018 | code-beam-america | archives/sf_2018 |
| code-beam-sf-2019 | Code BEAM SF 2019 | code-beam-america | archives/sf_2019 |
| code-beam-sf | Code BEAM SF 2020 | code-beam-america | archives/sf_2020 |
| code-beam-v-america-2021 | Code BEAM V America 2021 (Mar) | code-beam-america | archives/v_america_mar_2021 |
| code-beam-sf-2021 | Code BEAM America 2021 (Nov) | code-beam-america | archives/america_nov_2021 |
| code-beam-sto-2019 | Code BEAM STO 2019 | code-beam-stockholm | archive/may_2019 |
| code-beam-sto | Code BEAM STO 2020 (Sep) | code-beam-stockholm | archive/september_2020 |
| code-beam-sto-2021 | Code BEAM STO 2021 (May) | code-beam-stockholm | archive/may_2021 |
| code-beam-sto-2022 | Code BEAM Europe 2022 (STO) | code-beam-stockholm | archive/may_2022 |

New repos — create first (see below), then add editions:

| Snapshot slug | Real edition | Target repo (NEW) | Proposed archive dir |
|---|---|---|---|
| code-beam-lite-berlin-2018 | Lite Berlin 2018 | code-beam-lite | archives/berlin_2018 |
| cbl-amsterdam-2018 | Lite Amsterdam 2018 | code-beam-lite | archives/amsterdam_2018 |
| cbl-munich-2018 | Lite Munich 2018 | code-beam-lite | archives/munich_2018 |
| code-beam-lite-italy | Lite Italy 2019 | code-beam-lite | archives/italy_2019 |
| code-beam-lite-budapest | Lite Budapest 2019 | code-beam-lite | archives/budapest_2019 |
| code-beam-lite-berlin-2019 | Lite Berlin 2019 | code-beam-lite | archives/berlin_2019 |
| code-beam-lite-india | Lite India 2019 (partial) | code-beam-lite | archives/india_2019 |
| code-beam-lite-amsterdam | Lite Amsterdam 2019 | code-beam-lite | archives/amsterdam_2019 |
| code-beam-lite-virtual | Lite Virtual 2020 | code-beam-lite | archives/virtual_2020 |
| code-mesh-2018 | Code Mesh LDN 2018 | code-mesh | archives/ldn_2018 |
| code-mesh-ldn-2019 | Code Mesh LDN 2019 | code-mesh | archives/ldn_2019 |
| code-mesh-ldn | Code Mesh V 2020 | code-mesh | archives/ldn_2020 |
| code-elixir-ldn-2019 | Code Elixir LDN 2019 | code-elixir-ldn | archives/ldn_2019 |

## New repos to create (needs auth + decisions)

- **esl/code-beam-lite** — orphan Lite cities. No single live domain. CNAME
  DECISION: new subdomain (e.g. lite-archive.codesync.global), a path under an
  existing domain, or github.io default.
- **esl/code-mesh** — brand retired. codemesh.io still alive (2016/2017);
  CNAME could be codemesh.io if that domain is under ESL control and repointed.
- **esl/code-elixir-ldn** — brand retired; elixir.london DNS is dead. CNAME
  DECISION needed (new subdomain or github.io).

Model each new repo on an existing one's serving setup (static files + Pages).
Since snapshots are self-contained static HTML, the repo needs no Jekyll build —
just the `archives/<edition>/` folders + CNAME + Pages enabled.

## Per-edition push steps (for the authenticated operator)

For existing repos (example, code-beam-america):

```
git clone https://github.com/esl/code-beam-america.git
cd code-beam-america
git checkout -b archive-cms-editions
cp -R <snapshots>/code-beam-sf-2018   archives/sf_2018
cp -R <snapshots>/code-beam-sf-2019   archives/sf_2019
# ... etc for this repo's rows
git add archives && git commit -m "Add CMS-era archive editions"
git push -u origin archive-cms-editions
# open PR against default branch
```

For new repos: create the repo, add a CNAME + README, then the same
`cp -R` of each edition into `archives/`, commit, push, enable Pages.

## Remaining manual cleanup before/after pushing

- **code-mesh-ldn**: one inline "buy your ticket on Eventbrite" text link with a
  dead 2020 URL in prose (not caught by section-level stripping). Snip by hand.
- Verify a couple of pushed archives render on Pages (Pages path-serving vs the
  relative asset paths — should work since assets are relative, but confirm).

## Hub-side follow-up (separate from brand repos)

After archives are live, add/point hub `/conferences/` entries for these
editions (most have no `_conferences/*.md` yet — INVENTORY.md "Hub repo data
fixes" section). Extracted editions link out to their new archive URLs, matching
how ElixirConf EU / Lambda Days rows already link out.

## CMS-extraction audit summary (2026-07-06)

22/22 conferences extracted. 0 download failures, 0 failed subpages, 0 missing
local assets (every speaker photo, bio, schedule, slide PDF, css/js/font, and
the ckeditor syntax-highlighter resolves). Strip rules verified: only
registration/ticket/newsletter/cookie sections and Eventbrite/analytics scripts
removed. code-beam-lite-india correctly has no schedule (its CMS page was never
built out). Visual spot-checks (Code BEAM Lite Italy, Code Mesh 2018) render
offline faithfully with schedules, speaker photos, talk-page video embeds, and
working slide downloads.
