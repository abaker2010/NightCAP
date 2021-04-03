# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.

from random import randint
from mongo.mongo_helper import NightcapMongoHelper
from nightcapcli.generator.option_generator import NightcapOptionGenerator
from nightcapcli.observer.publisher import NightcapCLIPublisher
from nightcapcore import NightcapCLIConfiguration, Printer, ScreenHelper, NightcapBanner
from nightcapcore.colors.nightcap_colors import NightcapColors
from nightcappackages import *
import cmd
from colorama import Fore, Style
from nightcapserver.server.server import NighcapCoreSimpleServer

try:
    from subprocess import DEVNULL  # py3k
except ImportError:
    import os

    DEVNULL = open(os.devnull, "wb")


class NightcapBaseCMD(cmd.Cmd):
    def __init__(
        self,
        selectedList: list,
        channelid=None,
    ):
        cmd.Cmd.__init__(self, completekey="tab", stdin=None, stdout=None)
        if selectedList != []:
            self.selectedList = selectedList
        else:
            self.selectedList = (
                []
                if NightcapCLIPublisher().selectedList == []
                else NightcapCLIPublisher().selectedList
            )
        itm = (
            ""
            if self.selectedList == None
            else list(
                map(
                    lambda v: "[" + Fore.LIGHTYELLOW_EX + v + Fore.LIGHTGREEN_EX + "]",
                    self.selectedList,
                )
            )
        )
        self.prompt = Fore.GREEN + "nightcap" + "".join(itm) + " > " + Fore.CYAN
        self.doc_header = Fore.GREEN + "Commands" + Style.RESET_ALL
        self.misc_header = Fore.GREEN + "System" + Style.RESET_ALL
        self.undoc_header = Fore.GREEN + "Other" + Style.RESET_ALL
        self.ruler = Fore.YELLOW + "-" + Style.RESET_ALL

        self.config = NightcapCLIConfiguration()
        self.verbosity = self.config.config.getboolean('NIGHTCAPCORE','verbose')
        self.printer = Printer()
        self.mongo_helper = NightcapMongoHelper(self.config)
        self.channelID = channelid

    def emptyline(self):
        pass

    # putting into place to be used later
    def preloop(self) -> None:
        return super().preloop()

    def postcmd(self, stop: bool, line: str) -> bool:
        # print("Post cmd loop")
        return super().postcmd(stop, line)

    def postloop(self) -> None:
        return super().postloop()

    #####

    def do_exit(self, line):
        ScreenHelper().clearScr()
        try:
            if self.channelID != None:
                #     self.printer.print_formatted_check(text="No channel ID attached to unregister")
                # else:
                NightcapCLIPublisher().del_channel(self.channelID)
        except Exception as e:
            pass
        return True

    # endregion

    def do_help(self, line):
        super(NightcapBaseCMD, self).do_help(line)

    def help_config(self):
        self.printer.help("Get the current system configuration(s)")

    def do_config(self, line):
        ScreenHelper().clearScr()
        self.printer.print_underlined_header_undecorated("Configuration")

        self.printer.print_underlined_header("Verbosity", leadingTab=2)
        self.printer.print_formatted_other(
                    "Verbosity", "Normal" if self.verbosity == False else "Debug", leadingTab=3,
                    optionalTextColor=Fore.LIGHTBLACK_EX if self.verbosity == False else Fore.LIGHTYELLOW_EX
                )

        self.printer.print_underlined_header("Projects", leadingTab=2)
        if len(line) == 0:
            if self.config.project != None:
                self.printer.print_formatted_other(
                    "Current Project",
                    str(self.config.project["project_name"]),
                    leadingTab=3,
                    optionalTextColor=Fore.LIGHTMAGENTA_EX,
                )
            else:
                self.printer.print_formatted_other(
                    "Current Project", "None", leadingTab=3
                )

        self.printer.print_underlined_header("Web Server (Django)", leadingTab=2)
        self.printer.print_formatted_other(
            "IP",
            self.config.config["REPORTINGSERVER"]["ip"],
            leadingTab=3,
            optionalTextColor=Fore.YELLOW,
        )
        self.printer.print_formatted_other(
            "Port",
            self.config.config["REPORTINGSERVER"]["port"],
            leadingTab=3,
            optionalTextColor=Fore.YELLOW,
        )
        self.printer.print_formatted_other(
            "URL",
            NighcapCoreSimpleServer(self.config).get_url(),
            leadingTab=3,
            optionalTextColor=Fore.YELLOW,
        )
        self.printer.print_formatted_other(
            "Status",
            NighcapCoreSimpleServer(self.config).get_status(),
            leadingTab=3,
            optionalTextColor=Fore.LIGHTGREEN_EX
            if NighcapCoreSimpleServer(self.config).get_status() == "UP"
            else Fore.MAGENTA,
        )

        self.printer.print_underlined_header("Database (Mongo)", leadingTab=2)
        self.printer.print_formatted_other(
            "URL",
            self.config.config["MONGOSERVER"]["ip"],
            leadingTab=3,
            optionalTextColor=Fore.YELLOW,
        )
        self.printer.print_formatted_other(
            "Status",
            self.config.config["MONGOSERVER"]["port"],
            leadingTab=3,
            optionalTextColor=Fore.YELLOW,
            endingBreaks=1,
        )

    def do_banner(self, line):
        ScreenHelper().clearScr()
        NightcapBanner().Banner()
