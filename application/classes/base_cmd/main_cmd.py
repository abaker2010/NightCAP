# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
from application.classes.project.project import NightcapProjects
from nightcapcore.base import NightcapCoreBase
from nightcapcore.configuration import configuration
from application.classes.base_cmd.base_cmd import NightcapBaseCMD
from colorama import Fore, Style
import os

class NightcapMainCMD(NightcapBaseCMD):
    def __init__(self, selectedList, configuration: configuration, packagebase: NightcapCoreBase = None):
        super(NightcapMainCMD, self).__init__(selectedList, configuration, packagebase)


    #region Shell
    def do_shell(self, line):
        "\n\tRun a shell command, becareful with this. This feature is still in beta\n"
        output = os.popen(line).read()
        print("\n{0}{1}{2}".format(Fore.LIGHTGREEN_EX,output, Style.RESET_ALL))
        self.last_output = output
    #endregion

    def do_projects(self, line):
        '''\n\nChange current project'''
        try:
            NightcapProjects(self.package_base, self.config).cmdloop()
        except Exception as e:
            print(e)