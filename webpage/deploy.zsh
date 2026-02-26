#!/bin/zsh
# Firstly enable NTNU-VPN
# Connect to smb://webedit.ntnu.no/janoivil through finder
# (Check name of the mounted drive, here we assume it is janoivil)
# Then run this script from the webpage/ directory

exec > >(tee -a deploy.log) 2>&1

VOLUME_PATH="/Volumes/janoivil/"
if [ ! -d "$VOLUME_PATH" ]; then
    echo "Error: $VOLUME_PATH is not mounted. Please connect to smb://webedit.ntnu.no/janoivil through finder and try again.\n"
    exit 1
fi

echo "Mounted drive found: $VOLUME_PATH\n"

echo "Activating venv...\n"
source ../.venv/bin/activate
echo "Done!\n"

# Updating documentation
cd ../docs/
./build_docs.sh

echo "Building documentation...\n"
make html
cd ../webpage/
echo "Done!\n"

echo "Copying index.html to /Volumes/janoivil/\n"
cp -f index.html /Volumes/janoivil/
echo "Done!\n"
echo "Copying docs/ to /Volumes/janoivil/docs/\n"
rsync -a ../docs/ /Volumes/janoivil/docs/
echo "Done!\n"
