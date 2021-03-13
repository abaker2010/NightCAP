# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.

from nightcapcore import NightcapCLIConfiguration
from nightcapserver import NighcapCoreSimpleServer
from colorama import Fore, Style
from ..base import NightcapBaseCMD
# from .projects_cmd import NightcapProjectsCMD
import os

class NightcapMainCMD(NightcapBaseCMD):
    def __init__(self, selectedList, configuration: NightcapCLIConfiguration):
        super(NightcapMainCMD, self).__init__(selectedList, configuration)

    #region Shell
    def do_shell(self, line):
        "\n\tRun a shell command, becareful with this. This feature is still in beta\n"
        output = os.popen(line).read()
        print("\n{0}{1}{2}".format(Fore.LIGHTGREEN_EX,output, Style.RESET_ALL))
        self.last_output = output
    #endregion

    #region Update Server
    def do_server(self,line):
        '''\n\tControll the update server\n\n\t\tOptions: status, start, stop'''
        try:
            if(line == "start"):
                NighcapCoreSimpleServer.instance().start()
            elif(line == "stop"):
                NighcapCoreSimpleServer.instance().shutdown()
            elif (line == "status"):
                print(NighcapCoreSimpleServer.instance().get_status())
        except Exception as e:
            print(e)
    #endregion

    # def do_projects(self, line):
    #     '''\n\nChange current project'''
    #     try:
    #         NightcapProjectsCMD(self.config).cmdloop()
    #     except Exception as e:
    #         print(e)