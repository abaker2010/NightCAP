# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
from colorama import Fore, Back, Style
from nightcappackages import *
from application.classes.helpers.screen.screen_helper import ScreenHelper

class NightcapDynamicUse():
    def __init__(self):
        self.modules_db = NightcapModules()
        self.submodules_db = NightcapSubModule()
        self.packages_db = NightcapPackages()

    def use(self, option_number: int, selectedList: list, line: str):
        try:
            if(option_number == 0):
                if(self._check_module_types(line)):
                    return line
                else:
                    raise Exception("Parameter not available")
            elif(option_number == 1):
                if(self._check_sub_module(line)):
                    return line
                else:
                    raise Exception("Parameter not available")
            elif(option_number == 2):
                if(self._check_packages(line, selectedList)):
                    return line
                else:
                    raise Exception("Parameter not available")
        except Exception as e:
            print("\n", Fore.RED, e, Style.RESET_ALL, "\n")

    def _check_module_types(self,line):
        if(line in self.modules_db.module_types()):
            ScreenHelper().clearScr()
            return True
        else:
            return False

    def _check_sub_module(self,line):
        if(line in self.submodules_db.submodules()):
            ScreenHelper().clearScr()
            return True
        else:
            return False

    def _check_packages(self,line, selected):
        if(line in self.packages_db.packages(selected)):
            ScreenHelper().clearScr()
            return True
        else:
            return False
        

    def validate(self, lines):
        if(len(lines) == 2):
            if(self._check_module_types(lines[0]) & self._check_sub_module(lines[1])):
                return True
            else:
                return False
        elif(len(lines) == 3):
            if(self._check_module_types(lines[0]) 
            & self._check_sub_module(lines[1])
            & self._check_packages(lines[2], lines[0:2])):
                return True
            else:
                return False
        else:
            return False


