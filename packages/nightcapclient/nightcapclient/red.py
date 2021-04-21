# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Imports
import argparse
import json
import abc
import os
import sys
import time
from abc import abstractmethod
from colorama import Fore
from colorama.ansi import Style
from nightcapcli.base.base_cmd import NightcapBaseCMD
from nightcapcore.configuration.package_config import NightcapCLIPackageConfiguration
from nightcapcore.printers.print import Printer
import pyshark
from pyshark.packet.packet import Packet
# endregion

class NightcapRedTeam(NightcapBaseCMD):
    def __init__(self, intro: str = None, *args, debug=False, **kwargs):

        parser = argparse.ArgumentParser(description="Process some pcaps.")
        parser.add_argument("--data", required=True,
                            help="list of pcap filenames")
        args = parser.parse_args()
        self.printer = Printer()

        
        _data = dict(json.loads(args.data))
        self.base_params = _data["0"]
        self.package_params = _data["1"]

        
        try:
            NightcapBaseCMD.__init__(
                    self, dict(json.loads(args.data))["2"], passedJson=dict(
                        json.loads(args.data))["0"]
                )

            self.printer.debug("Args after passing", args,
                           currentMode=self.config.verbosity)
        except Exception as e:
            self.printer.print_error(e)
     # region onClose

    def onClose(self):
        """Todo when the process is done"""
        try:
            self.printer.print_formatted_check('Elapse time (seconds)', str(
                round(self._elapseTime, 3)), endingBreaks=1)
        except Exception as e:
            print(e)
    # endregion

    # region onConsolePrint
    @abc.abstractmethod
    def onConsolePrint(self):
        """Generate Console Report"""
        raise NotImplementedError

    # endregion

    # region onIntro
    def onIntro(self):
        """Intro to the program"""
        # self.printer.print_underlined_header("Scanning with arguments")
        # self.show_params()
        # self.printer.item_1("*"*30, leadingText="", endingBreaks=1, leadingTab=1)
        pass

    # endregion

    # region onProcess
    @abc.abstractmethod
    def onProcess(self):
        """Process to do"""
        raise NotImplementedError

    # endregion

    # region onReport
    @abc.abstractmethod
    def onReport(self):
        """Generate Reports"""
        raise NotImplementedError

    # endregion

    # region onRun
    def onRun(self):
        """Run the program"""
        try:
            self.onIntro()
        except Exception as e:
            self.printer.print_error(Exception("Error with Intro"))
            raise e

        try:
            start = time.time()
            self.onProcess()
            # for cpt in self.get_pcaps(display_filter=self._display_filter):
            #     _count = 1
            #     for pkt in cpt:
            #         # print(type(pkt))
            #         sys.stdout.write(Fore.LIGHTCYAN_EX + "\r\t\t[?] " + Fore.LIGHTGREEN_EX +
            #                          "Scanning Packet # : " + Fore.LIGHTYELLOW_EX + str(_count) + Style.RESET_ALL)
            #         try:
            #             self.onProcess(pkt, _count)
            #         except Exception as e:
            #             print("There has been an error")
            #             print(e)
            #             pass
            #         _count += 1
            self._elapseTime = time.time() - start
            print("")
        except Exception as e:
            self.printer.print_error(Exception("Error with Processing"))
            print(e)
            # raise e

        try:
            self.onReport()
        except Exception as e:
            self.printer.print_error(Exception("Error with Reporting"))
            raise e

        try:
            self.onConsolePrint()
        except Exception as e:
            self.printer.print_error(Exception("Error with Console Printing"))
            raise e

        try:
            self.onClose()
        except Exception as e:
            self.printer.print_error(Exception("Error with Closing"))
            raise e

    # endregion

    # region run
    def run(self):
        self.onRun()

    # endregion


# region Show Params
    # def show_params(self, detailed: bool = False):

    #     # if self.project == None:
    #     #     proj = "None"
    #     # else:
    #     #     proj = Fore.LIGHTYELLOW_EX + str(self.project["project_name"])

    #     self.printer.print_underlined_header("Base Parameters", leadingTab=2)
        # self.printer.print_formatted_other(
        #     "PROJECT",
        #     proj,
        #     leadingTab=3,
        #     optionalTextColor=Fore.YELLOW,
        # )

        # if detailed == False:
        #     self.printer.print_formatted_other(
        #         "FILENAME",
        #         str(self.config.filename),
        #         leadingTab=3,
        #         optionalTextColor=Fore.YELLOW,
        #     )
        # else:
        #     self.printer.print_formatted_other(
        #         "FILENAME",
        #         "Pcap file name to be used for the scan",
        #         leadingTab=3,
        #         optionalTextColor=Fore.MAGENTA,
        #     )
        #     self.printer.print_formatted_additional(
        #         "Current Value",
        #         str(self.config.filename),
        #         leadingTab=4,
        #         optionalTextColor=Fore.YELLOW,
        #         endingBreaks=1
        #     )

        # # if detailed == False:
        # #     self.printer.print_formatted_other(
        # #         "ISDIR",
        # #         str(self.config.isDir),
        # #         leadingTab=3,
        # #         optionalTextColor=Fore.YELLOW,
        # #     )
        # # else:
        # #     self.printer.print_formatted_other(
        # #         "ISDIR",
        # #         "To either try and scan the pcap file or a directory of pcap files",
        # #         leadingTab=3,
        # #         optionalTextColor=Fore.MAGENTA,
        # #     )
        # #     self.printer.print_formatted_additional(
        # #         "Current Value",
        # #         str(self.config.isDir),
        # #         leadingTab=4,
        # #         optionalTextColor=Fore.YELLOW,
        # #         endingBreaks=1
        # #     )

        # # if detailed == False:
        # #     self.printer.print_formatted_other(
        # #         "PATH",
        # #         str(self.config.dir),
        # #         leadingTab=3,
        # #         optionalTextColor=Fore.YELLOW,
        # #     )
        # # else:
        # #     self.printer.print_formatted_other(
        # #         "PATH",
        # #         "The directory of the pcap file(s)",
        # #         leadingTab=3,
        # #         optionalTextColor=Fore.MAGENTA,
        # #     )
        # #     self.printer.print_formatted_additional(
        # #         "Current Value",
        # #         str(self.config.dir),
        # #         leadingTab=4,
        # #         optionalTextColor=Fore.YELLOW,
        # #         endingBreaks=1
        # #     )

        # try:
        #     if self.pkg_params != {}:

        #         self.printer.print_underlined_header(
        #             "Package Parameters", leadingTab=2)
        #         if detailed == False:
        #             for k, v in self.pk.items():
        #                 _ = "None" if v == "" else v
        #                 self.printer.print_formatted_other(
        #                     str(k).upper(),
        #                     str(_),
        #                     leadingTab=3,
        #                     optionalTextColor=Fore.YELLOW,
        #                 )
        #         else:
        #             for k, v in self.pkg_params.items():
        #                 _ = "None" if v == "" else v
        #                 self.printer.print_formatted_other(
        #                     str(k).upper(),
        #                     str(self.pkg_descripts[k]),
        #                     leadingTab=3,
        #                     optionalTextColor=Fore.MAGENTA,
        #                 )
        #                 self.printer.print_formatted_other(
        #                     "Current Value",
        #                     str(_),
        #                     leadingTab=4,
        #                     optionalTextColor=Fore.YELLOW,
        #                 )
        # except Exception as e:
        #     pass
        # print()
    # endregion
