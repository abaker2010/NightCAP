# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Import
from nightcapcore import NightcapCLIConfiguration
from nightcapcore.singleton.singleton import Singleton
from nightcappackages.classes.databases.mogo.interfaces.mongo_db_interface import MongoDatabaseInterface
from nightcapcore.interface.template_interface import abstractfunc
from pymongo.errors import ServerSelectionTimeoutError

class MongoDatabaseOperationsConnection(MongoDatabaseInterface):
    def __init__(self):
        self.conf = NightcapCLIConfiguration()
        ip = self.conf.currentConfig["MONGOSERVER"]["ip"]
        port = self.conf.currentConfig["MONGOSERVER"]["port"]
        _db_name = self.conf.currentConfig["MONGOSERVER"]["db_name"]
        _uname = self.conf.currentConfig["MONGOSERVER"]["username"]
        _pass = self.conf.currentConfig["MONGOSERVER"]["password"]
        
        self.name = None
        if ip == None:
            raise Exception("Mongo Server IP not set")
        if port == None:
            raise Exception("Mongo Server Port not set")
        if _db_name == None:
            raise Exception("Mongo Server DB_Name not set")
        else:
            self.db_name = _db_name
        try:
            super().__init__(ip, port, _uname, _pass)
        except ServerSelectionTimeoutError as e:
            raise e

    @abstractfunc
    def create(self):
        pass

    @abstractfunc
    def read(self):
        pass

    @abstractfunc
    def update(self):
        pass

    @abstractfunc
    def delete(self):
        pass