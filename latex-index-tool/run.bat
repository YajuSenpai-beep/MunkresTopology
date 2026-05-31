@echo off
REM LaTeX Index Tool — quick launcher
REM Usage: run.bat insert --chapter 1 --dry-run
REM        run.bat parse index.txt -o entries.json
cd /d "%~dp0.."
python -m index.latex_index.cli %*
