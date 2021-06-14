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
        sep: str = ":",
        vtab=1,
        etab=1,
        leadingBreaks=1,
        default=["yes", "y", "ye", "ya", "yep", "yeah"],
        defaultReturn=False
    ) -> bool:
        width = len(text) + 5
        print("\n" * vtab)
        _input = input(questionColor + str("\t"*leadingBreaks + text + str(sep)).center(width, " ") + inputcolor)
        print("\n" * etab)
        if _input == "":
            return defaultReturn
        elif _input in default:
            return True
        else:
            return False
    #endregion

    # User input, the default entry for the data is Y (aka yes)
    def input_return_only(
        self,
        text: str,
        questionColor: Fore = Fore.LIGHTGREEN_EX,
        inputcolor: Fore = Fore.CYAN,
        sep: str = ":",
        vtab=1,
        etab=1,
        leadingBreaks=1,
        defaultReturn=False
    ) -> str:
        width = len(text) + 5
        print("\n" * vtab)
        _input = input(questionColor + str("\t"*leadingBreaks + text + str(sep)).center(width, " ") + inputcolor)
        print("\n" * etab)
        if _input == "":
            return defaultReturn
        else:
            return _input
    #endregion