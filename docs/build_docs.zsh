#!/bin/zsh
# This file get automatically run from the deploy.zsh file in ../webpage/

echo "Activating venv..."
source ../.venv/bin/activate
echo "Updating documentation..."
sphinx-apidoc -o docs/source/ code/
echo "Done!"

