# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Imports

from typing import final
from nightcapcore import *
import shutil
from colorama import Fore, Style
from nightcapcore import Printer
import requests
from tqdm.auto import tqdm
import os
import tempfile
import shutil
import urllib
import json
import time
import sys
from nightcappackages import *
from nightcapcore import NightcapCLIConfiguration
from nightcappackages.classes.commands.installer import NightcapPackageInstallerCommand
from nightcappackages.classes.commands.uninstaller import NightcapPackageUninstallerCommand
from nightcappackages.classes.databases.mogo.mongo_packages import MongoPackagesDatabase
# endregion


class NightcapUpdaterRebootCommand(Command):
    def __init__(self) -> None:
        super().__init__()
        

    def execute(self) -> None:
        print("Reboot please")
        raise KeyboardInterrupt("Restarting")


