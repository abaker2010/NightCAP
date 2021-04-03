# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
import os
import copy
import json
from nightcapcli.cmds.projects.projects_cmd import NightcapProjectsCMD
from nightcapcli.observer.publisher import NightcapCLIPublisher
from nightcapcore.configuration.configuration import NightcapCLIConfiguration
from nightcapcore.configuration.package_config import NightcapCLIPackageConfiguration
from nightcappackages.classes.databases.mogo.mongo_packages import MongoPackagesDatabase
from nightcapcli.base.base_cmd import NightcapBaseCMD

from colorama import Fore, Style


class NightcapCLIPackage(NightcapCLIPackageConfiguration, NightcapBaseCMD):
    def __init__(
        self,
        selectedList: list,
        pkg_config: dict = None,
        channelid: str = None,
    ):
        NightcapCLIPackageConfiguration.__init__(self, pkg_config)
        NightcapBaseCMD.__init__(self, selectedList)
        # self.config.generatePcaps = True
        
        # self._pconfig = configuration
        self.db = MongoPackagesDatabase()

        try:
            self.package_params = copy.deepcopy(
                pkg_config["package_information"]["entry_file_optional_params"]
            )
        except Exception as e:
            self.printer.print_error(e)
            self.package_params = None

    # def __del__(self):

    def do_projects(self, line):
        """\n\nChange current project"""
        try:
            NightcapProjectsCMD().cmdloop()
        except Exception as e:
            print(e)

    def help_run(self):
        self.printer.item_2(
            "Run package",
            leadingTab=1,
            vtabs=1,
            endingBreaks=1,
            leadingText="",
            textColor=Fore.LIGHTGREEN_EX,
        )

    def do_run(self, line):
        print("project information:", self.config.project)
        print("package information:", self.pkg_information,"\n")
        try:
            force = False
            if self.config.project == None:
                force = input(
                    (
                        Fore.YELLOW
                        + "Project not selected to be used would you like to continue? [Y/n]: "
                        + Fore.GREEN
                    )
                )
                print(Style.RESET_ALL, Fore.LIGHTCYAN_EX)
                print("config", type(self.config))
                yes_options = self.config.config["NIGHTCAPCORE"]["yes"].split(" ")
                if force == None:
                    force = False
                else:
                    if force in yes_options:
                        force = True
            else:
                force = True

            if force == True:
                if len(self.selectedList) == 3:
                    print("List to be used to find run path", self.selectedList)
                    exe_path = self.db.get_package_run_path(self.pkg_information)
                    print(exe_path)
                    dat = {}
                    dat[0] = self.toJson()
                    dat[1] = self.package_params
                    dat[2] = self.pkg_information
                    print("data before passing: ", dat)
                    call = "python3.8 %s --data '%s'" % (exe_path, json.dumps(dat, default=str))
                    os.system(call)
                else:
                    print("Package not selected to be used")
            else:
                self.printer.print_error(Exception("Scan canceled by user"))
        except Exception as e:
            self.printer.print_error(e)

    def cli_update(self, message):
        print("Trying to update from package cmd")
        self.do_exit()
