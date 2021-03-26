# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Import
from nightcapcli.cmds.cmd_shared.cmd_validator import NightcapCLIOptionsValidator
from nightcapcore import Printer, configuration, NightcapBanner, ScreenHelper
from ..generator import NightcapOptionGenerator
from colorama import Fore, Style
# endregion

class NightcapCLI_MixIn_Use():
    def __init__(self, selectedList: list, configuration: configuration,
                 pageobjct: object = None):
        self.config = configuration
        self.pageobjct = pageobjct
        self.selected = selectedList
        self.printer = Printer()

    def help_use(self):
        print("\nSelect/Use a module/submobule/package: use [module/submobule/package name]\n")

    def do_use(self, line: str, override: object = None):
        _validator = NightcapCLIOptionsValidator(line, self.selected)
        if _validator.isvalid:
            try:
                ScreenHelper().clearScr()
                if len(_validator.newSelectedList) == 3:
                    override(_validator.newSelectedList, self.config, _validator.get_package_config(_validator.newSelectedList)).cmdloop() 
                else:
                    self.pageobjct(_validator.newSelectedList, self.config).cmdloop() 
                
            except Exception as e:
                ScreenHelper().clearScr()
                NightcapBanner(self.config).Banner()
                print("\n", Fore.RED, e, Style.RESET_ALL, "\n")
        else:
            self.printer.print_error(Exception("Not a valid option. Use [options] for help"))

    def do_options(self, line):
        '''\nSee what options are available to use. Use -d on packages to see detailed information\n'''
        if(len(line) == 0):
            NightcapOptionGenerator(self.selected).options()
        elif(line == "-d"):
            if(len(self.selected) != 2):
                self.printer.print_formatted_additional(text="Detailed information can not be provided at this level")
                NightcapOptionGenerator(self.selected).options(isDetailed=False)
            else:
                NightcapOptionGenerator(self.selected).options(isDetailed=True)
        else:
            print("Error with command")
        
