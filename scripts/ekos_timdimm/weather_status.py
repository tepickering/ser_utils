#!/usr/bin/env python

import sys

import json

status = {
    'roof_status': {
        'open_ok': 1,
        'reasons': "Ready to roll"
    }
}

print(json.dumps(status))

sys.exit(0)
