#!/usr/bin/env python3
"""
MyLang command-line interface
Allows running: python -m mylang [file.mylang]
"""

from main import main
import sys
import os
from pathlib import Path

# Import main from the parent directory
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

if __name__ == '__main__':
    main()
