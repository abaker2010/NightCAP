# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.

from nightcapcli.cmds.cmd_shared.shell_cmd import ShellCMDMixin
from nightcapcli.cmds.projects import NightcapProjectsCMD
from nightcapcore import NightcapCLIConfiguration
from colorama import Fore, Style
from ..base import NightcapBaseCMD
from nightcapcore import ScreenHelper
from nightcapcli.cmds.settings import NightcapSettingsCMD


class NightcapMainCMD(NightcapBaseCMD, ShellCMDMixin):
    def __init__(
        self,
        selectedList,
        channelid: str = None,
    ):
        NightcapBaseCMD.__init__(self, selectedList, channelid)

    # region Update Server

    # def complete_server(self, text, line, begidx, endidx):
    #     return [i for i in ("start", "stop", "status") if i.startswith(text)]

    # def do_server(self, line):
    #     """\n\tControll the update server\n\n\t\tOptions: status, start, stop"""
    #     try:
    #         if line == "start":
    #             self.mongo_helper.docker_helper.start_nighcap_site()
    #             # NighcapCoreSimpleServer(self.config).start()
    #         elif line == "stop":
    #             self.mongo_helper.docker_helper.stop_nightcapsite()
    #         elif line == "status":
    #             print(self.mongo_helper.docker_helper.get_site_container_status())
    #         else:
    #             raise Exception(
    #                 "Error with server option. For more info use: help server"
    #             )
    #     except Exception as e:
    #         self.printer.print_error(e)

    # endregion

    def do_projects(self, line):
        """\n\nChange current project"""
        try:
            NightcapProjectsCMD().cmdloop()
        except Exception as e:
            print(e)

    def do_settings(self, line):
        print("Settings here")
        ScreenHelper().clearScr()
        NightcapSettingsCMD(self.channelID).cmdloop()
