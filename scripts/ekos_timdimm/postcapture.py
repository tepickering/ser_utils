#!/usr/bin/env python

import sys
import json
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
cam.set_stream_ROI(0, 0, 1608, 1104)
cam.record_frames(10, savedir="/home/timdimm", filename="find_boxes.ser")
aperture_data = load_ser_file("/home/timdimm/find_boxes.ser")
aperture_image = np.sum(aperture_data['data'], axis=0)
aps = find_apertures(aperture_image, brightest=2)
ap_stats = ApertureStats(aperture_image, aps[0])
x, y = np.mean(ap_stats.centroid, axis=0)

# center apertures in a 400x400 ROI and grab a 15 second cube
if ap_stats.max.max() > 16000:
    exptime = 0.0002
elif ap_stats.max.max() > 8000:
    exptime = 0.0005
else:
    exptime = 0.001
cam.stream_exposure(exptime)
cam.set_stream_ROI(int(x - 200), int(y - 200), 400, 400)
cam.record_duration(15, savedir="/home/timdimm", filename="seeing.ser")

seeing_data = analyze_dimm_cube("/home/timdimm/seeing.ser", airmass=pointing_status['airmass'])

with open(Path.home() / "seeing.csv", 'a') as fp:
    z = pointing_status['airmass']
    azimuth = pointing_status['az']
    fp.write(f"{Time.now().isot}, {seeing_data['seeing'].value:.2f}, {z:.3f}, {azimuth:.1f}\n")

with open("seeing.txt", 'w') as f:
    print(f"{seeing_data['seeing'].value:.2f}", file=f)
    tobs = seeing_data['frame_times'][-1].to_datetime(timezone=TimezoneInfo(2 * u.hour))
    print(tobs, file=f)

sys.exit(0)
