# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
from nightcapcore import configuration
from nightcapcore.base import NightcapCoreBase
from application.classes.base_cmd.base_cmd import NightcapBaseCMD

class NightcapCLIOptionsPackage(NightcapBaseCMD):
    def __init__(self,selectedList: list, configuration: configuration, packagebase: NightcapCoreBase = NightcapCoreBase()):
        NightcapBaseCMD.__init__(self, selectedList, configuration, packagebase)

    def do_params(self, line):
        print("Find out package params")