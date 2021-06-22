# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Import
from nightcapcore.configuration.configuration import NightcapCLIConfiguration
from nightcapcore import ScreenHelper, Printer
from colorama import Fore
import os
from colorama.ansi import Fore
from nightcapcore.helpers.screen.screen_helper import ScreenHelper
from nightcapcore.printers.print import Printer

DEVNULL = open(os.devnull, "wb")
# endregion


class NightcapDockRescueConfigHelper:
    def __init__(self, conf: NightcapCLIConfiguration) -> None:
        self.printer = Printer()
        self.conf = conf

    # region Is IP Valid
    def _isvalidIPAddress(self, IP: str) -> bool:
        """
        :type IP: str
        :rtype: str
        """

        def isIPv4(s):
            try:
                return str(int(s)) == s and 0 <= int(s) <= 255
            except:
                return False

        def isIPv6(s):
            if len(s) > 4:
                return False
            try:
                return int(s, 16) >= 0 and s[0] != "-"
            except:
                return False

        if IP.count(".") == 3 and all(isIPv4(i) for i in IP.split(".")):
            return True
        if IP.count(":") == 7 and all(isIPv6(i) for i in IP.split(":")):
            return True
        return False

    # endregion

    def change_connection_only(self):
        ScreenHelper().clearScr()
        self.printer.print_underlined_header("Change Docker Base Config")
        _ip = input(
            Fore.LIGHTGREEN_EX + str("\n\tNew IP Addrress: %s" % (Fore.LIGHTCYAN_EX))
        )
        _port = input(Fore.LIGHTGREEN_EX + str("\tNew Port: %s" % (Fore.LIGHTCYAN_EX)))
        ScreenHelper().clearScr()
        self.printer.print_header("Reconfig Info")
        self.printer.print_formatted_additional("IP", _ip)
        self.printer.print_formatted_additional("Port", _port)

        _ready = self.printer.input("Confirm? (Y/n)", defaultReturn=True)

        if _ready:
            print("Change IP")

            try:
                self.network = "MONGOSERVER"
                if str(_ip).lower() == "localhost":
                    self.conf.config.set(self.network, "ip", "127.0.0.1")
                    self.conf.Save()
                elif self._isvalidIPAddress(_ip):
                    self.conf.config.set(self.network, "ip", _ip)
                    self.conf.Save()
                else:
                    self.printer.print_error(
                        Exception(
                            "Error with setting IP Address { %s }, please try again"
                            % _ip
                        )
                    )

                try:
                    port = int(_port)
                    if 1 <= port <= 65535:
                        self.conf.config.set(self.network, "port", _port)
                        self.conf.Save()
                    else:
                        raise ValueError
                except ValueError:
                    self.printer.print_error(
                        Exception(
                            "Error with setting Port { %s }. Expected range 1 - 65535, please try again"
                            % _port
                        )
                    )
            except Exception as e:
                self.printer.print_error(e)

            return True
        else:
            return False
