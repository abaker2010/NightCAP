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

    def print_error(
        self,
        exception: Exception = None,
        message: str = '',
        *args,
        leadingText="[!]",
        errColor=Fore.RED,
        msgColor=Fore.LIGHTYELLOW_EX,
        optionalColor=Fore.YELLOW,
        leadingtab=1,
        vtab=1,
        endtab=1,
        **kwargs
    ):
        self.base_print(str(exception), message,
        leadingColor=errColor,textColor=msgColor,optionalTextColor=optionalColor,leadingTab=leadingtab,vtabs=vtab,
        endingBreaks=endtab,leadingText=leadingText,
         *args, **kwargs)
