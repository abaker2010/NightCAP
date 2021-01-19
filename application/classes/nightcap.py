# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
#region Import
from application.classes.configuration.configuration import Configuration
from application.classes.options.dynamic_options import NightcapDynamicOptions
from application.classes.settings.settings import NightcapSettings
from application.classes.helpers.screen.screen_helper import ScreenHelper
from application.classes.updater.updater import  NightcapUpdater
#endregion

class Nightcap(NightcapDynamicOptions):
    def __init__(self, configuration: Configuration):
        NightcapDynamicOptions.__init__(self, None, configuration)
        self.config = configuration

    def do_settings(self, line):
        print("Settings here")
        ScreenHelper().clearScr()
        NightcapSettings().cmdloop()

    def do_update(self, line):
        print("Updating system")
        try:
            NightcapUpdater.instance().update()
        except Exception as e:
            print(e)

#endregion
