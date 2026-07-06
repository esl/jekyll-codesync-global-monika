# Code Sync → Jekyll migration prompt (codesync-migration.v2)

## Purpose

Migrate codesync.global — currently served by an obsolete Sonata (PHP) CMS — to a
static Jekyll site hosted on GitHub, continuing the work started in
https://github.com/esl/jekyll-codesync-global-monika. The domain codesync.global
is KEPT and will point at the new site. The site's single primary job is to
promote upcoming Code Sync conferences; its secondary job is to be a complete,
accurate index of past conferences.

Everything produced by this migration is a **static site**: Jekyll builds plain
HTML/CSS/JS at build time, GitHub Pages serves the files. No server-side code,
no database, no admin panel. Content edits happen via git. Nothing dynamic
survives except optional client-side JavaScript, and even that is avoided for
archival content.

## Repo strategy

- THIS repo is the hub only: upcoming conferences, the all-conferences listing,
  brand pages, and links out to per-brand sites. No full conference sub-sites
  live here.
- ESL's established convention (verify on github.com/esl) is one Jekyll repo per
  conference brand with its own domain via CNAME and past editions under
  `archives/<city_year>/` (e.g. code-beam-europe/archives/berlin_2024). Existing
  brand repos include: code-beam-europe, code-beam-america, code-beam-stockholm,
  code-beam-mexico, code-beam-nyc, code-beam-london, code-beam-vancouver,
  elixirconf-eu-jekyll, virtual-elixirconf-eu-jekyll, elixirconf-us,
  elixirconf-brasil.
- Conferences currently hosted inside the CMS are extracted OUT:
  - brand already has a repo → add the edition under that repo's `archives/`
  - no brand repo → create one modeled on code-beam-europe's structure
- Expect the migration to produce commits/PRs across multiple ESL repos, not
  just this one.

## Inputs

- The hub Jekyll repo (local working copy) — analyse existing layouts, data
  files and conventions before adding anything; extend them, don't
  parallel-build.
- The live site https://codesync.global/ — read-only source of truth for
  content that still exists; it will be decommissioned.
- Conference sub-sites hosted inside the CMS (schedules, speaker pages, photos).
- External schedule providers used by some conferences: Whova and/or Sessionize.
- Code Sync YouTube channel + playlists — data source for the future videos
  section, and the only surviving record of some lost conferences (e.g.
  Elixir LDN).
- The Wayback Machine — fallback source for lost conference pages.
- The existing ESL brand repos — both as the structural template and as
  migration targets.

## Scope

IN:

1. Upcoming conferences prominently featured (the site's main goal).
2. /conferences/ page listing ALL past conferences, grouped into brand sections
   (as on the current site), each section ordered most-recent-first. Exactly
   ONE canonical listing: the main-nav "all conferences" link and the banner
   "all past conferences" link must resolve to the same page with the same
   ordering.
3. Extraction of CMS-hosted conference sub-sites into brand repos (see Repo
   strategy):
   - speaker sections including speaker photos (download and commit the assets)
   - schedule/agenda sections rebuilt as native static HTML/Liquid — extract
     the Whova/Sessionize/CMS data and render it, don't embed iframes
4. YouTube DATA capture during the inventory pass: for every conference,
   record its playlist URL (and where cheap, the video list: title, speaker,
   video ID) in the hub's conference data. This feeds the future videos
   section; the section itself is NOT built yet.
5. Reconstruction of lost conferences where feasible (YouTube playlists,
   Wayback Machine). A reconstructed page shows only what the sources support.

OUT (do not build):

- Blog posts or articles of any kind.
- Hosted/iframed video archive pages.
- Registration/ticketing sections of migrated conferences.
- The videos-section UI — awaiting design. Only the underlying data is in
  scope.

## Tasks to VERIFY before building (do not trust this description)

- The reported discrepancy: on the live site, the "all conferences" nav link
  and the banner "all past conferences" link allegedly show different
  conference ORDERING. Confirm on the live site and document what each
  actually shows before fixing.
- Which conferences are CMS-hosted vs. already in a brand repo vs. lost.
  Produce the inventory (see Output) before migrating anything.
- For each conference with a schedule: whether it uses Whova, Sessionize, or
  bespoke CMS markup, and whether the data is still retrievable.
- The exact structure of a brand repo's `archives/` edition before creating
  new ones — copy the convention, don't approximate it.

## Output

- Commits to the hub repo following its existing structure and conventions;
  conference content as structured data (front matter / `_data`), not
  hard-coded HTML sections — the CMS's hard-coded sections are what we're
  escaping.
- Branches/PRs to brand repos for extracted archive editions.
- A migration inventory (markdown file in the hub repo) listing every
  conference with: brand, year, status
  (migrated-to-\<repo\> | partial | lost | reconstructed-from-\<source\>),
  schedule source (whova/sessionize/cms/none), YouTube playlist URL or "none",
  and what's missing for partial ones.
- For anything reconstructed: a note in front matter recording the source.

## Constraints

- NEVER invent conference data — no guessed dates, speaker names, talk titles,
  or bios. Missing fields are null/omitted and recorded in the inventory.
- Don't destroy or rewrite existing work in any repo without flagging it first.
- Downloaded assets (speaker photos) are committed to the target repo, not
  hot-linked to the CMS (it's going away).
- Preserve the current site's brand grouping on /conferences/.
- The domain persists, so old codesync.global URLs will otherwise 404: keep
  high-traffic paths stable where practical, and produce a list of old→new
  URL mappings for anything that moves (for redirects or an updated 404 page).
- Don't push to brand-repo default branches — PRs only, they're live sites.

## Errors / edge cases

- Live page unreachable or schedule data gone → mark the conference `partial`
  or `lost` in the inventory with the reason; move on, don't stall.
- Whova/Sessionize data behind JS or auth → report which conferences are
  affected and what access is needed; don't scrape around auth walls.
- Speaker photo missing → ship the speaker entry without a photo, list it in
  the inventory; no placeholder stock images.
- Ambiguous brand assignment or conference identity → ask, don't guess.
- No write access to a brand repo → prepare the changes in a branch/patch and
  flag it, don't silently skip.
