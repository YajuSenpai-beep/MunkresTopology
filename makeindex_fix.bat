@echo off
REM makeindex wrapper: runs makeindex then _fix_ind.py
makeindex -s Topology_by_Munkres.ist %*
python latex-index-tool/_fix_ind.py
