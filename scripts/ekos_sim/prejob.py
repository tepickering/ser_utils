#!/usr/bin/python3

import json
import sys
from pathlib import Path
import logging
import logging.handlers

import dbus

from pathlib import Path


log = logging.getLogger("timDIMM")
log.setLevel(logging.INFO)

handler = logging.handlers.WatchedFileHandler(Path.home() / "timdimm.log")
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
log.addHandler(handler)

log.info(f"Running pre-job...")

bus = dbus.SessionBus()

mount = bus.get_object("org.kde.kstars", "/KStars/Ekos/Mount")
mount_interface = dbus.Interface(mount, 'org.freedesktop.DBus.Properties')

capture = bus.get_object("org.kde.kstars", "/KStars/Ekos/Capture")
capture_interface = dbus.Interface(capture, 'org.freedesktop.DBus.Properties')

mount_props = mount_interface.GetAll("org.kde.kstars.Ekos.Mount")
capture_props = capture_interface.GetAll("org.kde.kstars.Ekos.Capture")

az, el = float(mount_props['horizontalCoords'][0]), float(mount_props['horizontalCoords'][1])
ra, dec = float(mount_props['equatorialCoords'][0]), float(mount_props['equatorialCoords'][1])
ha = float(mount_props['hourAngle'])
target = capture_props['targetName']

log.info(f"Observing {target} at Az={az:.1f}°, El={el:.1f}°")

status = {
    'target': target,
    'az': az,
    'el': el,
    'ra': ra,
    'dec': dec,
    'ha': ha
}

with open(Path.home() / "status.json", 'w') as fp:
    fp.write(json.dumps(status, indent=4))

sys.exit(0)
