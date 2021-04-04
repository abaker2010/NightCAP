#!/usr/bin/env python3.8
# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
#region Imports
import os
import sys
import colorama
from colorama import Fore, Style
from mongo.mongo_helper import NightcapMongoHelper
from nightcapcli.observer.publisher import NightcapCLIPublisher
from nightcapcore import ScreenHelper, Printer, NightcapCLIConfiguration, NightcapBanner
from nightcapserver.server.server import NighcapCoreSimpleServer
from pymongo.errors import ServerSelectionTimeoutError
from application.nightcap import Nightcap
from application.legal.legal import Legal
from subprocess import Popen, PIPE, STDOUT

DEVNULL = open(os.devnull, "wb")
try:
    import readline
    if "libedit" in readline.__doc__:
        readline.parse_and_bind("bind ^I rl_complete")
    else:
        readline.parse_and_bind("tab: complete")
except ImportError:
    sys.stdout.write("No readline module found, no tab completion available.\n")
else:
    import rlcompleter
#endregion

#region Entry
class Entry:
    """
        
        This class is used to as a wrapper for the entry process to the program

        ...

        Attributes
        ----------

            conf: -> NightcapCLIConfiguration
                this allows us to use the main configuration of the program

            printer: -> Printer
                allows us to print to the command line

            yes: -> list
                used to check against for the user agreements

            mongo_server = None

            mongo_helper: -> NightcapMongoHelper
                helps us to interact witht the MongoDB Container

        Methods 
        -------
            Accessible 
            -------
                agreements(self): -> bool
                    asks the user to agree to the terms of usage and conduct

                banner(self): -> None
                    easier to access banner

    """
    #region Init
    def __init__(self):
        self.conf = NightcapCLIConfiguration()
        self.printer = Printer()
        self.yes = self.conf.config.get("NIGHTCAPCORE", "yes").split()
        # self.mongo_server = None
        self.mongo_helper = NightcapMongoHelper(self.conf)
    #endregion

    #region Agreements
    def agreements(self):
        """Legal agreement the at the user must accept to use the program"""
        while not self.conf.config.getboolean("NIGHTCAPCORE", "agreement"):
            ScreenHelper().clearScr()
            NightcapBanner().Banner()
            Legal().termsAndConditions()
            agree = input(
                Fore.LIGHTGREEN_EX
                + "\t\tYou must agree to our terms and conditions first (Y/n): "
                + Style.RESET_ALL
            ).lower()

            if agree in self.yes:
                self.conf.config.set("NIGHTCAPCORE", "agreement", "true")
                self.conf.Save()
                ScreenHelper().clearScr()
                self.banner()

        return True
    #endregion

    #region Banner
    def banner(self):
        NightcapBanner().Banner()
    #endregion
#endregion

#region Main
def main():
    """
        
        This class is used as the main entry to the program

    """
    _printer = Printer()
    _entry = Entry()
    try:
        colorama.init()
        if _entry.agreements():
            try:
                if _entry.mongo_helper.check_mongo_container():
                    _printer.print_formatted_check(
                        text="Mongo Server", optionaltext="Connected"
                    )
                    ScreenHelper().clearScr()
                    # _entry.banner()
                    # _channel = NightcapCLIPublisher().new_channel()
                    _who = Nightcap([], "basecli")
                    NightcapCLIPublisher().register("basecli", _who)

                    # print(NightcapCLIPublisher().channels)
                    l = _who.precmd("banner")
                    r = _who.onecmd(l)
                    r = _who.postcmd(r, l)
                    if not r:
                        _who.cmdloop()

                else:
                    try:
                        ScreenHelper().clearScr()
                        _entry.banner()
                        if _entry.mongo_helper.change_mongo_server():
                            ScreenHelper().clearScr()
                            main()
                    except Exception as e:
                        _printer.print_error(e)
            except ServerSelectionTimeoutError as e:
                raise e

    except KeyboardInterrupt:
        ScreenHelper().clearScr()
        _entry.banner()
        _printer.print_formatted_delete(text="Forced Termination!! ")
        exit()
    except ServerSelectionTimeoutError as e:
        try:
            ScreenHelper().clearScr()
            _entry.banner()
            if _entry.mongo_helper.change_mongo_server():
                ScreenHelper().clearScr()
                main()
        except Exception as e:
            _printer.print_error(e)
    except Exception as e:
        _printer.print_error(e)
    finally:
        _printer.print_underlined_header("Cleaning up...")
        try:
            NighcapCoreSimpleServer(_entry.conf).shutdown()
            _entry.mongo_helper.docker_helper.stop_all_containers()
        except Exception as e:
            _printer.print_error(e)
        exit()
#endregion

# region __NAME__ 
if __name__ == "__main__":
    main()
#endregion
