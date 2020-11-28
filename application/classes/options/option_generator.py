# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
from nightcappackages import *
from nightcapcore import NightcapCoreConsoleOutput
from colorama import Fore, Style

class NightcapOptionGenerator():
    def __init__(self, selectedList):
        self.selectedList = selectedList
        self.option_number = len(self.selectedList)
        self.console_output = NightcapCoreConsoleOutput()

    def options(self, isDetailed=False):
        
        vals = []
        opt = True
        if(self.option_number == 0):
            vals = list(map(lambda v: v + Fore.LIGHTMAGENTA_EX + " (" + str(NightcapInstalledPackageCounter().count_from_selected_module(v)) + ")" + Style.RESET_ALL, NightcapModules().module_types()))
        elif(self.option_number == 1):
            vals = list(map(lambda v: v + Fore.LIGHTMAGENTA_EX + " (" + str(NightcapInstalledPackageCounter().count_from_selected_submodule(self.selectedList[0], v)) + ")" + Style.RESET_ALL, NightcapSubModule().submodules()))
        elif(self.option_number == 2):
            vals = NightcapPackages().packages(self.selectedList,isDetailed)   
        else:
            opt = False
        if(opt):
            title1 = "Available Options"
            self.console_output.output("\n")
            self.console_output.output(title1, color=Fore.CYAN)
            self.console_output.output("-"*(len(title1)*2), color=Fore.LIGHTYELLOW_EX)
        
            if(isDetailed):
                for v in vals:
                    print("\t", v)
            else:
                _join = Fore.YELLOW + " | " + Style.RESET_ALL
                _vals = list(map(lambda v: Fore.CYAN + v + Style.RESET_ALL, vals))
                
                _cvals = []
                if(len(vals) != 0):
                    if(len(vals) > 1):
                        for v in _vals:
                            _cvals.append(v)
                            _cvals.append(_join)
                        _cvals = _cvals[:-1]
                    else:
                        for v in _vals:
                            _cvals.append(v)
                else:
                    _cvals.append("No Pacakges Installed")

                self.console_output.output("".join(_cvals))
            self.console_output.output('\n\n')
        else:
            self.console_output.output("No Options Available", level=6)
        
    def option_help(self):
        print(
        '''
        Modules that are available to use to investigate pcap files.
        View modules using the 'options' command
            Optional detailed view with command: options detailed
        
            ~ Usage: use [module]
        '''
        )
    
    
