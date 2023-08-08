#!/usr/bin/env python

import sys
from pathlib import Path
import logging
import logging.handlers

log = logging.getLogger("timDIMM")
log.setLevel(logging.INFO)

log.info(f"Aborting Ox Wagon...")

sys.exit(0)
