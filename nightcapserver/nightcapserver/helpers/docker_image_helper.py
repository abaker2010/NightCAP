# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Imports
from nightcapserver.helpers.docker_status import NightcapDockerStatus
from pathlib import Path
import subprocess
from subprocess import Popen, PIPE, STDOUT
import time
import os
import re
import getpass
import docker as dDocker
from colorama.ansi import Fore
from nightcapcore.configuration import NightcapCLIConfiguration
from nightcapcore.docker.docker_checker import NightcapCoreDockerChecker
from nightcapcore.helpers.screen.screen_helper import ScreenHelper
from nightcapcore.printers.print import Printer
from nightcappackages.classes.paths import (
    NightcapPackagesPathsEnum,
    NightcapPackagesPaths,
)
from nightcappackages.classes.helpers import NightcapRestoreHelper
from abc import ABC, abstractmethod

DEVNULL = open(os.devnull, "wb")
# endregion


class NightcapDockerImageHelper(ABC):

    # region Init
    def __init__(self, name: str, tag: str) -> None:
        self.name = name
        self.tag = tag
        self.printer = Printer()
        self.docker = dDocker.from_env()
        # try:
        #     # return self.docker.images.get(image+":"+tag)
        #     self.image = self.docker.images.get(name+":"+tag)
        # except Exception as e:
        #     # if not self.suppress:
        #         # self.printer.print_error(Exception("Image Does Not Exist"))
        #     self.image = None

    # endregion

    def image_exists(self) -> NightcapDockerStatus:
        try:
            return (
                NightcapDockerStatus.MISSING
                if self.docker.images.get(self.name + ":" + self.tag) == None
                else NightcapDockerStatus.EXISTS
            )
        except Exception as e:
            return NightcapDockerStatus.MISSING

    @abstractmethod
    def init_image(self) -> bool:
        raise NotImplementedError
