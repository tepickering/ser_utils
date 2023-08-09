#!/usr/bin/env python

import sys
from pathlib import Path
import logging
import logging.handlers

log = logging.getLogger("timDIMM")
log.setLevel(logging.INFO)

script, az = sys.argv

handler = logging.handlers.WatchedFileHandler(Path.home() / "ox_wagon.log")
log.addHandler(handler)

log.info(f"Ox Wagon receiving slew command to {az}...")

sys.exit(0)
