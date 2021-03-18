#!/usr/bin/env python3.8
# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
#region imports
import sys
import colorama 
from colorama import Fore, Style
from nightcapcore import ScreenHelper, Printer, NightcapCLIConfiguration, NightcapBanner
from nightcappackages.classes.databases.mogo.checker import MongoDatabaseChecker
from nightcapserver.server.server import NighcapCoreSimpleServer
from pymongo.errors import ServerSelectionTimeoutError
from application.nightcap import Nightcap
from application.legal.legal import Legal

try:
    import readline
    if 'libedit' in readline.__doc__:
        readline.parse_and_bind("bind ^I rl_complete")
    else:
        readline.parse_and_bind("tab: complete")
except ImportError:
    sys.stdout.write("No readline module found, no tab completion available.\n")
else:
    import rlcompleter
#endregion


class Entry:
    def __init__(self):
        self.conf = NightcapCLIConfiguration()
        self.printer = Printer()
        self.yes = self.conf.currentConfig.get('NIGHTCAPCORE', 'yes').split()
        self.mongo_server = None

    def agreements(self):
        """Legal agreement the at the user must accept to use the program"""
        
        while not self.conf.currentConfig.getboolean("NIGHTCAPCORE", "agreement"):
            ScreenHelper().clearScr()
            NightcapBanner(self.conf).Banner()
            Legal().termsAndConditions()
            agree = input(Fore.LIGHTGREEN_EX + "\t\tYou must agree to our terms and conditions first (Y/n): " + Style.RESET_ALL).lower()

            if agree in self.yes:
                self.conf.currentConfig.set('NIGHTCAPCORE', 'agreement', 'true')
                self.conf.Save()
                ScreenHelper().clearScr()
                self.banner()

        return True

    def banner(self):
        NightcapBanner(self.conf).Banner()

    def checkmongodb(self):
        try:
            self.printer.print_formatted_additional(text="Please wait while connecting to Mongo Server...")
            self.mongo_server = MongoDatabaseChecker()
            return True
        except ServerSelectionTimeoutError as e:
            raise e

    def change_mongo_server(self, ip: str = None, port: str = None):
        self.printer.print_underlined_header_undecorated(text="Current Mongo Settings")
        self.printer.print_formatted_additional(text="IP", optionaltext=self.conf.currentConfig["MONGOSERVER"]["ip"])
        self.printer.print_formatted_additional(text="Port", optionaltext=self.conf.currentConfig["MONGOSERVER"]["port"], endingBreaks=1)
        agree = input(Fore.LIGHTGREEN_EX + "\t\tError connecting to mongo server would you like to change the IP/Port (Y/N/R): " + Style.RESET_ALL).lower()
        if agree in self.yes:
            _ip = input(Fore.LIGHTGREEN_EX + "\t\tNew IP Address: " + Style.RESET_ALL).lower()
            _port = input(Fore.LIGHTGREEN_EX + "\t\tNew Port: " + Style.RESET_ALL).lower()
            try:
                self.conf.currentConfig.set('MONGOSERVER', 'ip', str(_ip))
                self.conf.currentConfig.set('MONGOSERVER', 'port', str(_port))
                self.conf.Save()
            except Exception as e:
                raise e
            return True
        elif "r" == agree.lower():
            main()
        else:
            raise Exception("User terminated server change")

    def check_mongo_dbs(self):
        _db_exits = self.mongo_server.check_database()
        if(_db_exits):
            self.printer.print_formatted_check(text="Mongo Server initialize", optionaltext="Yes")
            return _db_exits
        else:
            self.printer.print_formatted_additional(text="Mongo Server initialize", optionaltext="No")
            agree = input(Fore.LIGHTGREEN_EX + "\n\t\tWould you like to initialize the Mongo Server (Y/N): " + Style.RESET_ALL).lower()
            if agree in self.yes:
                print("Init for mongo db needs to go here")
                self.mongo_server.initialize_database()
                main()
            else:
                raise KeyboardInterrupt()

        

def main():
    _printer = Printer()
    _entry = Entry()
    try:
        colorama.init()
        
        _entry.banner()

        if(_entry.agreements()):
            try:
                if(_entry.checkmongodb()):
                    _printer.print_formatted_check(text="Mongo Server", optionaltext="Connected")
                    if(_entry.check_mongo_dbs()):
                        ScreenHelper().clearScr()
                        _entry.banner()
                        Nightcap(_entry.conf).cmdloop()
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
            if(_entry.change_mongo_server()):
                ScreenHelper().clearScr()
                main()
        except Exception as e:
            _printer.print_error(exception=e)
    except Exception as e:
        _printer.print_error(exception=e)
    finally:
        _printer.print_underlined_header(text="Cleaning up...")
        try:
            NighcapCoreSimpleServer(_entry.conf).shutdown()
        except Exception as e:
            _printer.print_error(exception=e)
        exit()
#region Main named if for keyboard interrupt
if __name__ == '__main__':
    main()
#endregion