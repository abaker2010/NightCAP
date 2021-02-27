# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Import
# from application.classes.base_cmd.base_cmd import NightcapBaseCMD

from nightcapcore.singleton.singleton import Singleton
from nightcappackages.classes.databases.mogo.interfaces.mongo_network import MongoDatabaseInterface
from pymongo.errors import ServerSelectionTimeoutError

class MogoModuleDatabase(MongoDatabaseInterface):
    def __init__(self, ip: str = None, port: str = None):
        
        if ip == None:
            raise Exception("Mongo Server IP not set")
        if port == None:
            raise Exception("Mongo Server Port not set")
        try:
            super().__init__(ip, port)
        except ServerSelectionTimeoutError as e:
            raise e
        # print("Connected to Mongo Server", MongoDatabaseInterface.connect(self))

    def test(self):
        print("Called testing")