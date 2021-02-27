# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# from application.classes.helpers.printers.subprinters.item import ItemPrinter
# from application.classes.helpers.printers.subprinters.headerpy import HeaderPrinter
# from application.classes.helpers.printers.subprinters.errors import ErrorPrinter
# from application.classes.helpers.printers.subprinters.checkmark import CheckMarkPrinter
from nightcapcore.printers import InputPrinter, ItemPrinter, HeaderPrinter, ErrorPrinter, CheckMarkPrinter
from colorama import Fore, Back, Style
from nightcapcore.printers.subprinters.waiting import WaitingPrinter

class Printer(CheckMarkPrinter, ErrorPrinter, HeaderPrinter, ItemPrinter, InputPrinter, WaitingPrinter):
    def __init__(self):
        super(Printer, self).__init__()