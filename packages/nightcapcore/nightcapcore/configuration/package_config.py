# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
import copy
import os
from nightcapcore.printers.print import Printer
import pyshark
from abc import ABC
from pathlib import Path
from colorama import Fore, Style
from nightcapcore.configuration.configuration import NightcapCLIConfiguration

class NightcapCLIPackageConfiguration(NightcapCLIConfiguration):
    def __init__(
        self, pkg_information: dict
    ):
        NightcapCLIConfiguration.__init__(self)
        # NightcapCLIConfiguration.__init__(self)
        # self.config = config
        self.pkg_information = pkg_information
        self.pkg_params = []
        self.printer = Printer()
        self.generatePcaps = True
        
        try:
            self.pkg_params = copy.deepcopy(
                pkg_information["package_information"]["entry_file_optional_params"]
            )
            # print("Deep copied params", self.package_params)
        except Exception as e:
            self.printer.print_error(e)
            self.package_params = None
        # print("Generate pcap files package_conf", self.config.generatePcaps)
        # self.pcaps = self._get_pcaps() if self.config.generatePcaps == True else []

    #region Show Params
    def show_params(self):

        if self.project == None:
            proj = "None"
        else:
            proj = Fore.LIGHTYELLOW_EX + str(self.project["project_name"])

            
        self.printer.print_underlined_header("Base Parameters", leadingTab=2)
        self.printer.print_formatted_other(
            "PROJECT",
            proj,
            leadingTab=3,
            optionalTextColor=Fore.YELLOW,
        )
        self.printer.print_formatted_other(
            "FILENAME",
            str(self.filename),
            leadingTab=3,
            optionalTextColor=Fore.YELLOW,
        )
        self.printer.print_formatted_other(
            "ISDIR",
            str(self.isDir),
            leadingTab=3,
            optionalTextColor=Fore.YELLOW,
        )
        self.printer.print_formatted_other(
            "PATH",
            str(self.dir),
            leadingTab=3,
            optionalTextColor=Fore.YELLOW,
        )

        if self.package_params != {}:
            self.printer.print_underlined_header("Package Parameters", leadingTab=2)
            for k, v in self.pkg_params.items():
                _ = "None" if v == "" else v
                self.printer.print_formatted_other(
                    str(k).upper(),
                    str(_),
                    leadingTab=3,
                    optionalTextColor=Fore.YELLOW,
                )
        print()

    #endregion


    def complete_params(self, text, line, begidx, endidx):
        _ = ["isdir", "filename", "path"]
        _.extend(list(dict(self.pkg_params).keys()))
        return [i for i in _ if i.startswith(text)]

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

    def do_params(self,line):
        if len(line) == 0:
            self.show_params()
        else:
            try:
                _s = str(line).split(" ")

                if len(_s) != 2:
                    raise Exception("Paramater Error.")
                else:
                    if _s[0].lower() == "project":
                        self.printer.print_error(Exception("Projects not allowed to be set this way. Please use the projects command."))
                    else:
                        if _s[0].lower() == "isdir":
                            try:
                                _ = None
                                if str(_s[1]).lower() == 'true':
                                    _ = True
                                elif str(_s[1]).lower() == 'false':
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
        
    def _get_pcaps(self):
        try:
            _pcapFiles = []
            print("Trying to generate pcaps")
            if self.isDir:
                exts = self["NIGHTCAPCORE"]["extentions"].split(" ")

                for root, dirs, files in os.walk(self.dir, topdown=False):
                    for name in files:
                        if str(name).split(".")[1] in exts:
                            _pcapFiles.append(
                                pyshark.FileCapture(os.path.join(root, name))
                            )
            else:
                _pcapFiles.append(pyshark.FileCapture(os.path.join(self.dir, self.filename)))
            return _pcapFiles
        except Exception as e:
            self.printer.print_error(e)
            return []

    def toJson(self):
        js = {
            "project": self.project,
            "isDir": self.isDir,
            "dir": self.dir,
            "filename": self.filename
        }
        return js
    
