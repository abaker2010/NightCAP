# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
import os
import copy
import json
from nightcapcore import configuration, NightcapCoreBase
from application.classes.base_cmd.base_cmd import NightcapBaseCMD
from colorama import Fore, Style

class NightcapCLIOptionsPackage(NightcapBaseCMD):
    def __init__(self,selectedList: list, configuration: configuration, packagebase: NightcapCoreBase = NightcapCoreBase()):
        NightcapBaseCMD.__init__(self, selectedList, configuration, packagebase)
        self.config = configuration
        try:
            self.package_params = copy.deepcopy(self.packages_db.package_params(self.selectedList))
        except Exception as e:
            self.package_params = None

    def help_params(self):
        h1 = "See all available parameters:"
        h2 = "params"
        h3 = "set param:\tparams [PARAM] [PARAMVALUE]"
        p = '''
         %s 
         %s
         %s
        ''' % (
            (Fore.GREEN + h1),
            (Fore.YELLOW + h2 + Style.RESET_ALL),
            (Fore.YELLOW + h3 + Style.RESET_ALL),
            )
        print(p)

    def do_params(self, line):
        print("Find out package params")
        print("Base package")

        if(len(line) == 0):
            title1 = "Base Params"
            self.printer.print_underlined_header(text=title1, leadingText='', titleColor=Fore.LIGHTYELLOW_EX)
            self.package_base.show_params()
        


    def do_run(self,line):
    
        force = False
        if(self.package_base.project == None):
            force = input((Fore.YELLOW + "Project not selected to be used would you like to continue? [Y/n]: " + Fore.GREEN))
            print(Style.RESET_ALL, Fore.LIGHTCYAN_EX)
            yes_options = self.config.Config()["NIGHTCAP"]["yes"].split(" ")
            if(force == None):
                force = False
            else:
                if(force in yes_options):
                    force = True
        else:
            force = True

        if(force == True):
            if(len(self.selectedList) == 3):
                exe_path = self.packages_db.get_package_run_path(self.selectedList)
                dat = {}
                dat[0] = self.package_base.toJson()
                dat[1] = self.package_params
                print("data before passing: ", dat)
                
                call = "python3.8 %s --data '%s'" % (exe_path, json.dumps(dat))
                
                os.system(call)
            else:
                print("Package not selected to be used")
        else:
            self.console_output.output("Scan canceled by user\n", level=6)
