#!/usr/bin/env python3
"""
MyLang command-line interface
Allows running: python -m mylang [file.mylang]
"""

import sys
import os
from pathlib import Path

# Import main from the root directory
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, root_dir)

from main import main

if __name__ == '__main__':
    main()
