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

import dbus

from astropy.time import Time
import astropy.units as u

from timdimm_tng.wx.check_wx import get_current_conditions, WX_LIMITS

bus = dbus.SessionBus()

log = logging.getLogger("timDIMM")
log.setLevel(logging.INFO)

handler = logging.handlers.WatchedFileHandler(Path.home() / "ox_wagon.log")
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
log.addHandler(handler)

# set up dbus access to the ekos scheduler
remote_obj = bus.get_object("org.kde.kstars", "/KStars/Ekos/Scheduler")
sched_iface = dbus.Interface(remote_obj, 'org.kde.kstars.Ekos.Scheduler')
prop_iface = dbus.Interface(remote_obj, dbus_interface='org.freedesktop.DBus.Properties')
properties = prop_iface.GetAll("org.kde.kstars.Ekos.Scheduler")

script, path = sys.argv

with open(Path.home() / "roof_status.json", 'r') as fp:
    roof_status = json.load(fp)

last_bad = Time(roof_status['last_bad'], format='isot')
wx_message = ""
open_ok = True

wx_status, wx_checks = get_current_conditions()

if wx_checks is None:
    open_ok = False
    wx_message = "No weather data available within the last 10 minutes"
else:
    # humidity limit exceeded
    if wx_checks['humidity']:
        open_ok = False
        wx_message += f"High RH >{WX_LIMITS['humidity']}%; "

    # below cold temp limit
    if wx_checks['temp']:
        open_ok = False
        wx_message += f"Too cold, T < {WX_LIMITS['temp']}; "

    # wind limit of 50 kph
    if wx_checks['wind']:
        open_ok = False
        wx_message += f"Too windy, wind > {WX_LIMITS['wind']} kph; "

    # LCO only good precip sensor and not always timely
    if wx_status['precip']:
        open_ok = False
        wx_message += "Precip detected; "

    # LCO only cloud sensor and not always timely
    if wx_status['cloudy']:
        open_ok = False
        wx_message += "Too cloudy"

if not open_ok:
    last_bad = Time.now()

last_bad_diff = (Time.now() - last_bad)
if open_ok and last_bad_diff > 30 * u.min:
    wx_message = "Safe to open"
    scheduler_status = int(properties['status'])
    if scheduler_status == 0:
        log.info("Safe to open, but scheduler stopped. Restarting...")
        sched_iface.start()
elif open_ok and last_bad_diff <= 30 * u.min:
    open_ok = False
    wx_message = f"Only safe for the last {last_bad_diff.to(u.min): .1f}"

# update and write out roof status
roof_status['last_bad'] = last_bad.isot
roof_status['roof_status']['open_ok'] = open_ok
roof_status['roof_status']['reasons'] = wx_message

with open(Path.home() / "roof_status.json", 'w') as fp:
    json.dump(roof_status, fp, indent=4)

with open(Path.home() / "ox_wagon_status.txt", 'r') as coords:
    ox_wagon = coords.readline()
    with open(path, 'w') as indistat:
        indistat.truncate()
        indistat.write(ox_wagon)

sys.exit(0)
