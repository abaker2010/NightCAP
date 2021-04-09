# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Imports
import os
import copy
import json
from nightcapcli.cmds.projects.projects_cmd import NightcapProjectsCMD
from nightcapcore.configuration.configuration import NightcapCLIConfiguration
from nightcapcore.configuration.package_config import NightcapCLIPackageConfiguration
from nightcappackages.classes.databases.mogo.mongo_packages import MongoPackagesDatabase
from nightcapcli.base.base_cmd import NightcapBaseCMD
from colorama import Fore, Style

# endregion


class NightcapCLIPackage(NightcapBaseCMD):
    """
    (User CLI Object)

    This class is used for the packages cli. IE: [<T>][<T>][<T>]

    ...

    Attributes
    ----------
        ** Not including inherited attrs from NightcapCLIPackageConfiguration, NightcapBaseCMD

        db: -> MongoPackagesDatabase
            Returns an instance of the MongoPackagesDatabase

        package_params: -> dict
            The package parameters for the currently selected package

    Methods
    -------
        Accessible
        -------
            do_projects(self, line): -> None:
                Enters into the projects cmd

            help_run(self, line): -> None
                Override for the runs help command

            do_run(self, line): -> None
                Allows the user to run the selected package

            do_update(self, line): -> None
                Trys to update, currently not working and looks like wrong place for the code


    """

    # region Init
    def __init__(
        self,
        selectedList: list,
        pkg_config: dict = None,
        channelid: str = "",
    ):
        
        NightcapBaseCMD.__init__(self, selectedList, channelid=channelid)
        self.pkg_information = pkg_config
        self.pkg_params = []
        self.db = MongoPackagesDatabase()
        self.generatePcaps = True

        #     # NightcapCLIPackageConfiguration.__init__(self, pkg_config)
        
        #     # self.config.generatePcaps = True

        #     # self._pconfig = configuration
        #     self.db = MongoPackagesDatabase()
        #     try:
        #         self.package_params = copy.deepcopy(
        #             pkg_config["package_information"]["entry_file_optional_params"]
        #         )
        #     except Exception as e:
        #         self.printer.print_error(e)
        #         self.package_params = None
        #     print("Package object: ", selectedList)
        # # endregion

        try:
            self.pkg_params = {}
            self.pkg_descripts = {}
            if self.pkg_information["package_information"]["entry_file_optional_params"] != {}:
                for k, v in self.pkg_information["package_information"]["entry_file_optional_params"].items():
                    self.pkg_params[v["name"]] = v["value"]
                    self.pkg_descripts[v["name"]] = v["description"]

            # print("Deep copied params", self.package_params)
        except Exception as e:
            self.printer.print_error(e)
            self.pkg_params = {}
        
        print("Params:", self.pkg_params)
        # print(self.package_params)


    def do_exit(self, line):
        print("Selected list passed to package: ", self.selectedList)
        return super().do_exit(line)




    # region Show Params
    def show_params(self, detailed: bool = False):

        # if self.project == None:
        #     proj = "None"
        # else:
        #     proj = Fore.LIGHTYELLOW_EX + str(self.project["project_name"])

        self.printer.print_underlined_header("Base Parameters", leadingTab=2)
        # self.printer.print_formatted_other(
        #     "PROJECT",
        #     proj,
        #     leadingTab=3,
        #     optionalTextColor=Fore.YELLOW,
        # )

        if detailed == False:
            self.printer.print_formatted_other(
                "FILENAME",
                str(self.filename),
                leadingTab=3,
                optionalTextColor=Fore.YELLOW,
            )
        else:
            self.printer.print_formatted_other(
                "FILENAME",
                "Pcap file name to be used for the scan",
                leadingTab=3,
                optionalTextColor=Fore.MAGENTA,
            )
            self.printer.print_formatted_additional(
                "Current Value",
                str(self.filename),
                leadingTab=4,
                optionalTextColor=Fore.YELLOW,
                endingBreaks=1
            )

        if detailed == False:
            self.printer.print_formatted_other(
                "ISDIR",
                str(self.isDir),
                leadingTab=3,
                optionalTextColor=Fore.YELLOW,
            )
        else:
            self.printer.print_formatted_other(
                "ISDIR",
                "To either try and scan the pcap file or a directory of pcap files",
                leadingTab=3,
                optionalTextColor=Fore.MAGENTA,
            )
            self.printer.print_formatted_additional(
                "Current Value",
                str(self.isDir),
                leadingTab=4,
                optionalTextColor=Fore.YELLOW,
                endingBreaks=1
            )


        if detailed == False:
            self.printer.print_formatted_other(
                "PATH",
                str(self.dir),
                leadingTab=3,
                optionalTextColor=Fore.YELLOW,
            )
        else:
            self.printer.print_formatted_other(
                "PATH",
                "The directory of the pcap file(s)",
                leadingTab=3,
                optionalTextColor=Fore.MAGENTA,
            )
            self.printer.print_formatted_additional(
                "Current Value",
                str(self.dir),
                leadingTab=4,
                optionalTextColor=Fore.YELLOW,
                endingBreaks=1
            )

        try:
            if self.pkg_params != {}:

                self.printer.print_underlined_header("Package Parameters", leadingTab=2)
                if detailed == False:
                    for k, v in self.pkg_params.items():
                        _ = "None" if v == "" else v
                        self.printer.print_formatted_other(
                            str(k).upper(),
                            str(_),
                            leadingTab=3,
                            optionalTextColor=Fore.YELLOW,
                        )
                else:
                    for k, v in self.pkg_params.items():
                        _ = "None" if v == "" else v
                        self.printer.print_formatted_other(
                            str(k).upper(),
                            str(self.pkg_descripts[k]),
                            leadingTab=3,
                            optionalTextColor=Fore.MAGENTA,
                        )
                        self.printer.print_formatted_other(
                            "Current Value",
                            str(_),
                            leadingTab=4,
                            optionalTextColor=Fore.YELLOW,
                        )
        except Exception as e:
            pass
        print()

    # endregion

    # region Complete params
    def complete_params(self, text, line, begidx, endidx):
        _ = ["isdir", "filename", "path"]
        _.extend(list(dict(self.pkg_params).keys()))
        return [i for i in _ if i.startswith(text)]

    # endregion

    # region Help params
    def help_params(self):
        self.printer.item_2(
            "see parameters",
            "params",
            leadingTab=1,
            vtabs=1,
            leadingText="",
            textColor=Fore.LIGHTGREEN_EX,
        )
        self.printer.item_2(
            "set parameters",
            "params [PARAM] [PARAMVALUE]",
            leadingTab=1,
            endingBreaks=1,
            leadingText="",
            textColor=Fore.LIGHTGREEN_EX,
        )

    # endregion

    # region Do params
    def do_params(self, line):
        try:
            if len(line) == 0:
                self.show_params()
            else:
                try:
                    _s = str(line).split(" ")

                    if len(_s) != 2:
                        if _s[0] == '-d':
                            self.show_params(detailed=True)
                        else:
                            raise Exception("Paramater Error.")
                    else:
                        if _s[0].lower() == "project":
                            self.printer.print_error(
                                Exception(
                                    "Projects not allowed to be set this way. Please use the projects command."
                                )
                            )
                        else:
                            if _s[0].lower() == "isdir":
                                try:
                                    _ = None
                                    if str(_s[1]).lower() == "true":
                                        _ = True
                                    elif str(_s[1]).lower() == "false":
                                        _ = False
                                    else:
                                        raise Exception("Please use either True or False")
                                    self.isDir = _
                                except Exception as e:
                                    raise e
                            elif _s[0].lower() == "path":
                                try:
                                    self.dir = str(_s[1])
                                except Exception as e:
                                    raise e
                            elif _s[0].lower() == "filename":
                                try:
                                    self.filename = str(_s[1])
                                except Exception as e:
                                    raise e
                            else:
                                if _s[0] in dict(self.pkg_params).keys():
                                    self.pkg_params[_s[0]] = str(_s[1])
                except Exception as e:
                    raise e
        except Exception as e:
            self.printer.print_error(e)
        # endregion

    #region Do Projects
    def do_projects(self, line):
        """\n\nChange current project"""
        try:
            NightcapProjectsCMD().cmdloop()
        except Exception as e:
            print(e)
    #endregion

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
        # print("project information:", self.config.project)
        # print("package information:", self.pkg_information, "\n")
        try:
            force = False
            if self.project == None:
                force = input(
                    (
                        Fore.YELLOW
                        + "Project not selected to be used would you like to continue? [Y/n]: "
                        + Fore.GREEN
                    )
                )
                print(Style.RESET_ALL, Fore.LIGHTCYAN_EX)
                # print("config", type(self.config))
                yes_options = self.config.config.get("NIGHTCAPCORE","yes").split(" ")
                if force == None:
                    force = False
                else:
                    if force in yes_options:
                        force = True
            else:
                force = True

            if force == True:
                if len(self.selectedList) == 3:
                    # print("List to be used to find run path", self.selectedList)
                    exe_path = self.db.get_package_run_path(self.pkg_information)
                    print(self.pkg_information)
                    # print(exe_path)
                    dat = {}
                    dat[0] = self.toJson()
                    dat[1] = self.pkg_params
                    dat[2] = self.pkg_information
                    # print("data before passing: ", dat)
                    call = "python3.8 %s --data '%s'" % (
                        exe_path,
                        json.dumps(dat, default=str),
                    )
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

    # region To JSON
    def toJson(self):
        js = {
            "project": self.project,
            "isDir": self.isDir,
            "dir": self.dir,
            "filename": self.filename,
        }
        return js

    # endregion
