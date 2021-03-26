# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
#region Import
from nightcapcore import NightcapCLIConfiguration
from nightcapcli.cmds.settings import NightcapSettingsCMD
from nightcapcli.cmds import NightcapCLIOptionsPackage
from nightcapcli.mixins.mixin_use import NightcapCLI_MixIn_Use
from nightcapcli.mixins.mixin_usecmd import NightcapCLICMDMixIn
from nightcapcore import ScreenHelper
#endregion

class Nightcap(NightcapCLICMDMixIn):
    def __init__(self, selected: list, configuration: NightcapCLIConfiguration):
        NightcapCLICMDMixIn.__init__(self, selected, configuration, Nightcap)
        self._conf = configuration

    def do_settings(self, line):
        print("Settings here")
        ScreenHelper().clearScr()
        NightcapSettingsCMD(self._conf).cmdloop()

    def do_use(self, line):
        NightcapCLI_MixIn_Use.do_use(self, line, override=NightcapCLIOptionsPackage)
#endregion
