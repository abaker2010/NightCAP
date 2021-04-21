# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Imports
import os
import json
import hashlib
from nightcapcli.base.base_cmd import NightcapBaseCMD
from nightcapcore.configuration import NightcapCLIConfiguration
from colorama import Fore, Style

# endregion


class NightcapBackup(NightcapBaseCMD):
    def __init__(self, selectedList: list, channelid, passedJson):
        super().__init__(selectedList, channelid=channelid, passedJson=passedJson)