#!/usr/bin/env python

import sys
import json
import time
import shutil

from pathlib import Path
import logging
import logging.handlers

import numpy as np

from astropy.time import Time, TimezoneInfo
import astropy.units as u
from photutils.aperture import ApertureStats

from timdimm_tng.indi import INDI_Camera
from timdimm_tng.ser import load_ser_file
from timdimm_tng.analyze_cube import find_apertures, analyze_dimm_cube, seeing


log = logging.getLogger("HDIMM")
log.setLevel(logging.INFO)

handler = logging.handlers.WatchedFileHandler(Path.home() / "hdimm.log")
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
log.addHandler(handler)

log.info("Running post-capture script to collect seeing data...")

# grab the pointing status
with open(Path.home() / "pointing_status.json", 'r') as fp:
    pointing_status = json.load(fp)

# open and configure the camera
cam = INDI_Camera("ZWO CCD ASI432MM")
cam.ser_mode()

# need to toggle video stream on and off to get camera out of a "stuck" state
# it can get into, apparently. when in the state, the record_frames/record_duration
# methods will generate INDI warnings saying "recording device is busy". toggling
# video stream in kstars cleared it and these INDI commands perform the same function.
cam.set_prop("CCD_VIDEO_STREAM", "STREAM_ON", value="On")
time.sleep(2)
cam.set_prop("CCD_VIDEO_STREAM", "STREAM_OFF", value="On")
time.sleep(1)

# grab a short full-frame cube
cam.stream_exposure(0.001)
cam.set_ROI(0, 0, 1608, 1104)
cam.record_frames(2, savedir="/seeing", filename="find_boxes.ser")
time.sleep(1)
aperture_data = load_ser_file("/seeing/find_boxes.ser")
aperture_image = np.mean(aperture_data['data'], axis=0)
aps = find_apertures(aperture_image, brightest=3)
ap_stats = ApertureStats(aperture_image, aps[0])
centroids = ap_stats.centroid
if len(centroids) != 3:
    log.warning("Failed to find three apertures.")
    sys.exit(0)

x, y = np.mean(ap_stats.centroid, axis=0)

# center apertures in a 400x400 ROI and grab a 15 second cube
if ap_stats.max.min() > 8000:
    exptime = 0.0002
elif ap_stats.max.min() > 4000:
    exptime = 0.0005
elif ap_stats.max.min() < 500:
    exptime = 0.002
else:
    exptime = 0.001
cam.stream_exposure(exptime)
left = max(0, int(x - 200))
top = max(0, int(y - 200))
cam.set_ROI(left, top, 400, 400)
cam.record_duration(15, savedir="/seeing", filename="seeing.ser")
time.sleep(17)

try:
    seeing_data = analyze_dimm_cube(
        "/seeing/seeing.ser",
        napertures=3,
        airmass=pointing_status['airmass'],
        seeing_func=seeing
    )
except Exception as e:
    log.error(f"Seeing analysis failed: {e}")

if np.isfinite(seeing_data['seeing'].value) and seeing_data['seeing'].value < 10.0:
    log.info(f"Seeing: {seeing_data['seeing']:.2f}; N bad: {seeing_data['N_bad']}")
    if seeing_data['N_bad'] < 20:
        csv_file = Path.home() / "seeing.csv"
        if not csv_file.exists():
            with open(csv_file, 'w') as fp:
                fp.write("time,target,seeing,seeing_1,seeing_2,seeing_3,airmass,azimuth,exptime\n")

        with open(csv_file, 'a') as fp:
            z = pointing_status['airmass']
            azimuth = pointing_status['az']
            target = pointing_status['target']
            seeing = seeing_data['seeing'].value
            seeing_1 = seeing_data['raw_seeing'][0].value
            seeing_2 = seeing_data['raw_seeing'][1].value
            seeing_3 = seeing_data['raw_seeing'][2].value
            fp.write(
                f"{Time.now().isot},{target},{seeing:.3f},{seeing_1:.3f},{seeing_2:.3f},{seeing_3:.3f},{z:.3f},{azimuth:.1f},{exptime}\n"
            )

        with open(Path.home() / "seeing.txt", 'w') as f:
            print(f"{seeing_data['seeing'].value:.2f}", file=f)
            tobs = seeing_data['frame_times'][-1].to_datetime(timezone=TimezoneInfo(2 * u.hour)).isoformat()
            print(tobs, file=f)
    else:
        log.warning("Too many bad frames in seeing data.")

else:
    log.warning("Analysis of seeing data failed.")
    shutil.copy("/seeing/seeing.ser", Path.home() / "seeing_failed.ser")

sys.exit(0)
