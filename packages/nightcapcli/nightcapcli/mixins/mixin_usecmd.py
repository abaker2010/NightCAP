# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Import
from nightcapcli.mixins.mixin_use import NightcapCLI_MixIn_Use
from nightcapcore import NightcapCLIConfiguration
from ..cmds import NightcapMainCMD
# endregion

class NightcapCLICMDMixIn(NightcapCLI_MixIn_Use, NightcapMainCMD):
    def __init__(self, selectedList: list, configuration: NightcapCLIConfiguration, nextobj: type = object, channelid: str = None):
        NightcapMainCMD.__init__(self, selectedList, configuration, channelid)
        NightcapCLI_MixIn_Use.__init__(self, selectedList, configuration, nextobj, channelid)
