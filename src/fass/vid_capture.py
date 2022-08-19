import sys
import argparse
import logging

from pathlib import Path

from fass.indi import INDI_Camera


log = logging.getLogger('SER video capture')
log.setLevel(logging.INFO)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)s - %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)


def main():
    parser = argparse.ArgumentParser(description='Utility for recording videos from INDI cameras')

    parser.add_argument(
        '-h', '--host',
        metavar="<hostname>",
        help="Hostname of INDI Server Host Computer",
        default='localhost'
    )

    parser.add_argument(
        '-p', '--port',
        metavar="<port>",
        help="INDI Server Port",
        default=7624
    )

    parser.add_argument(
        '-c', '--camera',
        metavar="<INDI camera>",
        help="Name of INDI Camera",
        default='CCD Simulator'
    )

    parser.add_argument(
        '-e', '--exposure',
        metavar="<exposure time>",
        help="Camera Exposure Time in seconds",
        default=0.1
    )

    parser.add_argument(
        '-n', '--nframes',
        metavar="<N frames>",
        help="Number of Frames to Capture",
        default=100
    )

    parser.add_argument(
        '--savedir',
        metavar="<save directory>",
        help="Directory to Save to"
    )

    parser.add_argument(
        '--filename',
        metavar="<filename>",
        help="Filename to Save Video to"
    )

    parser.add_argument(
        '--ser',
        action='store_true',
        help="Use SER Video Recorder"
    )

    parser.add_argument(
        '--ogv',
        action='store_true',
        help="Use OGV Video Recorder"
    )

    parser.add_argument(
        '--raw',
        action='store_true',
        help="Use RAW Video Encoder"
    )

    parser.add_argument(
        '--mjpeg',
        action='store_true',
        help="Use MJPEG Video Encoder"
    )

    args = parser.parse_args()

    cam = INDI_Camera(args.camera, host=args.host, port=args.port)
