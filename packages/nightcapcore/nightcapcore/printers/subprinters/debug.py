# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
from nightcapcore.printers.base import PrinterBase
from colorama import Fore, Back, Style


class DebugPrinter(PrinterBase):
    def __init__(self):
        super(PrinterBase, self).__init__()

    def debug(
        self,
        text: object = None,
        optionaltext: object = None,
        currentMode: bool = False,
        *args,
        leadingText='[DEBUG]',
        leadingTab=0,
        optionalTextColor=Fore.LIGHTBLACK_EX,
        textColor=Fore.LIGHTCYAN_EX,
        leadingColor=Fore.MAGENTA,
        **kwargs
    ):
        # print("Text", text)
        # print("Optional",optionaltext)
        if currentMode == True:
            self.base_print(text, optionaltext, *args, leadingText=leadingText,leadingTab=leadingTab, leadingColor=leadingColor, textColor=textColor, optionalTextColor=optionalTextColor, **kwargs)
        # self.base_print(self,text, optionaltext)
