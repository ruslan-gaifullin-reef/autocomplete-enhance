#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK

import argcomplete
import argparse
import time

# Heavy imports
import pandas as pd
import numpy as np

time.sleep(3)

parser = argparse.ArgumentParser()
parser.add_argument("--foo", choices=["a", "b", "c"])

argcomplete.autocomplete(parser)

args = parser.parse_args()
