#!/bin/zsh
# Firstly enable NTNU-VPN
# Connect to smb://webedit.ntnu.no/janoivil through finder
# (Check name of the mounted drive, here we assume it is janoivil)
# Then run this script from the webpage/ directory

exec > >(tee -a deploy.log) 2>&1
set -e

VOLUME_PATH="/Volumes/janoivil/"
SCRIPT_DIR="${0:A:h}"
ROOT_DIR="${SCRIPT_DIR:h}"
THESIS_DIR="${ROOT_DIR}/thesis/latex"
REBUILD_THESIS=0

if [[ "${1:-}" == "--rebuild-thesis" ]]; then
    REBUILD_THESIS=1
fi

if [ ! -d "$VOLUME_PATH" ]; then
    echo "Error: $VOLUME_PATH is not mounted. Please connect to smb://webedit.ntnu.no/janoivil through finder and try again.\n"
    exit 1
fi

echo "Mounted drive found: $VOLUME_PATH\n"

echo "Activating venv...\n"
source ../.venv/bin/activate
echo "Done!\n"

if [[ "$REBUILD_THESIS" == "1" || ! -f "${THESIS_DIR}/main.aux" || ! -f "${THESIS_DIR}/main.pdf" ]]; then
    echo "Building thesis PDF and LaTeX references...\n"
    cd "${THESIS_DIR}"
    latexmk -pdf -interaction=nonstopmode main.tex
    cd "${SCRIPT_DIR}"
    echo "Done!\n"
else
    echo "Using existing thesis build artifacts from ${THESIS_DIR}.\n"
    echo "Pass --rebuild-thesis if you want to force a fresh LaTeX build.\n"
fi

echo "Building archive page from thesis examples...\n"
python3 build_archive.py
echo "Done!\n"

echo "Building documentation...\n"
cd ../docs/
./build_docs.zsh
cd ../webpage/
echo "Done!\n"

echo "Copying index.html to /Volumes/janoivil/\n"
cp -f index.html /Volumes/janoivil/
echo "Done!\n"
echo "Copying thesis PDF to /Volumes/janoivil/thesis/\n"
mkdir -p /Volumes/janoivil/thesis/
cp -f ../thesis/latex/main.pdf /Volumes/janoivil/thesis/main.pdf
echo "Done!\n"
echo "Copying docs/ to /Volumes/janoivil/docs/\n"
rsync -a ../docs/_build/html/ /Volumes/janoivil/docs/
echo "Done!\n"
echo "Copying output/ to /Volumes/janoivil/output/\n"
rsync -a ../output/ /Volumes/janoivil/output/
echo "Done!\n"
echo "Copying thesis examples to /Volumes/janoivil/thesis-examples/\n"
rsync -a ../thesis/latex/examples/ /Volumes/janoivil/thesis-examples/
echo "Done!\n"
