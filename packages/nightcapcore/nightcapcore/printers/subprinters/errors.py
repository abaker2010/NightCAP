# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
from nightcapcore.printers import PrinterBase
from colorama import Fore, Back, Style


class ErrorPrinter(PrinterBase):
    def __init__(self):
        super().__init__()

    def print_error(self, exception: Exception, errColor = Fore.RED, msgColor = Fore.LIGHTYELLOW_EX, leadingtab=1, optionalText: str = '', vtab=1, endtab=1):
        self.base_print(leadingText="[!]", text=optionalText + str(exception), leadingColor=errColor, textColor=msgColor, leadingTab=leadingtab, vtabs=vtab, endingBreaks=endtab)