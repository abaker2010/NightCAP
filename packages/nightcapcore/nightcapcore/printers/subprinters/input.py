# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
from nightcapcore.printers.base.printer_base import PrinterBase
from colorama import Fore, Back, Style

class InputPrinter(PrinterBase):

    def __init__(self):
        super().__init__()

    def input(self, text: str, questionColor: Fore = Fore.LIGHTGREEN_EX,inputcolor: Fore = Fore.CYAN, width: int = 5,sep: str = ' ', vtab=1, etab=1):
        print('\n'*vtab)
        _input =  input(questionColor + str(text).center(width,sep) + inputcolor)
        print('\n'*etab)
        return _input