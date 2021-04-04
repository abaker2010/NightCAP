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
    def __init__(self):
        self._config()
        self.printer = Printer()

        self.project = (
            None
            if self.config.get("NIGHTCAPSCAN", "project") == "None"
            else self.config.get("NIGHTCAPSCAN", "project")
        )
        self.isDir = (
            False
            if self.config.getboolean("NIGHTCAPSCAN", "isdir") == "None"
            else self.config.getboolean("NIGHTCAPSCAN", "isdir")
        )
        self.dir = (
            os.path.join(Path(__file__).resolve().parent.parent, "test_pcaps")
            if self.config.get("NIGHTCAPSCAN", "dir") == "None"
            else self.config.get("NIGHTCAPSCAN", "dir")
        )
        self.filename = (
            "Obscure.pcap"
            if self.config.get("NIGHTCAPSCAN", "filename") == "None"
            else self.config.get("NIGHTCAPSCAN", "filename")
        )

    def _config(self):
        conf = configparser.RawConfigParser()
        _path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "nightcapcore.cfg"
        )
        conf.read(_path)
        self.config = conf
        # return conf

    def Save(self):
        _path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "nightcapcore.cfg"
        )
        with open(_path, "w") as configfile:
            self.config.write(configfile)
