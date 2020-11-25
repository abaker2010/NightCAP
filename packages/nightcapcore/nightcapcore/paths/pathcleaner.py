# Copyright 2020 by Aarom Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
import os

class NightcapPathCleaner(object):
    def __init__(self, cwd: str):
        self.cwd = cwd

    def combine_with_base(self, path: str, paths: list = []):
        _cleaned_list = list(map(lambda v :  str(v), paths))
        return os.sep.join([self.cwd, path, os.sep.join(_cleaned_list)])
