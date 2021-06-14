# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Imports
from nightcapcore import Printer
import tempfile
import shutil
from nightcappackages import *
# endregion


class NightcapTmpFileHelper(object):

    def __init__(self) -> None:
        super().__init__()
        self.tmp_location: str = ""
        self.printer = Printer()
        self._deleted = False

    def __del__(self):
        try:
            if self._deleted:
                self._rmtmp()
        except Exception as e:
            pass

    
    def delete(self):
        self._rmtmp()
        self._deleted = True

    def create(self):
        self._createtmp()
        self._deleted = False

    def _createtmp(self):
        # region Tmp dir functions
        self.tmp_location = tempfile.mkdtemp()
        # if self.verbose:
        self.printer.print_underlined_header("Preparing")
        self.printer.item_1("Creating tmp dir " + self.tmp_location)

    def _rmtmp(self):
        self.printer.print_underlined_header("Clean Up")
        # if self.verbose:
        self.printer.print_formatted_check("Tmp dir removed", endingBreaks=1)
        shutil.rmtree(self.tmp_location)
        # self.tmpUpdatePaths = []
        # self.tmpUpdateLocation = None