# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Imports
import os
import docker as dDocker
from nightcappackages.classes.commands.updater import NightcapPackageUpdaterCommand
from nightcapcore.invoker.invoker import Invoker
from nightcapcore import (
    ScreenHelper,
    Printer,
    NightcapCLIConfiguration,
    NightcapBanner,
    Legal,
)
from nightcapserver.commands.mongo_setup import NightcapServerMongoSetup
from nightcapserver.helpers.mongo_helper import NightcapMongoDockerHelper
from nightcapserver.helpers.docker_status import NightcapDockerStatus
from colorama import Style, Fore
from nightcapcore.configuration import NightcapCLIConfiguration
from nightcapcore.helpers.screen.screen_helper import ScreenHelper
from nightcapcore.printers.print import Printer
from pymongo.errors import ServerSelectionTimeoutError

DEVNULL = open(os.devnull, "wb")
# endregion


class NightcapDockerConfigurationHelper:

    # region Init
    def __init__(self, config: NightcapCLIConfiguration) -> None:
        super().__init__()
        self.conf = config
        self.printer = Printer()
        self.docker = dDocker.from_env()
        self.mongo_helper = NightcapMongoDockerHelper()
        # self.django_helper = NightcapDjangoDockerHelper()

    # endregion

    def check_legal(self):
        """Legal agreement the at the user must accept to use the program"""
        while not self.conf.config.getboolean("NIGHTCAPCORE", "agreement"):
            ScreenHelper().clearScr()
            NightcapBanner().Banner()
            Legal().termsAndConditions()
            agree = self.printer.input(
                "You must agree to our terms and conditions first (y/N)"
            )

            if agree:
                self.conf.config.set("NIGHTCAPCORE", "agreement", True)
                self.conf.Save()
                ScreenHelper().clearScr()
                return True
        return True

    # def env_check(self):
    #     try:
    #         if (
    #             self.mongo_helper.image_exists() == NightcapDockerStatus.EXISTS
    #             and self.mongo_helper.container_status() == NightcapDockerStatus.RUNNING
    #         ):
    #             _mongo = (NightcapDockerStatus.EXISTS, NightcapDockerStatus.RUNNING)
    #         else:
    #             _mongo = (
    #                 self.mongo_helper.image_exists(),
    #                 self.mongo_helper.container_status(),
    #             )

    #         # if self.django_helper.image_exists() ==  NightcapDockerStatus.EXISTS and self.django_helper.container_status() !=  NightcapDockerStatus.MISSING:
    #         #     _django = (NightcapDockerStatus.EXISTS, NightcapDockerStatus.EXISTS)
    #         # else:
    #         #     _django = (self.django_helper.image_exists(), self.django_helper.container_status())
    #         return (_mongo, (NightcapDockerStatus.EXISTS, NightcapDockerStatus.EXISTS))

    #     except ServerSelectionTimeoutError as e:
    #         self.printer.print_error(e)
    #         raise e
    #     except Exception as e:
    #         self.printer.print_error(e)
    #         raise e

    def change_configuration(self):
        self.printer.print_underlined_header("Current Network Settings")
        self.printer.print_formatted_additional(
            text="IP", optionaltext=self.conf.config["MONGOSERVER"]["ip"]
        )
        self.printer.print_formatted_additional(
            text="Port",
            optionaltext=self.conf.config["MONGOSERVER"]["port"],
            endingBreaks=1,
        )

        self.printer.print_underlined_header("Current Docker Data")
        self.printer.print_formatted_additional(
            "Note", "Mongo required to be running to start"
        )
        self.printer.print_underlined_header_undecorated("MongoDB", leadingTab=2)

        self.printer.item_2(
            text="Image",
            optionalText=str(self.mongo_helper.image_exists().value).capitalize(),
            leadingTab=3,
        )
        self.printer.item_2(
            text="Container",
            optionalText=str(self.mongo_helper.container_status().value).capitalize(),
            leadingTab=3,
            endingBreaks=1,
        )

        # self.printer.print_underlined_header_undecorated(
        #     "Nighcapsite", leadingTab=2
        # )

        # self.printer.item_2(
        #     text="Image", optionalText=str(self.django_helper.image_exists().value).capitalize(), leadingTab=3
        # )
        # self.printer.item_2(
        #     text="Container",
        #     optionalText=str(
        #         self.django_helper.container_status().value).capitalize(),
        #     leadingTab=3,
        # )

        self.printer.print_underlined_header("Please Select an option")
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
            text="Change Settings",
            optionaltext="CS",
            leadingTab=2,
            optionalTextColor=Fore.MAGENTA,
        )
        self.printer.print_formatted_additional(
            text="Connect",
            optionaltext="C",
            leadingTab=2,
            optionalTextColor=Fore.MAGENTA,
        )
        self.printer.print_formatted_additional(
            text="Exit",
            optionaltext="E",
            leadingTab=2,
            optionalTextColor=Fore.MAGENTA,
            endingBreaks=1,
        )

        _selection = self.printer.input_return_only(
            "Choice: ", defaultReturn="", leadingBreaks=2
        )

        if _selection != "":
            if _selection.strip().lower() == "i":
                # ScreenHelper().clearScr()
                # self.printer.print_underlined_header("Setting Up Environment")
                # self.printer.print_underlined_header("Checking Images")
                # _mongo_image_ready = self.mongo_helper.init_image()
                
                ScreenHelper().clearScr()
                self.printer.print_underlined_header("Setting Up Environment", leadingBreaks=1, endingBreaks=1)
                try:
                    mongo_setup_invoker = Invoker()
                    mongo_setup_invoker.set_on_start(NightcapServerMongoSetup(self.mongo_helper, self.conf))

                    if mongo_setup_invoker.execute():
                        
                        return True
                    # if self.mongo_helper.init_image():
                    #     print("Mongo image exists create container")
                    #     try:
                    #         if self.mongo_helper.init_container():
                    #             if self.mongo_helper.container_start():
                    #                 print("mongo ready done")
                    #                 print(
                    #                     "Mongo Status: %s"
                    #                     % (self.mongo_helper.container_status())
                    #                 )
                    #                 invoker = Invoker()
                    #                 invoker.set_on_start(
                    #                     NightcapPackageUpdaterCommand(
                    #                         self.conf, True, force=True
                    #                     )
                    #                 )
                    #                 invoker.execute()
                    #                 return True
                    #     except Exception as ce:
                    #         raise ce
                    # if self.mongo_helper.init_image():
                    #     print("Mongo Init done")

                    # else:
                    #     raise Exception("Error with Mongo Init")
                    # if _mongo_image_ready:
                    #     if self.mongo_helper.init_container():
                    #         if self.mongo_helper.container_start():
                    #             invoker = Invoker()
                    #             invoker.set_on_start(NightcapPackageUpdaterCommand(self.conf, True, force=True))
                    #             invoker.execute()

                    #         return True
                except Exception as e:
                    self.printer.print_error(e)
                    return False
                # _django_image_ready = self.django_helper.init_image()

                # if _mongo_image_ready and _django_image_ready:

                #     self.printer.print_underlined_header("Checking Containers")
                #     _mongo_container_ready = self.mongo_helper.init_container()
                #     _django_container_ready = self.django_helper.init_container()
                #     if _mongo_container_ready and _django_container_ready:
                #         _mstatus = self.mongo_helper.container_start()
                #         _dstatus = self.django_helper.container_start()

                #         invoker = Invoker()
                #         self.django_helper.set_account()

                #         invoker.set_on_start(NightcapPackageUpdaterCommand(self.conf, True, force=True))
                #         invoker.execute()

                #         return True
                #     else:
                #         self.printer.print_error(Exception("Error Creating Containers"))
            # else:
            #     self.printer.print_error(Exception("Error Pullimg/Creating Images"))

            elif _selection.strip().lower() == "cs":
                print("Change Settings")
                self._change_mogo_settings()
                self.change_configuration()
            elif _selection.strip().lower() == "c":
                print(self.mongo_helper.container_status())

                if self.mongo_helper.container_status() != NightcapDockerStatus.RUNNING:
                    self.printer.print_error(
                        Exception("Mongo container needs to be running")
                    )
                    self.change_configuration()
                else:
                    print("Trying to launch")
                    return True
            elif _selection.strip().lower() == "s":

                _selection2 = self.printer.input_return_only(
                    "Would you like to start both containers? (M/E)"
                )

                # if str(_selection2).lower() == "b":
                #     _mstatus = self.mongo_helper.container_start()
                #     _dstatus = self.django_helper.container_start()
                if str(_selection2).lower() == "m":
                    _mstatus = self.mongo_helper.container_start()
                # if str(_selection2).lower() == "d":
                #     _dstatus = self.django_helper.container_start()
                if str(_selection2).lower() == "e":
                    pass

                ScreenHelper().clearScr()
                self.change_configuration()

            elif _selection.strip().lower() == "r":
                _mstatus = self.mongo_helper.continer_restart()
                _dstatus = self.django_helper.continer_restart()

                if _dstatus == None or _mstatus == None:
                    ScreenHelper().clearScr()
                    self.printer.print_error(
                        Exception("Could not restart container. Some are missing.")
                    )
                    self.change_configuration()
            elif _selection.strip().lower() == "e":
                ScreenHelper().clearScr()
                raise KeyboardInterrupt()
            else:
                ScreenHelper().clearScr()
                self.printer.print_error(
                    Exception("Selection not allowed. Please try again.")
                )
                self.change_configuration()
        else:
            ScreenHelper().clearScr()
            self.printer.print_error(
                Exception("Selection not allowed. Please try again.")
            )
            self.change_configuration()

        return True

    def _change_mogo_settings(self):
        ScreenHelper().clearScr()
        try:
            self.printer.print_underlined_header("Changing Mongo Config")
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
                self.printer.print_error(e)
                return False
            return True
        except KeyboardInterrupt as e:
            ScreenHelper().clearScr()
            self.printer.print_error(Exception("User terminated configuration"))
            return False
