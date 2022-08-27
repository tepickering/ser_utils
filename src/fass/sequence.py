import os
import json
import pkg_resources
import shutil


import xmltodict


class Sequence:
    """
    Wrap an INDI/Ekos imaging sequence
    """
    def __init__(self):
        template = pkg_resources.resource_filename(__name__, os.path.join("templates", "sequence_template.json"))
        capture_script = shutil.which("vid_capture")

        with open(template, 'r') as fp:
            self.config = json.load(fp)

        self.config['SequenceQueue']['Job']['PostCaptureScript'] = capture_script
