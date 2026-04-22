#!/bin/zsh
# Build the Sphinx documentation for the current melody engine.

set -e

echo "Activating venv..."
source ../.venv/bin/activate

echo "Building documentation..."
make clean html

echo "Documentation built at docs/_build/html/index.html"
