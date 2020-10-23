#!/usr/bin/env python
# encoding: utf-8

# IMPORTS
import sys
import os

sys.path.append(os.path.abspath(os.getcwd()))
from hebrew_tokenizer.api import tokenize
__version__ = "1.0.1"
__all__ = ['tokenize']

