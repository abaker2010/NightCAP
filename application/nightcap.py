# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Import
import cmd
from nightcapcli.cmds.main_cmd import NightcapMainCMD
from nightcapcli.observer.publisher import NightcapCLIPublisher
from nightcapcore import NightcapCLIConfiguration
from nightcapcli.cmds.settings import NightcapSettingsCMD
from nightcapcli.cmds import NightcapCLIPackage
from nightcapcli.mixins.mixin_maincmd import NightcapCLICMDMixIn
from nightcapcore import ScreenHelper

# endregion


class Nightcap(NightcapCLICMDMixIn):
    def __init__(
        self,
        selected: list,
        channelid: str = "",
        parentid: str = "",
        additionalchildren: list = [],
    ):
        NightcapCLICMDMixIn.__init__(self, selected, Nightcap, channelid)
        self.channelid = channelid
        self.parentid = parentid

        if additionalchildren != []:
            _nns = self.selectedList.copy()
            _nns.append(additionalchildren[0])
            _nac = additionalchildren[1::]
            _directions = {"nextstep": _nns, "additionalsteps": _nac, "remove": 0}
            self._push_object(_directions)

    def __del__(self):
        # print("Trying to close object")
        # print("Trying to notify parent ID:", self.parentid)
        pass

    def _push_object(self, directions: dict):
        _channel = NightcapCLIPublisher().new_channel()
        _who = None
        if len(directions["nextstep"]) == 3:
            _who = NightcapCLIPackage(
                directions["nextstep"],
                NightcapCLIPublisher().get_package_config(directions["nextstep"]),
                _channel,
            )
        else:
            _who = self.pageobjct(
                directions["nextstep"],
                _channel,
                self.channelID,
                directions["additionalsteps"],
            )

        NightcapCLIPublisher().register(_channel, _who)

        _who.cmdloop()

    def cli_update(self, message):
        # print("Cli update called")
        if type(message) == bool:
            # print("Child object destroyed:", str(message))
            # print("Current list is:", NightcapCLIPublisher().selectedList)
            pass

        elif type(message) == dict:
            # self.printer.print_formatted_additional("dict object")
            # print(message)
            self._push_object(message)
        else:
            pass
            # print("Message", message)


# endregion
