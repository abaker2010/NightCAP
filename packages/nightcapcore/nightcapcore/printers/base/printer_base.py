# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
from colorama import Fore, Back, Style


class PrinterBase(object):
    def __init__(self):
        super().__init__()

    def base_print(
        self,
        text: object = None,
        optionaltext: object = None,
        *args,
        leadingTab=1,
        leadingText="",
        leadingBreaks=0,
        endingBreaks=0,
        vtabs=0,
        seperator=" : ",
        leadingColor=Fore.LIGHTGREEN_EX,
        textColor=Fore.LIGHTGREEN_EX,
        optionalTextColor=Fore.LIGHTGREEN_EX,
        breakTextColor=Fore.LIGHTMAGENTA_EX,
        styleRest=Style.RESET_ALL,
        **kwargs
    ) -> None:
        # print("okay")
        # print("Leading tab", str(leadingTab))
        _start = ("\v" * vtabs) + ("\n" * leadingBreaks)
        _leading = ("\t" * leadingTab) + " " + leadingColor + leadingText
        _text = textColor + str(text)
        _optional = (
            (breakTextColor + seperator + optionalTextColor + str(optionaltext))
            if optionaltext != None
            else ""
        )
        _end = styleRest + ("\n" * endingBreaks)
        print(_start + _leading + Style.RESET_ALL + " " + _text + _optional + _end)

    def animated_base_print(
        self,
        leadingTab=1,
        leadingText="",
        text="",
        optionalText="",
        leadingBreaks=0,
        endingBreaks=0,
        vtabs=0,
        seperator=" : ",
        leadingColor=Fore.LIGHTGREEN_EX,
        textColor=Fore.LIGHTGREEN_EX,
        optionalTextColor=Fore.LIGHTGREEN_EX,
        breakTextColor=Fore.LIGHTMAGENTA_EX,
        styleRest=Style.RESET_ALL,
    ) -> None:
        _start = ("\v" * vtabs) + ("\n" * leadingBreaks)
        _leading = ("\t" * leadingTab) + " " + leadingColor + leadingText
        _text = textColor + str(text)
        _optional = (
            (breakTextColor + seperator + optionalTextColor + optionalText)
            if len(optionalText) != 0
            else ""
        )
        _end = styleRest
        print(_start + _leading + " " + _text + _optional + _end, end="\r")
