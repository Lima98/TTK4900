#!/bin/zsh
# Build and publish the thesis archive/documentation to GitHub Pages.

set -euo pipefail

SCRIPT_DIR="${0:A:h}"
ROOT_DIR="${SCRIPT_DIR:h}"
REMOTE="${PAGES_REMOTE:-origin}"
PAGES_BRANCH="${PAGES_BRANCH:-gh-pages}"
WORKTREE="${PAGES_WORKTREE:-${ROOT_DIR:h}/TTK4900-gh-pages}"
DEFAULT_MESSAGE="Deploy thesis website $(date '+%Y-%m-%d %H:%M')"
COMMIT_MESSAGE="${1:-}"

if [[ -z "$COMMIT_MESSAGE" ]]; then
    if [[ -t 0 ]]; then
        echo -n "Commit message [$DEFAULT_MESSAGE]: "
        read -r COMMIT_MESSAGE
    fi
    COMMIT_MESSAGE="${COMMIT_MESSAGE:-$DEFAULT_MESSAGE}"
fi

echo "Building thesis PDF and LaTeX references..."
cd "$ROOT_DIR/thesis/latex"
latexmk -pdf -interaction=nonstopmode main.tex

echo "Building archive page from thesis examples..."
cd "$SCRIPT_DIR"
python3 build_archive.py

echo "Building documentation..."
cd "$ROOT_DIR/docs"
./build_docs.zsh

echo "Preparing GitHub Pages worktree at $WORKTREE..."
cd "$ROOT_DIR"
if [[ -e "$WORKTREE/.git" || -f "$WORKTREE/.git" ]]; then
    git -C "$WORKTREE" checkout "$PAGES_BRANCH"
elif git show-ref --verify --quiet "refs/heads/$PAGES_BRANCH"; then
    git worktree add "$WORKTREE" "$PAGES_BRANCH"
elif git ls-remote --exit-code --heads "$REMOTE" "$PAGES_BRANCH" >/dev/null 2>&1; then
    git fetch "$REMOTE" "$PAGES_BRANCH:$PAGES_BRANCH"
    git worktree add "$WORKTREE" "$PAGES_BRANCH"
else
    git worktree add --detach "$WORKTREE" HEAD
    git -C "$WORKTREE" checkout --orphan "$PAGES_BRANCH"
fi

if [[ "$WORKTREE" == "$ROOT_DIR" || "$WORKTREE" == "/" ]]; then
    echo "Refusing to publish into unsafe worktree path: $WORKTREE"
    exit 1
fi

echo "Replacing static site contents..."
find "$WORKTREE" -mindepth 1 -maxdepth 1 ! -name ".git" -exec rm -rf {} +
mkdir -p "$WORKTREE/docs" "$WORKTREE/thesis" "$WORKTREE/thesis-examples"
cp -f "$ROOT_DIR/webpage/index.html" "$WORKTREE/index.html"
cp -f "$ROOT_DIR/thesis/latex/main.pdf" "$WORKTREE/thesis/main.pdf"
rsync -a --delete "$ROOT_DIR/docs/_build/html/" "$WORKTREE/docs/"
rsync -a --delete "$ROOT_DIR/thesis/latex/examples/" "$WORKTREE/thesis-examples/"
touch "$WORKTREE/.nojekyll"

echo "Committing site update..."
git -C "$WORKTREE" add -A
if git -C "$WORKTREE" diff --cached --quiet; then
    echo "No GitHub Pages changes to commit."
else
    git -C "$WORKTREE" commit -m "$COMMIT_MESSAGE"
fi

echo "Pushing $PAGES_BRANCH to $REMOTE..."
git -C "$WORKTREE" push "$REMOTE" "$PAGES_BRANCH"

echo "GitHub Pages deploy complete."
echo "If this is the first deploy, enable Pages in GitHub settings: Deploy from branch '$PAGES_BRANCH' / root."
