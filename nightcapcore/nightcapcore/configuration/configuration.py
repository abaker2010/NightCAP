# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
import os
import configparser
from pathlib import Path
from nightcapcore.printers.print import Printer
from nightcapcore.singleton.singleton import Singleton


class NightcapCLIConfiguration(metaclass=Singleton):
    def __init__(self, data: dict = None) -> None:
        self._config()
        self.printer = Printer()

        self.verbosity = self.config.getboolean("NIGHTCAPCORE", "verbose")

        self.project = (
            None
            if self.config.get("NIGHTCAPSCAN", "project") == "None"
            else self.config.get("NIGHTCAPSCAN", "project")
        )

        self.buildNumber = int(self.config.get("BUILD_DATA", "build"))
        self.versionNumber = int(self.config.get("BUILD_DATA", "version"))
        self.mainbranch = self.config.getboolean("BUILD_DATA", "main_branch")

        if data != None:
            self.project = data['project']

    def _config(self) -> None:
        conf = configparser.RawConfigParser()
        _path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "nightcapcore.cfg"
        )
        conf.read(_path)
        self.config = conf
        # return conf

    def Save(self) -> None:
        _path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "nightcapcore.cfg"
        )
        with open(_path, "w") as configfile:
            self.config.write(configfile)
