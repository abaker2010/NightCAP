# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Import
# from application.classes.base_cmd.base_cmd import NightcapBaseCMD
# from application.classes.base_cmd.main_cmd import NightcapMainCMD
# from application.classes.options.mixin.mixin_use import NightcapCLIOption_MixIn_Use
# from application.classes.options.mixin.mixin_options import NightcapCLIOption_MixIn_Options
from nightcapcore import NightcapCLIConfiguration
from ..cmds import NightcapMainCMD
from ..mixins import NightcapCLIOption_MixIn_Options, NightcapCLIOption_MixIn_Use
# endregion

class NightcapCLIUseCMDMixIn(NightcapMainCMD, NightcapCLIOption_MixIn_Options, NightcapCLIOption_MixIn_Use):
    def __init__(self, selectedList: list, configuration: NightcapCLIConfiguration, nextobj: type = object):
        NightcapMainCMD.__init__(self, selectedList, configuration)
        NightcapCLIOption_MixIn_Options.__init__(self, selectedList)
        NightcapCLIOption_MixIn_Use.__init__(self, selectedList, configuration, nextobj)