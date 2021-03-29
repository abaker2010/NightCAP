# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
import os
from .pathsenum import NightcapPathsEnum
from .pathcleaner import NightcapPathCleaner


class NightcapPaths(NightcapPathCleaner):
    def __init__(self):
        """Paths for the Nightcap project"""
        NightcapPathCleaner.__init__(
            self, os.path.dirname(__file__).replace((os.sep + "paths"), "")
        )

    def generate_path(self, path: NightcapPathsEnum, pathextra: list = []):
        try:
            return self.combine_with_base(path.value, pathextra)
        except Exception as e:
            return e
