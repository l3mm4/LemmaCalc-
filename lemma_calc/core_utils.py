import os
import sys
import argparse
import pydoc

HISTORY_FILE = "history.json"
VERSION = "0.5"


def show_doc(filename):
    """
    Displays documentation from the docs/ directory using a pager.
    Works regardless of where the script is run from.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    docs_path = os.path.join(base_dir, "..", "docs", filename)
    try:
        with open(docs_path, "r") as f:
            content = f.read()
            pydoc.pager(content)
    except FileNotFoundError:
        print(f"Documentation file '{filename}' not found at {docs_path}.")


def handle_command_line_args():
    parser = argparse.ArgumentParser(
        description="LemmaCalc™ - A Python-powered CLI calculator"
    )
    parser.add_argument("--man", action="store_true", help="Show the man page")
    parser.add_argument("--tldr", action="store_true", help="Show the TLDR guide")
    parser.add_argument(
        "--version", action="store_true", help="Show the program version"
    )
    args = parser.parse_args()

    if args.man:
        show_doc("man.txt")
        sys.exit(0)
    elif args.tldr:
        show_doc("tldr.txt")
        sys.exit(0)
    elif args.version:
        print(f"LemmaCalc™ version {VERSION}")
        sys.exit(0)
