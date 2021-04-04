# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Imports
import argparse
import json
from .configuration import NightcapCLIConfiguration

# endregion


class NightcapCore(NightcapCLIConfiguration):
    """

    This class is used initalize the core lib

    """

    def __init__(self):
        parser = argparse.ArgumentParser(description="Process some pcaps.")
        parser.add_argument("--data", required=True, help="list of pcap filenames")
        args = parser.parse_args()
        NightcapCLIConfiguration.__init__(self)
