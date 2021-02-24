# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Import
from nightcapcore.printers.print import Printer
from application.classes.options.cli_options_validator import NightcapCLIOptionsValidator
from nightcapcore import configuration
from nightcapcore.base import NightcapCoreBase
from application.classes.banners.nightcap_banner import NightcapBanner
from application.classes.helpers.screen.screen_helper import ScreenHelper
from colorama import Fore, Style
# endregion

class NightcapCLIOption_MixIn_Use():
    def __init__(self, selectedList: list, configuration: configuration,
                 packagebase: NightcapCoreBase = NightcapCoreBase(),
                 pageobjct: object = None):
        self.config = configuration
        self.package_base = packagebase
        self.pageobjct = pageobjct
        self.selected = selectedList
        self.printer = Printer()

    def help_use(self):
        print("\nSelect/Use a module/submobule/package: use [module/submobule/package name]\n")

    def do_use(self, line: str, override: object = None):
        _validator = NightcapCLIOptionsValidator(line, self.selected)
        if _validator.isvalid:
            try:
                if len(_validator.newSelectedList) == 3:
                    override(_validator.newSelectedList, self.config, self.package_base).cmdloop() 
                else:
                    self.pageobjct(_validator.newSelectedList, self.config, self.package_base).cmdloop() 
                
            except Exception as e:
                ScreenHelper().clearScr()
                NightcapBanner(self.config).Banner()
                print("\n", Fore.RED, e, Style.RESET_ALL, "\n")
        else:
            self.printer.print_error(Exception("Not a valid option. Use [options] for help"))
        
