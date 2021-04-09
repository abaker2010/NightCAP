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
    """
    This object is used to create the CLI's for the users:
        - Base
        - Module
        - Submodule

    Init:
        - selected list         :  used for [<T>][<T>] options for console
        - channelid             :  used for the (self) notifications from the observer
        - parentid              :  used for the parent interactive notifications from the observer
        - additionalchildren    :  used for additional page creation when a deep path is specified
    """

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
        print("Trying to push new object")
        print("Current path:", NightcapCLIPublisher().selectedList)
        print("Directions: ", directions["nextstep"][-1])

        try:
            print("Making new channel")
            _channel = NightcapCLIPublisher().new_channel()
            print(NightcapCLIPublisher().channels)
            print("Channels: ", _channel)
            # raise Exception("Test Error")

            if len(directions["nextstep"]) != 3:
                print("trying to add:", directions["nextstep"][-1])
                self.addselected(directions["nextstep"][-1])
                print("Testing after")
                print(NightcapCLIPublisher().selectedList)
                # NightcapCLIPublisher().selectedList.append(directions["nextstep"][-1])
                _who = self.pageobjct(
                    NightcapCLIPublisher().selectedList,
                    _channel,
                    self.channelID,
                    directions["additionalsteps"],
                )

                NightcapCLIPublisher().register(_channel, _who)
                _who.cmdloop()
            else:
                print("trying to add:", directions["nextstep"][-1])
                self.addselected(directions["nextstep"][-1])

                print("Testing after")
                print(NightcapCLIPublisher().selectedList)

                print("Package Config")
                print(NightcapCLIPublisher().get_package_config(NightcapCLIPublisher().selectedList))
                # NightcapCLIPublisher().selectedList.append(directions["nextstep"][-1])
                _who = NightcapCLIPackage(
                    NightcapCLIPublisher().selectedList,
                    NightcapCLIPublisher().get_package_config(NightcapCLIPublisher().selectedList),
                    _channel,
                )

                NightcapCLIPublisher().register(_channel, _who)
                _who.cmdloop()
                # raise Exception("Not Implemented")
        except Exception as e:
            self.printer.print_error(e)
            NightcapCLIPublisher().del_channel(_channel)
            print(NightcapCLIPublisher().channels)
        # NightcapCLIPublisher().selectedList.append(directions["nextstep"][-1])
        # print(NightcapCLIPublisher().selectedList)
        # _channel = NightcapCLIPublisher().new_channel()
        # _who = None
        
        # if len(directions["nextstep"]) == 3:
        #     print("pushing object with", NightcapCLIPublisher().selectedList)
        #     # _who = NightcapCLIPackage(
        #     #     NightcapCLIPublisher().selectedList,
        #     #     NightcapCLIPublisher().get_package_config(NightcapCLIPublisher().selectedList),
        #     #     _channel,
        #     # )
        #     print("PKG Data:", NightcapCLIPublisher().get_package_config(NightcapCLIPublisher().selectedList))
        # else:
        #     _who = self.pageobjct(
        #         NightcapCLIPublisher().selectedList,
        #         _channel,
        #         self.channelID,
        #         directions["additionalsteps"],
        #     )

        #     NightcapCLIPublisher().register(_channel, _who)
        #     _who.cmdloop()

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
