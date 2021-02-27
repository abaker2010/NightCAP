# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Import
# from application.classes.base_cmd.base_cmd import NightcapBaseCMD
from nightcappackages.classes.databases.mogo.interfaces.mongo_network import MongoDatabaseInterface
from pymongo.errors import ServerSelectionTimeoutError

class MongoDatabaseChecker(MongoDatabaseInterface):
    def __init__(self, ip: str = None, port: str = None, db_name: str = None):
        
        if ip == None:
            raise Exception("Mongo Server IP not set")
        if port == None:
            raise Exception("Mongo Server Port not set")
        if db_name == None:
            raise Exception("Mongo Server DB_Name not set")
        else:
            self.db_name = db_name
        try:
            super().__init__(ip, port)
        except ServerSelectionTimeoutError as e:
            raise e
        # print("Connected to Mongo Server", MongoDatabaseInterface.connect(self))

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