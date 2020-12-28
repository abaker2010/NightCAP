# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
from nightcapcore import NightcapCoreBase
from nightcapcore import NightcapCoreConsoleOutput
from nightcappackages import *
import cmd
from colorama import Fore, Style


class NightcapBaseCMD(cmd.Cmd):
    def __init__(self, selectedList, packagebase: NightcapCoreBase = None):
        cmd.Cmd.__init__(self,completekey='tab', stdin=None, stdout=None)
        self.selectedList = [] if selectedList == None else selectedList
        itm = "" if selectedList == None else list(map(lambda v : "[" + Fore.LIGHTYELLOW_EX + v + Fore.LIGHTGREEN_EX + "]", selectedList))
        self.prompt = Fore.GREEN + 'nightcap' + "".join(itm) + ' > ' + Fore.CYAN
        self.doc_header = Fore.GREEN + 'Commands' + Style.RESET_ALL
        self.misc_header = Fore.GREEN + 'System' + Style.RESET_ALL
        self.undoc_header = Fore.GREEN + 'Other' + Style.RESET_ALL
        self.ruler = Fore.YELLOW + '-' + Style.RESET_ALL

        # region Needs to be singleton objects
        self.modules_db = NightcapModules()
        self.packages_db = NightcapPackages()
        self.submodules_db = NightcapSubModule()
        self.package_base = packagebase
        self.console_output = NightcapCoreConsoleOutput()
        #endregion
