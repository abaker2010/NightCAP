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


class NightcapDockerContainerHelper(ABC):

    # region Init
    def __init__(self, name: str) -> None:
        self.cname = name
        self.printer = Printer()
        self.docker = dDocker.from_env()
        try:
            self.continer = self.docker.containers.get(self.cname)
        except:
            self.continer = None

    # endregion

    def container_start(self) -> str:
        try:
            _container = self.docker.containers.get(self.cname)
            if _container != None:
                
                _container.start()
                while self.docker.containers.get(self.cname).attrs["State"]["Status"] != 'running':
                    print("waiting: ", self.docker.containers.get(self.cname).attrs["State"]["Status"])

                return self.docker.containers.get(self.cname).attrs["State"]["Status"]
        except Exception as e:
            self.printer.print_error(
                Exception("Container %s Does Not Exist" % self.cname)
            )

    def continer_stop(self) -> str:
        try:
            _container = self.docker.containers.get(self.cname)
            if _container != None:
                _container.stop()
                return _container.attrs["State"]["Status"]
        except Exception as e:
            self.printer.print_error(
                Exception("Container %s Does Not Exist" % self.cname)
            )

    def continer_restart(self) -> str:
        try:
            _container = self.docker.containers.get(self.cname)
            if _container != None:
                _container.restart()
                return _container.attrs["State"]["Status"]
        except Exception as e:
            self.printer.print_error(
                Exception("Container %s Does Not Exist" % self.cname)
            )

    def container_status(self) -> NightcapDockerStatus:
        try:
            _container = self.docker.containers.get(self.cname)
            if _container == None:
                return NightcapDockerStatus.MISSING
            else:
                if _container.attrs["State"]["Status"] == "created":
                    return NightcapDockerStatus.EXISTS
                elif _container.attrs["State"]["Status"] == "running":
                    return NightcapDockerStatus.RUNNING
                elif _container.attrs["State"]["Status"] == "exited":
                    return NightcapDockerStatus.STOPPED
                else:
                    raise Exception("Container %s Status Needs Fixed!" % self.cname)
        except Exception as e:
            return NightcapDockerStatus.MISSING

    @abstractmethod
    def init_container(self) -> bool:
        raise NotImplementedError
