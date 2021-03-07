# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
from application.classes.helpers.screen.screen_helper import ScreenHelper
from nightcappackages.classes.databases.interfaces.template_interface import abstractfunc
from nightcappackages.classes.databases.interfaces.database_connector_interface import DatabaseConnectorInterface
from nightcapcore.printers.print import Printer
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
import time
import threading

class MongoDatabaseInterface(DatabaseConnectorInterface):
    def __init__(self, ip: str, port: str):
        self._connected = False
        self.printer = Printer()
        self.animationDone = False
        self.client = None
        try:
            self.connect(ip, port)
        except ServerSelectionTimeoutError as e:
            raise e
    
    def connect(self, ip: str = None, port: str = None):
        client = MongoClient(str(ip), int(port), serverSelectionTimeoutMS=500)
        client.server_info() # force connection on a request as the
                            # connect=True parameter of MongoClient seems
                            # to be useless here 
        self.client = client
        return True
        
    def transfer(self):
        pass

    def close(self):
        pass