#!/bin/bash
# LaTeX Index Tool — quick launcher
# Usage: ./run.sh insert --chapter 1 --dry-run
#        ./run.sh parse index.txt -o entries.json
cd "$(dirname "$0")/.."
python -m index.latex_index.cli "$@"
