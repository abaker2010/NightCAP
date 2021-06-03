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
# region Imports
import copy
import os
from nightcapcore.printers.print import Printer
import pyshark
from abc import ABC
from pathlib import Path
from colorama import Fore, Style
from nightcapcore.configuration.configuration import NightcapCLIConfiguration

# endregion


class NightcapCLIPackageConfiguration(NightcapCLIConfiguration):
    """

    This class is used for the package configuration

    ...

    Attributes
    ----------
        pkg_information: -> dict
            This is the package information for the selected package

        pkg_params: -> dict
            Required parameters for the package

        printer: -> Printer
            Console printer

        generatePcaps: -> bool
            If the object should generate the FileCaputre list

    Methods
    -------
        Accessible
        -------
            show_params(self): -> None
                Print a list of the parameters

            complete_params(self, text, line, begidx, endidx): -> list
                Tab auto complete for the package params

            help_params(self): -> None
                Override for the params help options

            do_params(self,line): -> None
                Allows the users to set/view the params. (-d for detailed view)

            toJson(self): -> dict
                Returns a json object of the object


        None Accessible
        -------
            _get_pcaps(self): -> list
                Returns an empty list or a list of FileCaptures that were specified in the params

    """

    # region Init
    def __init__(self, pkg_information: dict, data: dict = None) -> None:
        NightcapCLIConfiguration.__init__(self, data=data)
        # NightcapCLIConfiguration.__init__(self)
        # self.config = config
        self.pkg_information = pkg_information
        self.pkg_params = []
        self.printer = Printer()
        self.generatePcaps = True

        try:
            self.pkg_params = {}
            self.pkg_descripts = {}
            if pkg_information["package_information"]["entry_file_optional_params"] != {}:
                for k, v in pkg_information["package_information"]["entry_file_optional_params"].items():
                    self.pkg_params[v["name"]] = v["value"]
                    self.pkg_descripts[v["name"]] = v["description"]

            # print("Deep copied params", self.package_params)
        except Exception as e:
            self.printer.print_error(e)
            self.package_params = None
        # print("Generate pcap files package_conf", self.config.generatePcaps)
        # self.pcaps = self._get_pcaps() if self.config.generatePcaps == True else []
    # endregion

    # region Show Params
    def show_params(self, detailed: bool = False) -> None:

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
            if self.package_params != {}:

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
    def complete_params(self, text, line, begidx, endidx) -> list:
        _ = ["isdir", "filename", "path"]
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

    # region Get pcaps
    def get_pcaps(self, *args, keep_packets=True, display_filter=None, only_summaries=False,
                 decryption_key=None, encryption_type="wpa-pwk", decode_as=None,
                 disable_protocol=None, tshark_path=None, override_prefs=None,
                 use_json=False, output_file=None, include_raw=False, eventloop=None, custom_parameters=None,
                 debug=False, **kwargs) -> None:
        try:
            _pcapFiles = []
            # print("Trying to generate pcaps")Generating Reports
            if self.isDir:
                exts = self["NIGHTCAPCORE"]["extentions"].split(" ")

                for root, dirs, files in os.walk(self.dir, topdown=False):
                    for name in files:
                        if str(name).split(".")[1] in exts:
                            _pcapFiles.append(
                                pyshark.FileCapture(
                                    os.path.join(root, name),
                                    display_filter=display_filter,
                                    keep_packets=keep_packets,
                                    only_summaries=only_summaries,
                                    decryption_key=decryption_key,
                                    encryption_type=encryption_type,
                                    decode_as=decode_as,
                                    disable_protocol=disable_protocol,
                                    tshark_path=tshark_path,
                                    override_prefs=override_prefs,
                                    use_json=use_json,
                                    output_file=output_file,
                                    include_raw=include_raw,
                                    eventloop=eventloop,
                                    custom_parameters=custom_parameters,
                                    debug=debug
                                )
                            )
            else:
                _pcapFiles.append(
                    pyshark.FileCapture(
                        os.path.join(self.dir, self.filename), 
                        display_filter=display_filter,
                        keep_packets=keep_packets,
                        only_summaries=only_summaries,
                        decryption_key=decryption_key,
                        encryption_type=encryption_type,
                        decode_as=decode_as,
                        disable_protocol=disable_protocol,
                        tshark_path=tshark_path,
                        override_prefs=override_prefs,
                        use_json=use_json,
                        output_file=output_file,
                        include_raw=include_raw,
                        eventloop=eventloop,
                        custom_parameters=custom_parameters,
                        debug=debug
                    )
                )
            return _pcapFiles
        except Exception as e:
            self.printer.print_error(e)
            return []

    # endregion

    # region To JSON
    def toJson(self) -> dict:
        js = {
            "project": self.project,
            "isDir": self.isDir,
            "dir": self.dir,
            "filename": self.filename,
        }
        return js

    # endregion
