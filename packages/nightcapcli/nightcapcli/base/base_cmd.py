# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.

from random import randint
from nightcapcore import NightcapCLIConfiguration, Printer, ScreenHelper, NightcapBanner
from nightcapcore.colors.nightcap_colors import NightcapColors
from nightcappackages import *
import cmd
from colorama import Fore, Style
from nightcapserver.server.server import NighcapCoreSimpleServer
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
    def __init__(self, selectedList, configuration: NightcapCLIConfiguration):
        super(NightcapBaseCMD, self).__init__(selectedList)
        # region 
        self.config = configuration
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
        super(NightcapBaseCMD, self).do_help(line)

    def help_config(self):
        self.printer.help(text="Get the current system configuration(s)")

    def do_config(self, line):
        ScreenHelper().clearScr()
        self.printer.print_underlined_header_undecorated(text='Configuration')

        self.printer.print_underlined_header(text='Projects', leadingTab=2)
        if(len(line) == 0):
            if(self.config.project != None):
                self.printer.print_formatted_other(text="Current Project", optionaltext=str(self.config.project['project_name']),leadingTab=3, optionalTextColor=Fore.LIGHTMAGENTA_EX)
            else:
                self.printer.print_formatted_other(text="Current Project", optionaltext='None',leadingTab=3)
                
        self.printer.print_underlined_header(text='Web Server (Django)', leadingTab=2)
        self.printer.print_formatted_other(text='IP', optionaltext=self.config.currentConfig["REPORTINGSERVER"]["ip"], leadingTab=3, optionalTextColor=Fore.YELLOW)
        self.printer.print_formatted_other(text='Port', optionaltext=self.config.currentConfig["REPORTINGSERVER"]["port"], leadingTab=3, optionalTextColor=Fore.YELLOW)
        self.printer.print_formatted_other(text='URL', optionaltext=NighcapCoreSimpleServer().get_url(), leadingTab=3, optionalTextColor=Fore.YELLOW)
        # self.printer.print_formatted_other(text='Status', optionaltext= "UP" if NighcapCoreSimpleServer().status == True else "DOWN", leadingTab=3, optionalTextColor=Fore.YELLOW)

        self.printer.print_underlined_header(text='Database (Mongo)', leadingTab=2)
        self.printer.print_formatted_other(text='URL', optionaltext=self.config.currentConfig["MONGOSERVER"]["ip"], leadingTab=3, optionalTextColor=Fore.YELLOW)
        self.printer.print_formatted_other(text='Status', optionaltext=self.config.currentConfig["MONGOSERVER"]["port"], leadingTab=3, optionalTextColor=Fore.YELLOW)

    def do_banner(self, line):
        ScreenHelper().clearScr()
        NightcapBanner(self.config).Banner()
