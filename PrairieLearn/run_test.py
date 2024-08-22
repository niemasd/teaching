#! /usr/bin/env python3
'''
Run a Python unittest grading script (test.py) in PrairieLearn. Assumes the following folder structure:
'''

# imports
from pathlib import Path

# constants
SELF_DIR_O = Path(__file__).parent
SELF_DIR = SELF_DIR_O.resolve()
