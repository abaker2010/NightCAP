# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Imports
import os
from typing import Any, List
from colorama import Fore
from nightcapcore.configuration.configuration import NightcapCLIConfiguration
from nightcapcli.cmds.projects.projects_cmd import NightcapProjectsCMD
from nightcapcli.base.base_cmd import NightcapBaseCMD
from nightcappackages.classes.helpers import NightcapJSONEncoder
from nightcappackages.classes.databases.mogo.mongo_packages import MongoPackagesDatabase

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
    ) -> None:

        NightcapBaseCMD.__init__(self, selectedList, channelid=channelid)
        self.pkg_information = pkg_config
        self.pkg_params = []
        self.db = MongoPackagesDatabase()
        self.generatePcaps = True

        try:
            self.pkg_params = {}
            self.pkg_descripts = {}
            self.pkg_required = {}
            if (
                self.pkg_information["package_information"][
                    "entry_file_optional_params"
                ]
                != {}
            ):
                for k, v in self.pkg_information["package_information"][
                    "entry_file_optional_params"
                ].items():
                    self.pkg_params[v["name"]] = v["value"]
                    self.pkg_descripts[v["name"]] = v["description"]
                    try:
                        self.pkg_required[v["name"]] = bool(v["required"])
                    except:
                        self.pkg_required[v["name"]] = False
        except Exception as e:
            self.printer.print_error(e)
            self.pkg_params = {}

    def do_exit(self, line) -> bool:
        self.printer.debug("Selected list passed to package", self.selectedList)
        return super().do_exit(line)

    # region Show Params
    def show_params(self, detailed: bool = False) -> None:
        try:
            if self.pkg_params != {}:
                self.printer.print_underlined_header("Package Parameters", leadingTab=2)
                if detailed == False:
                    for k, v in self.pkg_params.items():
                        _ = "None" if v == "" else v
                        self.printer.print_formatted_other(
                            "%s%s"
                            % (
                                "(Required) "
                                if bool(self.pkg_required[k]) == True
                                else "",
                                str(k).upper(),
                            ),
                            str(_),
                            leadingTab=3,
                            optionalTextColor=Fore.YELLOW,
                        )
                else:
                    for k, v in self.pkg_params.items():
                        _ = "None" if v == "" else v
                        self.printer.print_formatted_other(
                            "%s%s"
                            % (
                                "(Required) "
                                if bool(self.pkg_required[k]) == True
                                else "",
                                str(k).upper(),
                            ),
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
    def complete_params(self, text, line, begidx, endidx) -> List[str]:
        _ = []
        _.extend(list(dict(self.pkg_params).keys()))
        return [i for i in _ if i.startswith(text)]

    # endregion

    # region Help params
    def help_params(self) -> None:
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
    def do_params(self, line) -> None:
        try:
            if len(line) == 0:
                self.show_params()
            else:
                try:
                    _s = str(line).split(" ")

                    if len(_s) != 2:
                        if _s[0] == "-d":
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
                            if _s[0] in dict(self.pkg_params).keys():
                                self.pkg_params[_s[0]] = str(_s[1])
                except Exception as e:
                    raise e
        except Exception as e:
            self.printer.print_error(e)
        # endregion

    # #region Do Projects
    # def do_projects(self, line) -> None:
    #     """\n\nChange current project"""
    #     try:
    #         NightcapProjectsCMD().cmdloop()
    #     except Exception as e:
    #         print(e)
    # #endregion

    # region Help Run
    def help_run(self):
        self.printer.item_2(
            "Run package",
            leadingTab=1,
            vtabs=1,
            endingBreaks=1,
            leadingText="",
            textColor=Fore.LIGHTGREEN_EX,
        )

    # endregion

    # region Do Run
    def do_run(self, line) -> None:
        try:
            force = False
            if NightcapCLIConfiguration().project == None:
                _ = self.printer.input(
                    "Project not selected for reporting. Would you like to continue? (Y/n)",
                    defaultReturn=True,
                )
                if _:
                    force = True
            else:
                force = True

            if force:
                if self._check_params():
                    _data = self._prepare_data()
                    self._call_package(_data)

            else:
                self.printer.print_error(Exception("User Terminated Scan"))
        except Exception as e:
            self.printer.print_error(e)

    # endregion

    def _check_params(self):
        for k, v in self.pkg_params.items():
            if bool(self.pkg_required[k]):
                if v == "None":
                    raise Exception("Required param: %s" % (k))
        return True

    def _prepare_data(self) -> str:
        dat = {}
        dat[0] = self.toJson()
        dat[1] = self.pkg_params
        dat[2] = self.pkg_information
        return NightcapJSONEncoder().encode(dat)

    def _call_package(self, dat: Any):
        if len(self.selectedList) == 3:
            try:
                exe_path = self.db.get_package_run_path(self.pkg_information)
                try:
                    exe_path = os.path.join(exe_path)
                except Exception as e:
                    pass
                if type(exe_path) == list:
                    exe_path = os.path.join(exe_path)
                if "github" in self.pkg_information["package_information"].keys():
                    flags = ""
                    _flag_pairs = {}
                    if (
                        self.pkg_information["package_information"][
                            "entry_file_optional_params"
                        ]
                        != {}
                    ):
                        for k, v in self.pkg_information["package_information"][
                            "entry_file_optional_params"
                        ].items():
                            try:
                                _required = (
                                    True if v["required"].lower() == "true" else False
                                )
                            except Exception as e:
                                _required = False
                            _flag_pairs[v["name"]] = {
                                "flag": v["corresponding_flag"],
                                "param_needed": bool(v["param_needed"]),
                                "required": _required,
                            }

                    for k, v in self.pkg_params.items():
                        if _flag_pairs[k]["required"] == True:
                            if v == "None" or v == None or v == False:
                                raise Exception("Required Param: " + str(k))
                            else:

                                flags += "%s %s " % (_flag_pairs[k]["flag"], str(v))
                        else:
                            if v != "None" and v != "False":
                                if v.lower() == "true":
                                    flags += "%s " % (_flag_pairs[k]["flag"])

                    call = "%s %s %s" % (
                        self.pkg_information["package_information"]["github"]["lang"],
                        exe_path,
                        flags,
                    )
                    # print(call)
                else:
                    call = "python3.8 %s --data '%s'" % (exe_path, dat)

                # print(call)
                os.system(call)
            except Exception as e:
                self.printer.print_error(e)
        else:
            self.printer.print_error(Exception("Package not selected to be used"))
            print(self.selectedList)

    # region Update
    def cli_update(self, message) -> bool:
        print("Trying to update from package cmd")
        self.do_exit()

    # endregion

    # region To JSON
    def toJson(self) -> dict:

        js = {
            "project": None
            if NightcapCLIConfiguration().project == None
            else NightcapCLIConfiguration().project
        }
        return js

    # endregion
