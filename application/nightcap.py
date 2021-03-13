# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
#region Import
from nightcapcore import NightcapCLIConfiguration
from nightcapcli import NightcapSettingsCMD, NightcapCLIOptionsSelector
from nightcapcore import ScreenHelper
#endregion

class Nightcap(NightcapCLIOptionsSelector):
    def __init__(self, configuration: NightcapCLIConfiguration):
        NightcapCLIOptionsSelector.__init__(self, [], configuration)
        self._conf = configuration

    def do_settings(self, line):
        print("Settings here")
        ScreenHelper().clearScr()
        NightcapSettingsCMD(self._conf).cmdloop()
#endregion
