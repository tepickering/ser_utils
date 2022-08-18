import sys
import subprocess

import logging


class INDI_Device:
    """
    Wrapper for communicating with an INDI server via INDI's command-line tools

    Arguments
    ---------
    devname : str
        Name of the INDI device

    host : str (default: localhost)
        Hostname of the INDI server host computer

    port : int (default: 7624)
        Port the INDI server is using
    """
    def __init__(self, devname, host='localhost', port=7624, log=None):
        self.devname = devname
        self.host = host
        self.port = str(port)

        if log is None:
            self.log = logging.getLogger(f"{devname} at {host}:{port}")
            self.log.setLevel(logging.INFO)
        else:
            self.log = log

    def set_prop(self, property, key, value):
        """
        Use indi_setprop to set an INDI property

        Arguments
        ---------
        property : str
            INDI property of device to be configured

        key : str
            Which key of the property to configure

        value : str or float
            New value of the property key
        """
        cmd = ['indi_setprop', '-h', self.host, '-p', self.port]

        indi_str = f"{self.devname}.{property}.{key}={value}"

        cmd.append(indi_str)

        try:
            p = subprocess.run(cmd, check=True, capture_output=True)
        except Exception as e:
            self.log.error(f"Command failed: {e}")
            return e

        self.log.info(f"Set {indi_str} on {self.host}:{self.port}")

        if len(p.stdout) > 0:
            self.log.info(p.stdout)
        if len(p.stderr) > 0:
            self.log.error(p.stderr)

        return p

