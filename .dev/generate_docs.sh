#!/bin/bash

# Documentation Generation Script for OpenPanel Docker Module

set -e

echo "Setting up documentation environment..."

# Install required packages

echo "Generating documentation..."

# Create docs directory if it doesn't exist
mkdir -p docs/_static docs/_templates

# Generate API documentation
cd docs
sphinx-build -b html . _build/

echo "Documentation generated successfully!"
echo "Open docs/_build/index.html to view the documentation"

# Optional: Start auto-build server
read -p "Start auto-build server? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Starting auto-build server on http://localhost:8000"
    sphinx-autobuild . _build/ --host 0.0.0.0 --port 8000
fi