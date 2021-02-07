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
        '''\nUpdate the project. Usage: update [main|dev]. If no option is specified the default will be used.\n'''
        sline = str(line).lstrip().split(' ')
        print("Line: ", str(line).split(" "))
        try:
            if(len(sline) == 1):
                print("No Verbose")
                if(sline[0] == ''):
                    print("using default / no verbose")
                    NightcapUpdater.instance().update(True)
                elif(sline[0] == 'dev'):
                    print("using dev / no verbose")
                    NightcapUpdater.instance().update(False)
                elif(sline[0] == 'main'):
                    print("Using main / no verbose")
                    NightcapUpdater.instance().update(True)
                else:
                    print("Not an option")
            elif(len(sline) == 2):
                print("Verbose")
                if(sline[0] == 'dev'):
                    print("using dev / verbose")
                    NightcapUpdater.instance().update(False, True)
                elif(sline[0] == 'main'):
                    print("Using main / verbose")
                    NightcapUpdater.instance().update(True, True)
                else:
                    print("Error with verbose")
            else:
                print("To many arguments")
        except Exception as e:
            print("Exception:",e)
        # try:
        #     if not line:
        #         NightcapUpdater.instance().update(True)
        #     else:
        #         if str(line).lower() == "main":
        #             NightcapUpdater.instance().update(True)
        #         elif str(line).lower() == "dev":
        #             NightcapUpdater.instance().update(False)
            
        # except Exception as e:
        #     print(e)

#endregion
