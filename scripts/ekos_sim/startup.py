#!/usr/bin/env python

import sys
from pathlib import Path
import logging
import logging.handlers

log = logging.getLogger("timDIMM")
log.setLevel(logging.INFO)

log.info(f"Starting up timDIMM observing session...")

sys.exit(0)
