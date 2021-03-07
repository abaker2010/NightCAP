# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Import
# from application.classes.base_cmd.base_cmd import NightcapBaseCMD
from nightcapcore.configuration.configuration import NighcapCoreConfiguration
from nightcapcore.decorators.singleton import Singleton
from nightcappackages.classes.databases.mogo.interfaces.mongo_network import MongoDatabaseInterface
from nightcappackages.classes.databases.mogo.mongo_connection import MongoDatabaseConnection
from pymongo.errors import ServerSelectionTimeoutError

@Singleton
class MongoDatabaseChecker(MongoDatabaseConnection):
    def __init__(self):
        super().__init__()
        
    def check_database(self):
        if(self.db_name in self.client.list_database_names()):
            return True
        else:
            return False

    def initialize_database(self):
        mydict = { "name": "John", "address": "Highway 37" }
        self.client[self.db_name]['holder'].insert_one(mydict)

    def test(self):
        print("Called testing")