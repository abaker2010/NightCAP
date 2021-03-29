# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
from nightcapcore.printers import PrinterBase
from colorama import Fore, Back, Style


class HeaderPrinter(PrinterBase):
    def __init__(self):
        super().__init__()

    def print_header(
        self,
        text="",
        *args,
        leadingTab=1,
        leadingText="",
        leadingBreaks=0,
        endingBreaks=0,
        vtabs=0,
        titleColor=Fore.LIGHTGREEN_EX,
        leadingColor=Fore.YELLOW,
        styleRest=Style.RESET_ALL,
        **kwargs
    ):
        self.base_print(
            str(text + styleRest),
            leadingText=leadingText,
            textColor=titleColor,
            leadingColor=leadingColor,
            leadingBreaks=leadingBreaks,
            leadingTab=leadingTab,
            endingBreaks=endingBreaks,
            vtabs=vtabs,
            *args,**kwargs
        )

    def print_underlined_header(
        self,
        text: str = "",
        *args,
        leadingTab=1,
        leadingText="[-]",
        underline="-",
        leadingBreaks=1,
        endingBreaks=0,
        vtabs=0,
        titleColor=Fore.LIGHTGREEN_EX,
        underlineColor=Fore.LIGHTMAGENTA_EX,
        leadingColor=Fore.YELLOW,
        styleRest=Style.RESET_ALL,
        **kwargs
    ):
        self.base_print(
            text=text,
            vtabs=vtabs,
            leadingText=leadingText,
            textColor=titleColor,
            leadingColor=leadingColor,
            leadingBreaks=leadingBreaks,
            leadingTab=leadingTab,
            *args,**kwargs
        )  
        self.base_print(
            text=str((underline * len(text)) + styleRest),
            endingBreaks=endingBreaks,
            leadingTab=leadingTab,
            leadingColor=underlineColor,
        )

    def print_underlined_header_undecorated(
        self,
        text="",
        *args,
        leadingTab=1,
        leadingText="",
        underline="-",
        leadingBreaks=1,
        endingBreaks=0,
        vtabs=0,
        titleColor=Fore.LIGHTYELLOW_EX,
        underlineColor=Fore.LIGHTMAGENTA_EX,
        leadingColor=Fore.YELLOW,
        styleRest=Style.RESET_ALL,
        **kwargs
    ):
        self.base_print(
            text=text,
            vtabs=vtabs,
            leadingText=leadingText,
            textColor=titleColor,
            leadingColor=leadingColor,
            leadingBreaks=leadingBreaks,
            leadingTab=leadingTab,
            *args,**kwargs
        )  # , leadingBreaks=leadingBreaks, leadingTab=leadingTab, endingBreaks=endingBreaks,vtabs=vtabs,leadingColor=titleColor)
        self.base_print(
            text=str((underline * len(text)) + styleRest),
            endingBreaks=endingBreaks,
            leadingTab=leadingTab,
            leadingColor=underlineColor,
        )
