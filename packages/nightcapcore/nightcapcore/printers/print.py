# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# from application.classes.helpers.printers.subprinters.item import ItemPrinter
# from application.classes.helpers.printers.subprinters.headerpy import HeaderPrinter
# from application.classes.helpers.printers.subprinters.errors import ErrorPrinter
# from application.classes.helpers.printers.subprinters.checkmark import CheckMarkPrinter
from nightcapcore.printers.subprinters.item import ItemPrinter
from nightcapcore.printers.subprinters.headerpy import HeaderPrinter
from nightcapcore.printers.subprinters.errors import ErrorPrinter
from nightcapcore.printers.subprinters.checkmark import CheckMarkPrinter
from colorama import Fore, Back, Style

class Printer(CheckMarkPrinter, ErrorPrinter, HeaderPrinter, ItemPrinter):
    def __init__(self):
        super(Printer, self).__init__()