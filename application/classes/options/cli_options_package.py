# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
import os
import copy
import json
from nightcapcore import NightcapCLIConfiguration
from nightcappackages.classes.databases.mogo.mongo_packages import MongoPackagesDatabase
from application.classes.base_cmd.base_cmd import NightcapBaseCMD
from colorama import Fore, Style

class NightcapCLIOptionsPackage(NightcapBaseCMD):
    def __init__(self,selectedList: list, configuration: NightcapCLIConfiguration, pkg_config: dict = None):
        NightcapBaseCMD.__init__(self, selectedList, configuration)
        self.config = configuration
        self.pkg_config = pkg_config
        self.db = MongoPackagesDatabase.instance()
        # print("Pkg config", pkg_config)
        # print("Pkg config", type(pkg_config))
        try:
            self.package_params = copy.deepcopy(pkg_config["package_information"]["entry_file_optional_params"])
            # print("Deep copied params", self.package_params)
        except Exception as e:
            self.printer.print_error(exception=e)
            self.package_params = None

    def help_params(self):
        self.printer.item_2(text="see parameters", optionalText="params", leadingTab=1, vtabs=1, leadingText='', textColor=Fore.LIGHTGREEN_EX)
        self.printer.item_2(text="set parameters", optionalText="params [PARAM] [PARAMVALUE]", leadingTab=1,  endingBreaks=1, leadingText='', textColor=Fore.LIGHTGREEN_EX)
 
    def do_params(self, line):
        # print("Find out package params")
        # print("Base package")
        
        title1 = "Base Params"
        title2 = "Package Params"
        _params = self.pkg_config['package_information']['entry_file_optional_params']

        if(len(line) == 0):
            self.printer.print_underlined_header(text=title1, leadingText='', titleColor=Fore.LIGHTYELLOW_EX)
            self.config.show_params()

            if(len(_params) != 0):
                self.printer.print_underlined_header(text=title2, leadingText='', titleColor=Fore.LIGHTYELLOW_EX)
                for k,v in self.pkg_config['package_information']['entry_file_optional_params'].items():
                    v = "None" if v == "" else v
                    self.printer.item_2(text="~ %s" % k, optionalText=v, leadingTab=1, leadingText='', textColor=Fore.LIGHTGREEN_EX)
        else:
            print("Line for params:", line)
            try:
                _s = line.split(" ")
                
                if _s[0] in _params.keys():
                    print("Contains key")
                    _params[_s[0]] = _s[1]
                else:
                    print("dose not contain key")

            except Exception as e:
                self.printer.print_error(exception=e)
                self.printer.print_error(exception=Exception("Error with setting parameter"))


        print()


    def help_run(self):
        self.printer.item_2(text="Run package", leadingTab=1, vtabs=1, endingBreaks=1, leadingText='', textColor=Fore.LIGHTGREEN_EX)

    def do_run(self,line):
        force = False
        if(self.config.project == None):
            force = input((Fore.YELLOW + "Project not selected to be used would you like to continue? [Y/n]: " + Fore.GREEN))
            print(Style.RESET_ALL, Fore.LIGHTCYAN_EX)
            yes_options = self.config.currentConfig["NIGHTCAPCORE"]["yes"].split(" ")
            if(force == None):
                force = False
            else:
                if(force in yes_options):
                    force = True
        else:
            force = True

        if(force == True):
            if(len(self.selectedList) == 3):
                print("List to be used to find run path", self.selectedList)
                # needs to be set up with the NightCap Mongo Packages instance
                exe_path = self.db.get_package_run_path(self.pkg_config)
                # exe_path = self.packages_db.get_package_run_path(self.pkg_config)
                print(exe_path)
                dat = {}
                dat[0] = self.config.toJson()
                dat[1] = self.package_params
                print("data before passing: ", dat)
                call = "python3.8 %s --data '%s'" % (exe_path, json.dumps(dat))
                os.system(call)
            else:
                print("Package not selected to be used")
        else:
            self.printer.print_error(exception=Exception("Scan canceled by user"))
