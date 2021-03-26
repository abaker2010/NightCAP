# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Import
from nightcapcore import NightcapCLIConfiguration
from ..cmds import NightcapMainCMD
from ..mixins import NightcapCLI_MixIn_Use
# endregion

class NightcapCLICMDMixIn(NightcapMainCMD, NightcapCLI_MixIn_Use):
    def __init__(self, selectedList: list, configuration: NightcapCLIConfiguration, nextobj: type = object):
        NightcapMainCMD.__init__(self, selectedList, configuration)
        NightcapCLI_MixIn_Use.__init__(self, selectedList, configuration, nextobj)
