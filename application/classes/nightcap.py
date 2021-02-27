# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
#region Import
from nightcapcore.configuration.configuration import NighcapCoreConfiguration
from application.classes.base_cmd.settings_cmd import NightcapSettingsCMD
from application.classes.options.cli_options_selector import NightcapCLIOptionsSelector
from application.classes.helpers.screen.screen_helper import ScreenHelper
#endregion

class Nightcap(NightcapCLIOptionsSelector):
    def __init__(self, configuration: NighcapCoreConfiguration):
        NightcapCLIOptionsSelector.__init__(self, [], configuration)

    def do_settings(self, line):
        print("Settings here")
        ScreenHelper().clearScr()
        NightcapSettingsCMD().cmdloop()
#endregion
