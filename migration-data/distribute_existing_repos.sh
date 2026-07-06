#!/usr/bin/env bash
# Stage CMS snapshots into the two EXISTING live brand repos via a PULL REQUEST.
#
# These repos are LIVE (MIGRATION.md: never push to their default branch). This
# script clones each, creates a branch, copies the mapped snapshots into the
# repo's archive dir, commits, and pushes THE BRANCH. It then prints the URL to
# open the PR — you review + merge on GitHub.
#
# Run in YOUR authenticated terminal (the automation session can't push).
#   DRY_RUN=1 bash distribute_existing_repos.sh   # preview, no clone/push
#   bash distribute_existing_repos.sh             # clone, branch, commit, push branch
#
# Naming note: the archive-dir names below are proposed; because this goes via PR
# you can rename before merging, or edit the MAP here first. code-beam-america
# uses archives/ (plural); code-beam-stockholm uses archive/ (singular).
set -euo pipefail

SNAP_DIR="${SNAP_DIR:-/private/tmp/claude-501/-Users-monika-Documents-jekyll-codesync-global-monika/f696939e-4b77-46ca-bf6d-d51b0746ebb6/scratchpad/snapshots}"
WORK="${WORK:-$(mktemp -d)}"
BRANCH="${BRANCH:-archive-cms-editions}"
DRY_RUN="${DRY_RUN:-0}"

# repo|archive_base|snapshot_slug|archive_dir
MAP="
code-beam-america|archives|code-beam-sf-2018|sf_2018
code-beam-america|archives|code-beam-sf-2019|sf_2019
code-beam-america|archives|code-beam-sf|sf_2020
code-beam-america|archives|code-beam-v-america-2021|v_america_mar_2021
code-beam-america|archives|code-beam-sf-2021|america_nov_2021
code-beam-stockholm|archive|code-beam-sto-2019|may_2019
code-beam-stockholm|archive|code-beam-sto|september_2020
code-beam-stockholm|archive|code-beam-sto-2021|may_2021
code-beam-stockholm|archive|code-beam-sto-2022|may_2022
"

run() { if [ "$DRY_RUN" = "1" ]; then echo "  DRY: $*"; else eval "$*"; fi; }

for repo in code-beam-america code-beam-stockholm; do
  echo "=== $repo ==="
  dir="$WORK/$repo"
  if [ "$DRY_RUN" = "1" ]; then
    echo "  DRY: git clone --depth 1 https://github.com/esl/$repo.git $dir"
    echo "  DRY: git -C $dir checkout -b $BRANCH"
  else
    git clone --depth 1 "https://github.com/esl/$repo.git" "$dir"
    git -C "$dir" checkout -b "$BRANCH"
  fi

  count=0
  while IFS='|' read -r r base slug adir; do
    [ "$r" = "$repo" ] || continue
    src="$SNAP_DIR/$slug"
    if [ ! -d "$src" ]; then echo "  MISSING snapshot: $src" >&2; exit 1; fi
    dest="$dir/$base/$adir"
    if [ "$DRY_RUN" != "1" ] && [ -e "$dest" ]; then
      echo "  SKIP (already exists in repo): $base/$adir" ; continue
    fi
    echo "  + $base/$adir  (from $slug)"
    run "mkdir -p '$dir/$base'"
    run "cp -R '$src' '$dest'"
    count=$((count+1))
  done <<< "$MAP"

  run "git -C '$dir' add -A"
  run "git -C '$dir' commit -m 'Add CMS-era archive editions ($count)'"
  run "git -C '$dir' push -u origin '$BRANCH'"
  echo "  branch pushed. Open a PR:"
  echo "    https://github.com/esl/$repo/pull/new/$BRANCH"
done

echo
[ "$DRY_RUN" = "1" ] && echo "(DRY RUN — nothing cloned/committed/pushed)"
echo "After merging: enable/confirm the editions render, then add hub /conferences/"
echo "entries pointing at the new archive URLs (see INVENTORY.md)."
