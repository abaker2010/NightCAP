# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Imports
import os
import sys
from docker.errors import DockerException
from colorama.ansi import Fore, Style
from nc_docker.docker_helper import NightcapDockerHelper
from nightcapcore.configuration import NightcapCLIConfiguration
from nightcapcore.docker.docker_checker import NightcapCoreDockerChecker
from nightcapcore.helpers.screen.screen_helper import ScreenHelper
from nightcapcore.printers.print import Printer
from nightcappackages.classes.databases.mogo.checker.mongo_database_checker import MongoDatabaseChecker
from pymongo.errors import ServerSelectionTimeoutError
# endregion


class NightcapMongoHelper:
    """

    This class is used to as a helper for MongoDB

    ...

    Attributes
    ----------
        printer: -> Printer
            allows us to print from the command line

        conf: -> NightcapCLIConfiguration
            allows us to have access to the main configuration

        yes: -> list
            list of yes 'words'

        docker_helper: -> NightcapDockerHelper
            allows us to talk to the MongoDB Docker Container

        mongo_server: -> MongoDatabaseChecker
            allows us to check the status of the Docker Container

    Methods
    -------
        Accessible
        -------
            check_mongo_container(self): -> bool
                checks to see if the Mongo container is running

            check_mongo_dbs(self): -> None
                prints the status

            change_mongo_server(self, ip: str = None, port: str = None): -> None
                Allows us to change the mongo server configurations

        None Accessible
        -------
            _change_mogo_settings(self, agree): -> bool
                changes the mongo settings
    """

    # region Init
    def __init__(self, conf: NightcapCLIConfiguration) -> None:
        super().__init__()
        self.printer = Printer()
        self.conf = conf
        self.yes = self.conf.config.get("NIGHTCAPCORE", "yes").split()
        try:
            self.docker_helper = NightcapDockerHelper(self.conf)
        except DockerException as de:
            self.printer.print_error(Exception("Error: Docker needs to be running locally"))
            exit()
        except Exception as e:
            self.printer.print_error(e)
            
        try:
            self.mongo_server = MongoDatabaseChecker()
        except Exception as e:
            self.mongo_server = None

    # endregion

    # region Check Mongo Container
    def check_mongo_container(self):
        try:
            self.printer.print_formatted_additional(
                text="Please wait while connecting to Mongo Server..."
            )
            # self.mongo_server = MongoDatabaseChecker()
            if self.docker_helper.mongo_continer_exists() == True:
                self.docker_helper.start_mongodb()
                return True
            return False
            # return True if self.docker_helper.get_mongo_container_status() == "running" else False
        except ServerSelectionTimeoutError as e:
            raise e

    # endregion

    # region Check Mongo DB Status
    def check_mongo_dbs(self):
        _db_exits = MongoDatabaseChecker().check_database()
        if _db_exits:
            self.printer.print_formatted_check(
                text="Mongo Server initialize", optionaltext="Yes"
            )
            return _db_exits
        else:
            self.printer.print_formatted_additional(
                text="Mongo Server initialize", optionaltext="No"
            )
            agree = self.printer.input(
                + "\n\t\tWould you like to initialize the Mongo Server (Y/N): "
            ).lower()
            if agree in self.yes:
                self.mongo_server.initialize_database()
                self.printer.print_formatted_additional(text="Rebooting...")
                os.execv(sys.argv[0], sys.argv)
            else:
                raise KeyboardInterrupt()

    # endregion

    # region Change Mongo Server
    def change_mongo_server(self, ip: str = None, port: str = None):
        self.printer.print_underlined_header("Current Mongo Settings")
        self.printer.print_formatted_additional(
            text="IP", optionaltext=self.conf.config["MONGOSERVER"]["ip"]
        )
        self.printer.print_formatted_additional(
            text="Port",
            optionaltext=self.conf.config["MONGOSERVER"]["port"],
            endingBreaks=1,
        )
        if "127.0.0.1" or "localhost" in self.conf.config["MONGOSERVER"]["ip"]:
            _docker_checker = NightcapCoreDockerChecker()
            # print("Docker image (Mongo) exists:", _docker_checker.mongo_im_exists)
            # print("Docker image (Django) exists:", _docker_checker.ncs_exits)
            self.docker_helper.get_container_status_by_name("")
            self.printer.print_underlined_header("Docker Images")
            self.printer.print_underlined_header_undecorated("MongoDB", leadingTab=2)
            if _docker_checker.mongo_im_exists == False:
                self.printer.print_formatted_delete(
                    text="Container Status",
                    optionaltext=self.docker_helper.get_mongo_container_status(),
                    leadingTab=3,
                )
                self.printer.print_formatted_delete(
                    text="Mongo", optionaltext="Missing", leadingTab=3, endingBreaks=1
                )
            else:
                self.printer.print_formatted_check(
                    text="Container Status",
                    optionaltext=self.docker_helper.get_mongo_container_status(),
                    leadingTab=3,
                    textColor=Fore.CYAN,
                )
                self.printer.print_formatted_additional(
                    text="Mongo Image",
                    optionaltext="Exists",
                    leadingTab=3,
                    optionalTextColor=Fore.RED,
                    endingBreaks=1,
                )
            # region Working Code (Commenting out for now due to time limitations for the feature)
            self.printer.print_underlined_header_undecorated(
                "Nighcapsite", leadingTab=2
            )
            if _docker_checker.ncs_exits == False:
                self.printer.print_formatted_delete(
                    text="Container Status",
                    optionaltext=self.docker_helper.get_site_container_status(),
                    leadingTab=3,
                )
                self.printer.print_formatted_delete(
                    text="Nightcapsite",
                    optionaltext="Missing",
                    leadingTab=3,
                    endingBreaks=1,
                )
            else:
                self.printer.print_formatted_check(
                    text="Container Status",
                    optionaltext=self.docker_helper.get_site_container_status(),
                    leadingTab=3,
                    textColor=Fore.CYAN,
                )
                self.printer.print_formatted_additional(
                    text="Nightcapsite",
                    optionaltext="Exists",
                    leadingTab=3,
                    optionalTextColor=Fore.RED,
                    endingBreaks=1,
                )
            # endregion
            
            self.printer.print_underlined_header("Error connecting to mongo server")
            self.printer.print_formatted_additional(
                text="Initialize",
                optionaltext="I",
                leadingTab=2,
                optionalTextColor=Fore.MAGENTA,
            )
            self.printer.print_formatted_additional(
                text="(Re)Start",
                optionaltext="R | S",
                leadingTab=2,
                optionalTextColor=Fore.MAGENTA,
            )
            self.printer.print_formatted_additional(
                text="Change",
                optionaltext="C",
                leadingTab=2,
                optionalTextColor=Fore.MAGENTA,
                endingBreaks=1,
            )

            _selection = input(
                Fore.LIGHTGREEN_EX + "\t\tOption: " + Style.RESET_ALL
            ).lower()

            if _selection.strip().lower() == "c":
                yes = self.printer.input(
                    Fore.YELLOW
                    + "\t\tAre you sure you want to change the settings (Y/n): "
                    + Style.RESET_ALL
                ).lower()
                self._change_mogo_settings(yes)
                ScreenHelper().clearScr()
                self.printer.print_formatted_additional(text="Rebooting...")
                os.execv(sys.argv[0], sys.argv)
            elif _selection.strip().lower() == "i":
                yes = self.printer.input(
                    Fore.YELLOW
                    + "\t\tAre you sure you want to initialize containers (Y/n): "
                    + Style.RESET_ALL
                ).lower()
                ScreenHelper().clearScr()
                if yes in self.yes:
                    self.printer.print_underlined_header_undecorated("Setting Up Environment", leadingTab=0)
                    _init = self.docker_helper.init_containers(_docker_checker)
                    if _init == True:
                    #     self.printer.print_underlined_header("Preparing Docker Images")
                    #     self.docker_helper.prepare_containers()
                        print()
                        self.printer.print_formatted_check("Set Up Done", leadingTab=1, endingBreaks=1)
                        self.printer.print_formatted_additional(text="Rebooting...")
                        os.execv(sys.argv[0], sys.argv)
            elif _selection.strip().lower() == "s":
                yes = self.printer.input(
                    Fore.YELLOW
                    + "\t\tAre you sure you want to start containers (Y/n): "
                    + Style.RESET_ALL
                ).lower()
                if yes in self.yes:
                    self.docker_helper.prepare_containers()
                    self.printer.print_formatted_additional(text="Rebooting...")
                    os.execv(sys.argv[0], sys.argv)
            elif "r" == _selection.strip().lower().lower():
                # self.printer.print_formatted_additional(text='Rebooting...')
                self.docker_helper.stop_mongodb()
                self.docker_helper.start_mongodb()
                os.execv(sys.argv[0], sys.argv)
            else:
                ScreenHelper().clearScr()
                self.change_mongo_server()

        else:
            agree = input(
                Fore.LIGHTGREEN_EX
                + "\t\tError connecting to mongo server would you like to change the IP/Port (Y/N/R): "
                + Style.RESET_ALL
            ).lower()
            self._change_mogo_settings(agree)

    # endregion

    # region Change Mongo Settings
    def _change_mogo_settings(self, agree):
        if agree in self.yes:
            ScreenHelper().clearScr()
            self.printer.print_underlined_header("Changing IP Address")
            _ip = input(
                Fore.LIGHTGREEN_EX + "\t\tNew IP Address: " + Style.RESET_ALL
            ).lower()
            _port = input(
                Fore.LIGHTGREEN_EX + "\t\tNew Port: " + Style.RESET_ALL
            ).lower()
            try:
                self.conf.config.set("MONGOSERVER", "ip", str(_ip))
                self.conf.config.set("MONGOSERVER", "port", str(_port))
                self.conf.Save()
            except Exception as e:
                raise e
            return True

        return False

    # endregion
