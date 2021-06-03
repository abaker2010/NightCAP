# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
from nightcapcore.printers import PrinterBase
from colorama import Fore, Back, Style


class InputPrinter(PrinterBase):
    def __init__(self):
        super().__init__()

    #region Input
    # User input, the default entry for the data is Y (aka yes)
    def input(
        self,
        text: str,
        questionColor: Fore = Fore.LIGHTGREEN_EX,
        inputcolor: Fore = Fore.CYAN,
        width: int = 5,
        sep: str = " ",
        vtab=1,
        etab=1,
        default="y"
    ) -> str:
        print("\n" * vtab)
        _input = input(questionColor + str(text).center(width, sep) + inputcolor)
        print("\n" * etab)
        if _input == "":
            return default
        else:
            return _input
    #endregion