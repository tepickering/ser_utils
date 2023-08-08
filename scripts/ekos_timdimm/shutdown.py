#!/usr/bin/env python

import sys
from pathlib import Path
import logging
import logging.handlers

log = logging.getLogger("timDIMM")
log.setLevel(logging.INFO)

script, az = sys.argv

log.info(f"Shutting down timDIMM observing session...")

sys.exit(0)
