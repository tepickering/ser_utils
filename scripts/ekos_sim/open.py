#!/usr/bin/env python

import sys
from pathlib import Path
import logging
import logging.handlers

log = logging.getLogger("timDIMM")
log.setLevel(logging.INFO)

handler = logging.handlers.WatchedFileHandler(Path.home() / "ox_wagon.log")
log.addHandler(handler)

script, path = sys.argv

with open(Path.home() / "ox_wagon_status.txt", 'w') as coords:
    coords.truncate()
    coords.write('0 1 0')

log.info(f"Unparking and Opening Ox Wagon...")

sys.exit(0)
