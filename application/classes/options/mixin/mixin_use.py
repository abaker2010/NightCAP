# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Import
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
        # self.selectedList = selectedList
        self.config = configuration
        self.package_base = packagebase
        self.pageobjct = pageobjct

    def help_use(self):
        print("\nSelect/Use a module/submobule/package: use [module/submobule/package name]\n")

    def do_use(self, items: list = [], override: object = None):
        # print("Using type ", self.pageobjct)
        try:
            # _nsl = self.selectedList
            if len(items) == 3:
                print("Replacing whole path")
                # _nsl = items
                override(items, self.config, self.package_base).cmdloop() 
            else:
                # for i in items:
                #     _nsl.append(i)
                self.pageobjct(items, self.config, self.package_base).cmdloop() 
            
        except Exception as e:
            ScreenHelper().clearScr()
            NightcapBanner(self.config).Banner()
            print("\n", Fore.RED, e, Style.RESET_ALL, "\n")
        
