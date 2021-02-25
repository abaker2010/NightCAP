# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
#region Import
from application.classes.options.option_generator import NightcapOptionGenerator
#endregion

class NightcapCLIOption_MixIn_Options():
    def __init__(self, selectedList: list):
        self.selectedList = selectedList
        
    def do_options(self, line):
        '''\nSee what options are available to use\n'''
        if(len(line) == 0):
            NightcapOptionGenerator(self.selectedList).options()
        elif(line == "detailed"):
            NightcapOptionGenerator(self.selectedList).options(isDetailed=True)
        else:
            print("Error with command")