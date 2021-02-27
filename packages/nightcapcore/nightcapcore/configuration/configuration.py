# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
import os
import configparser
from nightcapcore.singleton.singleton import Singleton

class NighcapCoreConfiguration(metaclass=Singleton):

    def __init__(self):
        self.installationDir = os.path.dirname(os.path.abspath(__file__)) + '/'
        self.configFile = self.installationDir + "nightcapcore.cfg"
        self.configParser = configparser.RawConfigParser()
        self.currentConfig = None
        self._config()
        
    def _config(self):
        conf = configparser.RawConfigParser()
        conf.read(self.configFile)
        self.currentConfig = conf
        

    def Save(self):
        conf = configparser.RawConfigParser()
        with open(self.configFile, 'w') as configfile:
            self.currentConfig.write(configfile)
    