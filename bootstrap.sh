#!/usr/bin/env bash
#
# bootstrap.sh — push the decca scaffold to GitHub.
#
# Run this ONCE, from inside the unzipped `decca/` folder:
#     bash bootstrap.sh
#
# It is safe to re-run: it will not clobber an existing history.

set -euo pipefail

REMOTE_URL="https://github.com/LeweeLewee/Decca.git"
BRANCH="main"

# 1. Initialise a repo here if one doesn't exist yet.
if [ ! -d .git ]; then
  git init
fi
git branch -M "$BRANCH"

# 2. Point 'origin' at your GitHub repo (add or update).
if git remote get-url origin >/dev/null 2>&1; then
  git remote set-url origin "$REMOTE_URL"
else
  git remote add origin "$REMOTE_URL"
fi

# 3. Stage and commit the scaffold (skip if there's nothing to commit).
git add .
if ! git diff --cached --quiet; then
  git commit -m "chore: initial project foundation"
else
  echo "Nothing new to commit."
fi

# 4. Reconcile with anything already on GitHub (e.g. a README created at
#    repo-creation time), then push.
git fetch origin "$BRANCH" || true
if git rev-parse --verify --quiet "origin/$BRANCH" >/dev/null; then
  # Remote branch exists: rebase our work on top of it so nothing is lost.
  git pull --rebase origin "$BRANCH" || {
    echo
    echo "Rebase hit a conflict (likely a README/LICENSE already on GitHub)."
    echo "Resolve the conflicted files, then run:"
    echo "    git rebase --continue && git push -u origin $BRANCH"
    exit 1
  }
fi

git push -u origin "$BRANCH"
echo
echo "Done. View it at: https://github.com/LeweeLewee/Decca/tree/main"
