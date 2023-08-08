#!/usr/bin/env python

import sys
from pathlib import Path
import logging
import logging.handlers

log = logging.getLogger("timDIMM")
log.setLevel(logging.INFO)

handler = logging.handlers.WatchedFileHandler(Path.home() / "timdimm.log")
log.addHandler(handler)

log.info("Ox Wagon disconnected")

sys.exit(0)
