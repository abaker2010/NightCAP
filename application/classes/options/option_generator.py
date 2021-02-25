# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
from nightcappackages import *
from nightcapcore.printers.print import Printer
from colorama import Fore, Style

class NightcapOptionGenerator():
    def __init__(self, selectedList):
        self.selectedList = selectedList
        self.option_number = len(self.selectedList)
        self.printer = Printer()

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
            self.printer
            title1 = "Available Options"
            self.printer.print_underlined_header(text=title1,leadingText='', titleColor=Fore.LIGHTYELLOW_EX)
        
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

                self.printer.item_1(text="".join(_cvals), leadingText='', leadingTab=1, vtabs=1, endingBreaks=1)
        else:
            self.printer.print_error(exception=Exception("Error No Option Available"))
        
    def option_help(self):
        print(
        '''
        Modules that are available to use to investigate pcap files.
        View modules using the 'options' command
            Optional detailed view with command: options detailed
        
            ~ Usage: use [module]
        '''
        )
    
    
