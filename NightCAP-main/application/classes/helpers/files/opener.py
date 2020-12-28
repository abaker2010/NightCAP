# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
import os

class FolderOpener():
    """Open reports and totals folders."""
    def __init__(self):
        self.path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.reports = os.path.realpath(os.path.join(self.path, "Reports"))
        self.totals = os.path.realpath(os.path.join(self.path, "Totals"))

    def open_reports(self):
        try:
            os.system(f'open {self.reports}')
        except Exception as e:
            print(e)
            print("Error opening reports. Please make sure that the folders exist: `checkfolders`")


    def open_totals(self):
        try:
            os.system(f'open {self.totals}')
        except Exception as e:
            print("Error opening reports. Please make sure that the folders exist: `checkfolders`")