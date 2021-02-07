# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
from application.classes.helpers.printers.base.printer_base import PrinterBase
from colorama import Fore, Back, Style


class ErrorPrinter(PrinterBase):
    def __init__(self):
        None

    def print_error(self, exception: Exception, errColor = Fore.RED, msgColor = Fore.RED, leadingtab=3):
        self.base_print(leadingText="[!]", text=str(exception), leadingColor=errColor, textColor=msgColor, leadingTab=leadingtab)