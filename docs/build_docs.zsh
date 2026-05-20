#!/bin/zsh
# Build the Sphinx documentation for the current melody engine.

set -e

echo "Activating venv..."
if [[ -f ../.venv/bin/activate ]]; then
  source ../.venv/bin/activate
else
  echo "No local venv found, using current environment."
fi

echo "Building documentation..."
make clean html

echo "Documentation built at docs/_build/html/index.html"
