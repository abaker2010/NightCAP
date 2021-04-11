# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
import os
from mongo.mongo_helper import NightcapMongoHelper
from nightcapcli.observer.publisher import NightcapCLIPublisher
from nightcapcore import NightcapCLIConfiguration, Printer, ScreenHelper, NightcapBanner
from nightcapcore.test_pcaps.test_pcaps import TestPcaps
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
    """
    This class is used as the base cmd for the program

    ...

    Attributes
    ----------
        selectedList:
            List for the consolses [<T>][<T>]

        channleID:
            The channel for the object

        config:
            NightcapCLIConfiguration, this is the main one for the program

        verbosity:
            Verbosity for the console printing

        printer:
            Printer object for the program

        mongo_helper:
            MongoDB Helper Object

    Methods
    -------
        emptyline(self):
            Override to keep the enter key cleaned up

        preloop(self):
            Override for the preloop before entering into the cmd

        postcmd(self, stop: bool, line: str) -> bool:
            Override for after the command is done but the user does not have control yet

        postloop(self) -> None:
            Override for after the cmd loop is exiting

        do_exit(self, line):
            Allows the user to exit the cmd loop

        do_help(self, line):
            Allows the user to call help

        help_config(self, line):
            Overrides configurations help command

        do_config(self, line):
            Allows the user to call the config command

        do_banner(self, line):
            Allows the user to clear the screen and recreate the banner
    """

    # region Init
    def __init__(
        self,
        selectedList: list,
        channelid=None,
        passedJson=None
    ):
        cmd.Cmd.__init__(self, completekey="tab", stdin=None, stdout=None)
        if selectedList != []:
            self.selectedList = selectedList
        else:
            self.selectedList = NightcapCLIPublisher().selectedList

        self.doc_header = Fore.GREEN + "Commands" + Style.RESET_ALL
        self.misc_header = Fore.GREEN + "System" + Style.RESET_ALL
        self.undoc_header = Fore.GREEN + "Other" + Style.RESET_ALL
        self.ruler = Fore.YELLOW + "-" + Style.RESET_ALL

        self.config = NightcapCLIConfiguration()
        
        self.printer = Printer()
        self.mongo_helper = NightcapMongoHelper(self.config)
        self.channelID = channelid
        self.prompt = self._prompt()
        
        # if passedJson != None:
        #     self.config.filename = passedJson['filename']
        #     self.config.isDir = passedJson['isDir']
        #     self.config.dir = passedJson['dir']
        #     self.config.project = passedJson['project']
        
    # endregion

    def addselected(self, item):
        NightcapCLIPublisher().selectedList.append(item)
        self.selectedList = NightcapCLIPublisher().selectedList

    def popselected(self):
        NightcapCLIPublisher().selectedList.pop(-1)
        self.selectedList = NightcapCLIPublisher().selectedList

    #region 
    def _prompt(self):
        _p = []
        for _ in self.selectedList:
            _p.append("[" + Fore.LIGHTYELLOW_EX + _ + Fore.LIGHTGREEN_EX + "]")
        _p = "".join(_p)
        return Fore.GREEN + "nightcap" + _p + " > " + Fore.CYAN
    #endregion

    # region CMD Overrides
    def emptyline(self):
        pass

    # putting into place to be used later
    def preloop(self) -> None:
        return super().preloop()

    def postcmd(self, stop: bool, line: str) -> bool:
        return super().postcmd(stop, line)

    def postloop(self) -> None:
        return super().postloop()

    # endregion
    #####

    # region Exit
    def do_exit(self, line):
        try:
            if self.channelID != None:
                self.printer.debug("Pop Before/After", self.channelID, currentMode=self.config.verbosity)
                self.printer.debug(NightcapCLIPublisher().channels, currentMode=self.config.verbosity)
                NightcapCLIPublisher().del_channel(self.channelID)
                self.popselected()
                self.printer.debug(NightcapCLIPublisher().channels, currentMode=self.config.verbosity)
            else:
                self.printer.debug("Pop Before/After (NO CHANNLE ID)", currentMode=self.config.verbosity)
                self.printer.debug(NightcapCLIPublisher().channels, currentMode=self.config.verbosity)
                self.popselected()
                self.printer.debug(NightcapCLIPublisher().channels, currentMode=self.config.verbosity)
                
        except Exception as e:
            pass
        return True
    # endregion

    # region Help
    def do_help(self, line):
        super(NightcapBaseCMD, self).do_help(line)

    # endregion

    # region Config
    def help_config(self):
        self.printer.help("Get the current system configuration(s)")

    def do_config(self, line):
        ScreenHelper().clearScr()
        self.printer.print_underlined_header_undecorated("Configuration")

        self.printer.print_underlined_header("Verbosity", leadingTab=2)
        self.printer.print_formatted_other(
            "Verbosity",
            "Normal" if self.config.verbosity == False else "Debug",
            leadingTab=3,
            optionalTextColor=Fore.LIGHTBLACK_EX
            if self.config.verbosity == False
            else Fore.LIGHTYELLOW_EX,
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

    # endregion

    # region Banner
    def do_banner(self, line):
        ScreenHelper().clearScr()
        NightcapBanner().Banner()

    # endregion
