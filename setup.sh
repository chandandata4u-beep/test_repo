#!/bin/bash

echo "Installing pre-commit..."
pip install pre-commit

echo "Installing git hooks..."
pre-commit install

echo "Installing pre-commit hook types..."
pre-commit install --hook-type pre-commit

echo "Done. Hooks enabled."