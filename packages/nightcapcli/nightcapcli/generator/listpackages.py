# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
from nightcappackages import *
from colorama import Fore, Style
from nightcapcore import *
from nightcappackages.classes.databases.mogo.mongo_packages import MongoPackagesDatabase

class NightcapListPackages():
    def __init__(self):
        self.packages_db = MongoPackagesDatabase.instance()
        self.priner = Printer()

    def list_packages(self):
        print("\n\t\tInstalled packages")
        print("\t\t","-" * 20,"\n",sep="")
        _packages = list(map(lambda v : v, self.packages_db.get_all_packages()))
        if(_packages == []):
            print(Fore.YELLOW + "\t\tNo Packages Installed\n", Style.RESET_ALL)
        else:
            for p in _packages:
                print(Fore.YELLOW,'\t- ', p['package_for']['module'],'/',p['package_for']['submodule'],'/',p['package_information']['package_name'], Fore.LIGHTCYAN_EX, "\tver: ",p['package_information']['version'], Fore.LIGHTMAGENTA_EX, "  author: ",p['author_info']['creator'], sep='')
                print(Fore.GREEN, '\t\t', p['package_information']['details'],"\n")
