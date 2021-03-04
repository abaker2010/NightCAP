# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.

from nightcapcore import NightcapCoreBase, configuration, Printer
from application.classes.helpers.screen.screen_helper import ScreenHelper

from application.classes.banners.nightcap_banner import NightcapBanner
from nightcappackages import *
import cmd
from colorama import Fore, Style

try:
    from subprocess import DEVNULL # py3k
except ImportError:
    import os
    DEVNULL = open(os.devnull, 'wb')
    
class _NightcapBaseCMD_Config(cmd.Cmd):
    def __init__(self, selectedList):
        cmd.Cmd.__init__(self,completekey='tab', stdin=None, stdout=None)
        self.selectedList = [] if selectedList == None else selectedList
        itm = "" if selectedList == None else list(map(lambda v : "[" + Fore.LIGHTYELLOW_EX + v + Fore.LIGHTGREEN_EX + "]", selectedList))
        self.prompt = Fore.GREEN + 'nightcap' + "".join(itm) + ' > ' + Fore.CYAN
        self.doc_header = Fore.GREEN + 'Commands' + Style.RESET_ALL
        self.misc_header = Fore.GREEN + 'System' + Style.RESET_ALL
        self.undoc_header = Fore.GREEN + 'Other' + Style.RESET_ALL
        self.ruler = Fore.YELLOW + '-' + Style.RESET_ALL
        

class NightcapBaseCMD(_NightcapBaseCMD_Config):
    def __init__(self, selectedList, configuration: configuration, packagebase: NightcapCoreBase = None):
        super(NightcapBaseCMD, self).__init__(selectedList)
        # region 
        self.config = configuration
        self.package_base = packagebase
        self.printer = Printer()
        #endregion

    #region Exit
    def do_exit(self,line):
        ScreenHelper().clearScr()
        try:
            self.selectedList.remove(self.selectedList[-1])
        except Exception as e:
            pass
        return True
    #endregion

    def do_help(self, line):
        try:
            if(len(line) == 0):
                if(self.package_base.project != None):
                    self.printer.print_underlined_header_undecorated(text="System settings")
                    self.printer.item_1(text="Current Project", optionalText=str(self.package_base.project['project_name']))
                else:
                    self.printer.print_underlined_header_undecorated(text="System settings")
                    self.printer.item_1(text="Current Project", optionalText='None')
        except Exception as e:
            # self.printer.print_error(exception=e)
            pass

        super(NightcapBaseCMD, self).do_help(line)


    def do_banner(self, line):
        ScreenHelper().clearScr()
        NightcapBanner(self.config).Banner()
