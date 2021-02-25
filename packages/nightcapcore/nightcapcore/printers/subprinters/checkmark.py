# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# from application.classes.helpers.printers.base.printer_base import PrinterBase
from nightcapcore.printers.base.printer_base import PrinterBase
from colorama import Fore, Back, Style

class CheckMarkPrinter(PrinterBase):
    def __init__(self):
        super().__init__()

    def print_formatted_check(self, text, optionaltext="", leadingBreaks=0, endingBreaks=0, vtabs=0, leadingTab=2,leadingColor=Fore.LIGHTGREEN_EX, textColor=Fore.LIGHTGREEN_EX,
                              optionalTextColor=Fore.LIGHTBLACK_EX, breakTextColor=Fore.LIGHTBLACK_EX):
        self.base_print(leadingText='[✓]', text=text, optionalText=optionaltext, leadingTab=leadingTab,
                         leadingBreaks=leadingBreaks, endingBreaks=endingBreaks, vtabs=vtabs, leadingColor=leadingColor,
                         optionalTextColor=optionalTextColor, textColor=textColor, breakTextColor=breakTextColor)

    def print_formatted_additional(self, text, optionaltext="", leadingBreaks=0, endingBreaks=0, vtabs=0, leadingTab=2,leadingColor=Fore.YELLOW, textColor=Fore.LIGHTGREEN_EX,
                              optionalTextColor=Fore.LIGHTBLACK_EX, breakTextColor=Fore.LIGHTBLACK_EX):
        self.base_print(leadingText='[>]', text=text, optionalText=optionaltext, leadingTab=leadingTab,
                         leadingBreaks=leadingBreaks, endingBreaks=endingBreaks, vtabs=vtabs, leadingColor=leadingColor,
                         optionalTextColor=optionalTextColor, textColor=textColor, breakTextColor=breakTextColor)

    def print_formatted_delete(self, text, optionaltext="", leadingBreaks=0, endingBreaks=0, vtabs=0, leadingTab=2,leadingColor=Fore.RED, textColor=Fore.LIGHTYELLOW_EX,
                              optionalTextColor=Fore.LIGHTBLACK_EX, breakTextColor=Fore.LIGHTBLACK_EX):
        self.base_print(leadingText='[x]', text=text, optionalText=optionaltext, leadingTab=leadingTab,
                         leadingBreaks=leadingBreaks, endingBreaks=endingBreaks, vtabs=vtabs, leadingColor=leadingColor,
                         optionalTextColor=optionalTextColor, textColor=textColor, breakTextColor=breakTextColor)