# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
class NightcapSimpleReportParagraph(dict):
    def __init__(self, text: str, format: str = "paragraph_default"):
        dict.__init__(self, text=text, format=format)
        self.text = text
        self.format = format
        