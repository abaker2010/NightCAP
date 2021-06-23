# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Imports
from nightcapcore.command.command import Command
from colorama import Fore
from nightcapcore import Printer
from nightcapcore.configuration.configuration import NightcapCLIConfiguration
from nightcapcore.invoker.invoker import Invoker
from nightcappackages.classes.commands.updater import NightcapPackageUpdaterCommand
from nightcapserver.helpers.mongo_helper import NightcapMongoDockerHelper
import requests
import os
from nightcappackages import *

# endregion


class NightcapServerMongoSetup(Command):

    def __init__(self, mongo_helper: NightcapMongoDockerHelper, conf: NightcapCLIConfiguration) -> None:
        super().__init__()
        self.printer = Printer()
        self.mongo_helper = mongo_helper
        self.conf = conf

    def execute(self) -> None:
        try:
        
            if self.mongo_helper.init_image(): 
                # self.printer.item_1("Mongo Image ", _image_init)

                # self.printer.print_formatted_additional("Init for container")
                if self.mongo_helper.init_container():
                    # self.printer.print_formatted_additional("Container Done", leadingTab=3)
                    self.mongo_helper.container_start()
                    self.printer.print_formatted_additional("Started Container", leadingTab=3)
                    if self.printer.input("Would you like to install base packages? (Y/n)", defaultReturn=True):
                        # print("Install updates")
                        # print(
                        #     "Mongo Status: %s"
                        #     % (self.mongo_helper.container_status())
                        # )
                        invoker = Invoker()
                        invoker.set_on_start(
                            NightcapPackageUpdaterCommand(
                                self.conf, True, force=True
                            )
                        )
                        invoker.execute()
                else:
                    self.printer.print_formatted_additional("Container Error", leadingTab=3)
                    raise Exception("Error with getting Mongo Init")

                return True
            else:

                raise Exception("Error with getting Mongo Image")
        except Exception as e:
            raise e

        
