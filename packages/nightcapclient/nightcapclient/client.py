# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
import argparse
import json
from nightcapcore import NightcapCLIConfiguration

class NightcapClient(NightcapCLIConfiguration):
    def __init__(self):
        parser = argparse.ArgumentParser(description='Process some pcaps.')
        parser.add_argument('--data', required=True,
                            help='list of pcap filenames')
        args = parser.parse_args()
        NightcapCLIConfiguration.__init__(self,generatePcaps=True,basedata=dict(json.loads(args.data)))