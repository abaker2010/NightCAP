# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
#region Import
from nightcapcli.observer.publisher import NightcapCLIPublisher
from nightcapcore import NightcapCLIConfiguration
from nightcapcli.cmds.settings import NightcapSettingsCMD
from nightcapcli.cmds import NightcapCLIOptionsPackage
from nightcapcli.mixins.mixin_use import NightcapCLI_MixIn_Use
from nightcapcli.mixins.mixin_usecmd import NightcapCLICMDMixIn
from nightcapcore import ScreenHelper
#endregion

class Nightcap(NightcapCLICMDMixIn):
    def __init__(self, selected: list, configuration: NightcapCLIConfiguration, channelid: str = '', parentid: str = '', additionalchildren: list = []):
        NightcapCLICMDMixIn.__init__(self, selected, configuration, Nightcap, channelid)
        self._conf = configuration
        self.channelid = channelid
        self.parentid = parentid
        if additionalchildren != []:
            # for _ in additionalchildren:
            #     print("additional child to create:", _)
            print('Before calling additional children', '/'+ '/'.join(additionalchildren))
            NightcapCLI_MixIn_Use.do_use(self, '/'+ '/'.join(additionalchildren), override=NightcapCLIOptionsPackage)
            # self.do_use( '/'+ '/'.join(additionalchildren))


    def do_settings(self, line):
        print("Settings here")
        ScreenHelper().clearScr()
        NightcapSettingsCMD(self._conf).cmdloop()

    def do_use(self, line):
        NightcapCLI_MixIn_Use.do_use(self, line, override=NightcapCLIOptionsPackage)

    def __del__(self):
        print("Trying to close object")
        print("Trying to notify parent ID:", self.parentid)
        try:
            NightcapCLIPublisher().dispatch(self.parentid, True)
        except:
            pass

    def cli_update(self, message):
        if type(message) == bool:
            print("Child object destroyed:", str(message))
            print("Current list is:", NightcapCLIPublisher().selectedList)
        else:
            print("Message", message)
        # self.do_exit()
        
#endregion
