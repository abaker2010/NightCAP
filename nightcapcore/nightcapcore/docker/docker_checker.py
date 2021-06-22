# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Imports
import time
from colorama import Fore, Style
from subprocess import Popen, PIPE, STDOUT
import docker as dDocker
import os

from nightcapcore.printers.print import Printer

DEVNULL = open(os.devnull, "wb")
# endregion


class NightcapCoreDockerChecker(object):
    """

    This class is used to help validate user input to the console

    ...

    Attributes
    ----------
        mongo_im_exists: -> bool
            Checks to see if the mongo image exists

        ncs_exits: -> bool
            Checks to see if the nightcapsite image exists

    Methods
    -------
        Accessible
        -------
            pull_image(self, image: str): -> None
                pulls the docker image passed

        None Accessible
        -------
            __check_image(self, image: str, tag: str, grep: str): -> bool
                returns a boolean depending on if the image exists or not

            _check_setup(self): -> bool
                returns a boolean depending on if the image has been pulled from the Docker images
    """

    # region Init
    def __init__(self) -> None:
        super().__init__()
        self.printer = Printer()
        self.docker = dDocker.from_env()

        self.mongo_im_exists = self.__check_image("mongo", "latest", "mongo")
        self.ncs_exits = self.__check_image("nightcapsite", "latest", "nightcapsite")

    # endregion

    # region Check Image
    def __check_image(self, image: str, tag: str, grep: str):
        try:
            return self.docker.images.get(image + ":" + tag)
        except Exception as e:
            return False

    # endregion

    # region Check Set-up
    def _check_setup(self):
        if self.mongo_im_exists == False:
            print("install mongo")

    # endregion

    # region Pull Image
    def pull_image(self, image: str) -> None:
        # self.printer.item_1("Please wait while pulling Image", image)
        # self.printer.print_underlined_header("Progress for downloading Mongo Image")
        try:
            # self.printer.print_formatted_additional("Pulling image", optionaltext=image)
            self.docker.images.pull(image)
            # self.printer.print_formatted_check("Done", leadingTab=3)
        except Exception as e:
            self.printer.print_error(Exception("Error pulling image: " + image))
            raise e

    # endregion
