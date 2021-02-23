# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Import
from application.classes.base_cmd.base_cmd import NightcapBaseCMD
from application.classes.options.mixin.mixin_use import NightcapCLIOption_MixIn_Use
from application.classes.options.mixin.mixin_options import NightcapCLIOption_MixIn_Options
from application.classes.configuration.configuration import Configuration
from nightcapcore.base import NightcapCoreBase
# endregion

class NightcapCLIUseCMDMixIn(NightcapBaseCMD, NightcapCLIOption_MixIn_Options, NightcapCLIOption_MixIn_Use):
    def __init__(self, selectedList: list, configuration: Configuration,
                 packagebase: NightcapCoreBase = NightcapCoreBase(), nextobj: type = object):
        NightcapBaseCMD.__init__(self, selectedList, configuration, packagebase)
        NightcapCLIOption_MixIn_Options.__init__(self, selectedList)
        NightcapCLIOption_MixIn_Use.__init__(self, selectedList, configuration, packagebase, nextobj)