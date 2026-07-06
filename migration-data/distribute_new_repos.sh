#!/usr/bin/env bash
# Distribute CMS snapshots into the three NEW archive repos.
#
# Run this in YOUR authenticated terminal (the automation session can't push).
# It clones each empty repo, copies the mapped snapshots into archives/<edition>/,
# adds a README, commits, and pushes to the default branch. New repos are empty
# so pushing to the default branch is safe (unlike the existing brand repos,
# which are live — those get PRs, see DISTRIBUTION.md).
#
# Usage:
#   DRY_RUN=1 bash distribute_new_repos.sh     # stage + show, no push (safe test)
#   bash distribute_new_repos.sh               # real run: clones, commits, pushes
#
# Prereqs: snapshots present at $SNAP_DIR (regenerate first if the scratchpad was
# cleared:  python3 migration-data/extract_cms.py <all 22 slugs> --out <dir> ).
# CNAME is intentionally NOT written yet — add it once DNS/subdomains are
# confirmed with the sysadmin (see DISTRIBUTION.md).
set -euo pipefail

SNAP_DIR="${SNAP_DIR:-/private/tmp/claude-501/-Users-monika-Documents-jekyll-codesync-global-monika/f696939e-4b77-46ca-bf6d-d51b0746ebb6/scratchpad/snapshots}"
WORK="${WORK:-$(mktemp -d)}"
DRY_RUN="${DRY_RUN:-0}"

# repo|snapshot_slug|archive_dir  (archive dir names are our choice for new repos)
MAP="
code-beam-lite|code-beam-lite-berlin-2018|berlin_2018
code-beam-lite|cbl-amsterdam-2018|amsterdam_2018
code-beam-lite|cbl-munich-2018|munich_2018
code-beam-lite|code-beam-lite-italy|italy_2019
code-beam-lite|code-beam-lite-budapest|budapest_2019
code-beam-lite|code-beam-lite-berlin-2019|berlin_2019
code-beam-lite|code-beam-lite-india|india_2019
code-beam-lite|code-beam-lite-amsterdam|amsterdam_2019
code-beam-lite|code-beam-lite-virtual|virtual_2020
code-mesh|code-mesh-2018|ldn_2018
code-mesh|code-mesh-ldn-2019|ldn_2019
code-mesh|code-mesh-ldn|ldn_2020
code-elixir-ldn|code-elixir-ldn-2019|ldn_2019
"

run() { if [ "$DRY_RUN" = "1" ]; then echo "  DRY: $*"; else eval "$*"; fi; }

for repo in code-beam-lite code-mesh code-elixir-ldn; do
  echo "=== $repo ==="
  dir="$WORK/$repo"
  if [ "$DRY_RUN" = "1" ]; then
    echo "  DRY: git clone https://github.com/esl/$repo.git $dir"
    mkdir -p "$dir/archives"
  else
    git clone "https://github.com/esl/$repo.git" "$dir"
    mkdir -p "$dir/archives"
  fi

  count=0
  while IFS='|' read -r r slug adir; do
    [ "$r" = "$repo" ] || continue
    src="$SNAP_DIR/$slug"
    if [ ! -d "$src" ]; then echo "  MISSING snapshot: $src" >&2; exit 1; fi
    echo "  + archives/$adir  (from $slug)"
    run "cp -R '$src' '$dir/archives/$adir'"
    count=$((count+1))
  done <<< "$MAP"

  # minimal README so the repo root isn't bare
  readme="$dir/README.md"
  if [ "$DRY_RUN" = "1" ]; then
    echo "  DRY: write $readme ($count editions)"
  else
    {
      echo "# ${repo}"
      echo
      echo "Archive of past ${repo} conference editions, migrated from the"
      echo "codesync.global CMS. Each edition is a self-contained static site"
      echo "under \`archives/\`."
      echo
      echo "## Editions"
      while IFS='|' read -r r slug adir; do [ "$r" = "$repo" ] && echo "- [\`archives/$adir\`](archives/$adir/)"; done <<< "$MAP"
    } > "$readme"
  fi

  run "git -C '$dir' add -A"
  run "git -C '$dir' commit -m 'Add CMS-era conference archives ($count editions)'"
  run "git -C '$dir' push origin HEAD"
  echo "  done: $count editions -> esl/$repo"
done

echo
echo "All new repos populated. Next:"
echo "  1. Enable GitHub Pages on each (default branch root) if not already."
echo "  2. Add CNAME per repo once DNS/subdomains are confirmed."
echo "  3. Existing repos (code-beam-america, code-beam-stockholm): use the PR"
echo "     flow in DISTRIBUTION.md for their 9 editions."
[ "$DRY_RUN" = "1" ] && echo "(DRY RUN — nothing cloned/committed/pushed; staged layout shown above)"
