# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
from nightcapcore.printers import (
    InputPrinter,
    ItemPrinter,
    HeaderPrinter,
    ErrorPrinter,
    CheckMarkPrinter,
    DebugPrinter,
)
from colorama import Fore, Back, Style
from nightcapcore.printers.subprinters.waiting import WaitingPrinter


class Printer(
    CheckMarkPrinter,
    ErrorPrinter,
    HeaderPrinter,
    ItemPrinter,
    InputPrinter,
    WaitingPrinter,
    DebugPrinter,
):
    def __init__(self) -> None:
        super(Printer, self).__init__()
