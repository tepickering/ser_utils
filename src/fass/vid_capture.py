import sys
import subprocess
import argparse

import logging

log = logging.getLogger('SER video capture')
log.setLevel(logging.INFO)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)s - %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)


def set_prop(dev, property, key, value, host='localhost', port=7624):
    """
    Wrapper to use indi_setprop to set an INDI property on the server at host:port

    Arguments
    ---------
    dev : str
        INDI device to be configured

    property : str
        INDI property of device to be configured

    key : str
        Which key of the property to configure

    value : str or float
        New value of the property key

    host : str (default: localhost)
        Hostname of the INDI server host computer

    port : int (default: 7624)
        Port the INDI server is using
    """
    cmd = ['indi_setprop', '-h', host, '-p', str(port)]

    indi_str = f"{dev}.{property}.{key}={value}"

    cmd.append(indi_str)

    try:
        p = subprocess.run(cmd, check=True, capture_output=True)
    except Exception as e:
        log.error(f"Command failed: {e}")
        return e

    log.info(f"Set {indi_str} on {host}:{port}")

    if len(p.stdout) > 0:
        log.info(p.stdout)
    if len(p.stderr) > 0:
        log.error(p.stderr)

    return p

