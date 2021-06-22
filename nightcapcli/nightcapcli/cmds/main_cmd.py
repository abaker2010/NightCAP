# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Imports
from typing import List
from nightcapcli.cmds.cmd_shared.shell_cmd import ShellCMDMixin
from nightcapcli.cmds.projects import NightcapProjectsCMD

# from nightcapserver.helpers.django_helper import NightcapDjangoDockerHelper
from ..base import NightcapBaseCMD
from nightcapcore import ScreenHelper
from nightcapcli.cmds.settings import NightcapSettingsCMD

# endregion


class NightcapMainCMD(NightcapBaseCMD, ShellCMDMixin):
    def __init__(
        self,
        selectedList,
        channelid: str = None,
    ) -> None:
        NightcapBaseCMD.__init__(self, selectedList, channelid)

    # #region Update Server
    # def complete_server(self, text, line, begidx, endidx) -> List[str]:
    #     return [i for i in ("start", "stop", "status") if i.startswith(text)]

    # def do_server(self, line) -> None:
    #     """\n\tControll the update server\n\n\t\tOptions: status, start, stop"""
    #     _helper = NightcapDjangoDockerHelper()
    #     try:
    #         if line == "start":
    #             _helper.container_start()
    #             # self.mongo_helper.docker_helper.start_nighcap_site()
    #         elif line == "stop":
    #             _helper.continer_stop()
    #             # self.mongo_helper.docker_helper.stop_nightcapsite()
    #         elif line == "status":
    #            self.printer.print_formatted_additional("Website Status", _helper.container_status().value, leadingBreaks=1)
    #             # print(self.mongo_helper.docker_helper.get_site_container_status())
    #         else:
    #             raise Exception(
    #                 "Error with server option. For more info use: help server"
    #             )
    #     except Exception as e:
    #         self.printer.print_error(e)

    # # endregion

    # #region Projects
    # def do_projects(self, line) -> None:
    #     """\n\nChange current project"""
    #     try:
    #         NightcapProjectsCMD().cmdloop()
    #     except Exception as e:
    #         print(e)
    # #endregion

    # region Settings
    def do_settings(self, line) -> None:
        print("Settings here")
        ScreenHelper().clearScr()
        NightcapSettingsCMD(self.channelID).cmdloop()

    # endregion
