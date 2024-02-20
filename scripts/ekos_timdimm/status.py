#!/usr/bin/env python

"""
When ekos is running with the dome scripting interface active, this script gets run every couple of seconds.
As such, this is a good place to do overall monitoring of conditions.
"""

import sys
import json
from pathlib import Path
import logging
import logging.handlers

import sdbus

from astropy.time import Time
from astropy.coordinates import get_sun, AltAz
import astropy.units as u

from timdimm_tng.locations import SAAO

from timdimm_tng.dbus.scheduler import Scheduler
from timdimm_tng.dbus.mount import Mount
from timdimm_tng.dbus.indi import INDI
from timdimm_tng.dbus.ekos import Ekos
from timdimm_tng.dbus.dome import Dome

from timdimm_tng.wx.check_wx import get_current_conditions


bus = sdbus.sd_bus_open_user()

scheduler = Scheduler(bus=bus)
mount = Mount(bus=bus)
indi = INDI(bus=bus)
ekos = Ekos(bus=bus)
dome = Dome(bus=bus)

log = logging.getLogger("timDIMM")
log.setLevel(logging.INFO)

handler = logging.handlers.WatchedFileHandler(Path.home() / "ox_wagon.log")
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
log.addHandler(handler)

script, path = sys.argv

roof_status = Path.home() / "roof_status.json"

if roof_status.exists():
    with open(roof_status, 'r') as fp:
        roof_status = json.load(fp)
else:
    roof_status = {}

wx_message = ""
open_ok = False

sun_coord = get_sun(Time.now())
sun_azel = sun_coord.transform_to(AltAz(obstime=Time.now(), location=SAAO))

# sun is up
if sun_azel.alt > -12 * u.deg:
    open_ok = False
    if sun_azel.alt > 0 * u.deg:
        wx_message += f"Sun is up: {sun_azel.alt: .1f} above the horizon; "
    else:
        wx_message += f"Nautical twilight: sun is at {sun_azel.alt: .1f}; "

# check weather and if SALT or MONET think it's safe to open
wx, safety_checks = get_current_conditions()

if safety_checks['monet']:
    open_ok = True
    log.info("MONET safety check passed. Safe to open.")
    wx_message += "MONET says it's ok to open; "

if safety_checks['salt']:
    open_ok = True
    log
    wx_message += "SALT says it's ok to open; "

if open_ok:
    wx_message = "Safe conditions according to either SALT or MONET"
    log.info("Safe to be open")
    if not scheduler.status:
        log.info("Scheduler stopped. Restarting...")
        scheduler.reset_all_jobs()
        scheduler.start()
else:
    # if we're still not clear to be open, make sure we're parked and closed
    if scheduler.status:
        log.info("Not ok to open, but scheduler running. Stopping...")
        scheduler.stop()
    if not dome.is_parked():
        log.info("Not ok to open, but Ox Wagon open. Closing and parking telescope...")
        dome.park()
        mount.park()

# update and write out roof status
roof_status['roof_status']['open_ok'] = open_ok
roof_status['roof_status']['reasons'] = wx_message

with open(Path.home() / "roof_status.json", 'w') as fp:
    json.dump(roof_status, fp, indent=4)

with open(Path.home() / "ox_wagon_status.txt", 'r') as coords:
    ox_wagon = coords.readline()
    with open(path, 'w') as indistat:
        indistat.truncate()
        indistat.write(ox_wagon)

# log.info(f"Ox Wagon status: {ox_wagon.strip()}")

sys.exit(0)
