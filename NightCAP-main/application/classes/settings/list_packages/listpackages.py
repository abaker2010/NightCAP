# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
import os
import json
from nightcappackages import *
from colorama import Fore, Style
from nightcapcore import *

class NightcapListPackages():
    def __init__(self):
        self.packages_db = NightcapPackages()

    def list_packages(self):
        print("\n\t\tInstalled packages")
        print("\t\t","-" * 20,"\n",sep="")
        self.packages_db.get_all_packages()
