"""makeindex wrapper: runs makeindex, _fix_ind.py, _fix_bn.py in sequence.

Designed to be called by latexmk as the $makeindex command.
On Windows, cmd.exe doesn't support && chaining; this Python wrapper
solves that by running all three steps in a single process.

Usage (called by latexmk):
    python latex-index-tool/_makeindex.py [makeindex options] -o output.ind input.idx
"""
import os
import subprocess
import sys

TOOL_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(TOOL_DIR)
IST = os.path.join(ROOT, "Topology_by_Munkres.ist")


def main():
    # Pass all arguments through to makeindex, adding the .ist style
    args = ["makeindex", "-s", IST] + sys.argv[1:]
    subprocess.run(args, check=True)

    # Run fix scripts
    subprocess.run(
        ["python", os.path.join(TOOL_DIR, "_fix_ind.py")], check=True
    )
    subprocess.run(
        ["python", os.path.join(TOOL_DIR, "_fix_bn.py")], check=True
    )
    subprocess.run(
        ["python", os.path.join(TOOL_DIR, "_fix_misc.py")], check=True
    )


if __name__ == "__main__":
    main()
