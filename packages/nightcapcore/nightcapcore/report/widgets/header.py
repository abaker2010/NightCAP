# Copyright 2020 by Aarom Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
class NightcapSimpleReportHeader(dict):
    def __init__(self, name: str, format: str = "header_default"):
        self.name = name
        self.format = format
        self.data = []
        dict.__init__(self, name=name, format=format, data=self.data)