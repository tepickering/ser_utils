#!/usr/bin/env python

import sys
import json
import time

from pathlib import Path
import logging
import logging.handlers

import numpy as np

from astropy.time import Time, TimezoneInfo
import astropy.units as u
from photutils.aperture import ApertureStats

from timdimm_tng.indi import INDI_Camera
from timdimm_tng.ser import load_ser_file
from timdimm_tng.analyze_cube import find_apertures, analyze_dimm_cube


log = logging.getLogger("timDIMM")
log.setLevel(logging.INFO)

handler = logging.handlers.WatchedFileHandler(Path.home() / "timdimm.log")
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
log.addHandler(handler)

log.info("Running post-capture script to collect seeing data...")

# grab the pointing status
with open(Path.home() / "pointing_status.json", 'r') as fp:
    pointing_status = json.load(fp)

# open and configure the camera
cam = INDI_Camera("ZWO ASI432MM")
cam.ser_mode()

# grab a short full-frame cube
cam.stream_exposure(0.001)
cam.set_ROI(0, 0, 1608, 1104)
cam.record_frames(10, savedir="/home/timdimm", filename="find_boxes.ser")
time.sleep(1)
aperture_data = load_ser_file("/home/timdimm/find_boxes.ser")
aperture_image = np.mean(aperture_data['data'], axis=0)
aps = find_apertures(aperture_image, brightest=2)
ap_stats = ApertureStats(aperture_image, aps[0])
x, y = np.mean(ap_stats.centroid, axis=0)

# center apertures in a 400x400 ROI and grab a 15 second cube
if ap_stats.max.max() > 8000:
    exptime = 0.0002
elif ap_stats.max.max() > 4000:
    exptime = 0.0005
else:
    exptime = 0.001
cam.stream_exposure(exptime)
left = max(0, int(x - 200))
top = max(0, int(y - 200))
cam.set_ROI(left, top, 400, 400)
cam.record_duration(15, savedir="/home/timdimm", filename="seeing.ser")
time.sleep(17)
seeing_data = analyze_dimm_cube("/home/timdimm/seeing.ser", airmass=pointing_status['airmass'])

csv_file = Path.home() / "seeing.csv"
if not csv_file.exists():
    with open(csv_file, 'w') as fp:
        fp.write("time,target,seeing,airmass,azimuth,exptime\n")

with open(csv_file, 'a') as fp:
    z = pointing_status['airmass']
    azimuth = pointing_status['az']
    target = pointing_status['target']
    seeing = seeing_data['seeing'].value
    fp.write(
        f"{Time.now().isot},{target},{seeing:.2f},{z:.3f},{azimuth:.1f},{exptime}\n"
    )

with open(Path.home() / "seeing.txt", 'w') as f:
    print(f"{seeing_data['seeing'].value:.2f}", file=f)
    tobs = seeing_data['frame_times'][-1].to_datetime(timezone=TimezoneInfo(2 * u.hour)).isoformat()
    print(tobs, file=f)

sys.exit(0)
