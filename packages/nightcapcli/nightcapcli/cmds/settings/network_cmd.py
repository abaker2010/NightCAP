# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.

# region Imports
from nightcapcli.base.base_cmd import NightcapBaseCMD
# endregion


class NightcapNetworkCMD(NightcapBaseCMD):
    # region Init
    def __init__(self, channelID: str = None):
        NightcapBaseCMD.__init__(self, ["settings", "network"], channelid=channelID)

    # endregion
    def complete_select(self, text, line, begidx, endidx):
        return [i for i in ("tor", "standard") if i.startswith(text)]

    def help_select(self):
        self.printer.help("Select the protocol to use for requests")
        self.printer.help("Useage: select <tor | standard>")

    def do_select(self, line):
        if str(line).lower() == "tor":
            print("Selecting tor")
        elif str(line).lower() == "standard":
            print("Selecting Standard")
        else:
            self.printer.print_error(Exception("Error selecting network. Please view the help to see options allowed."))


