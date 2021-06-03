# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Import
# from nightcapcli import NightcapCLIPublisher, NightcapCLIPackage, NightcapCLICMDMixIn
from nightcapcli.observer.publisher import NightcapCLIPublisher
from nightcapcli.cmds import NightcapCLIPackage
from nightcapcli.mixins.mixin_maincmd import NightcapCLICMDMixIn
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
    ) -> None:
        NightcapCLICMDMixIn.__init__(self, selected, Nightcap, channelid)
        self.channelid = channelid
        self.parentid = parentid

        if additionalchildren != []:
            _nns = self.selectedList.copy()
            _nns.append(additionalchildren[0])
            _nac = additionalchildren[1::]
            _directions = {"nextstep": _nns, "additionalsteps": _nac, "remove": 0}
            self._push_object(_directions)

    # def __del__(self):
    #     pass

    def _push_object(self, directions: dict) -> None:
        self.printer.debug("Trying to push new object", currentMode=self.config.verbosity)
        self.printer.debug("Current path:", NightcapCLIPublisher().selectedList, currentMode=self.config.verbosity)

        try:
            self.printer.debug("Making new channel", currentMode=self.config.verbosity)
            _channel = NightcapCLIPublisher().new_channel()

            self.printer.debug("Channels",NightcapCLIPublisher().channels, currentMode=self.config.verbosity)
            self.printer.debug("Channel", _channel, currentMode=self.config.verbosity)

            if len(directions["nextstep"]) != 3:
                self.printer.debug("Trying to add", directions["nextstep"][-1], currentMode=self.config.verbosity)
                self.addselected(directions["nextstep"][-1])

                self.printer.debug("After adding", NightcapCLIPublisher().selectedList, currentMode=self.config.verbosity)

                _who = self.pageobjct(
                    NightcapCLIPublisher().selectedList,
                    _channel,
                    self.channelID,
                    directions["additionalsteps"],
                )

                NightcapCLIPublisher().register(_channel, _who)
                _who.cmdloop()
            else:
                self.printer.debug("Trying to add", directions["nextstep"][-1], currentMode=self.config.verbosity)
                self.addselected(directions["nextstep"][-1])
                
                self.printer.debug("New Path", NightcapCLIPublisher().selectedList, currentMode=self.config.verbosity)
                self.printer.debug("Package Config", NightcapCLIPublisher().get_package_config(NightcapCLIPublisher().selectedList), currentMode=self.config.verbosity)
                
                _who = NightcapCLIPackage(
                    NightcapCLIPublisher().selectedList,
                    NightcapCLIPublisher().get_package_config(NightcapCLIPublisher().selectedList),
                    _channel,
                )

                NightcapCLIPublisher().register(_channel, _who)
                _who.cmdloop()
        except Exception as e:
            self.printer.print_error(e)
            NightcapCLIPublisher().del_channel(_channel)
            print(NightcapCLIPublisher().channels)
       

    def cli_update(self, message) -> None:
        if type(message) == bool:
            # print("Child object destroyed:", str(message))
            # print("Current list is:", NightcapCLIPublisher().selectedList)
            pass

        elif type(message) == dict:
            self._push_object(message)
        else:
            pass
# endregion
