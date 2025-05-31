# run_calc.py

import sys
import os
from lemma_calc.core_utils import handle_command_line_args

# Adds the current directory to sys.path so lemma_calc is found
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from lemma_calc.main import main

if __name__ == "__main__":
    handle_command_line_args()  # Handles --version, --man, --tldr and exits if needed
    main()  # Launch main REPL
