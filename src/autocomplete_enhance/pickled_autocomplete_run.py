#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK

import argcomplete
import pickle

def identity(string):
    return string

# load the cached parser from a file
with open("cached_parser.pkl", "rb") as f:
    parser = pickle.load(f)

# Use the cached parser for autocompletion
argcomplete.autocomplete(parser)
