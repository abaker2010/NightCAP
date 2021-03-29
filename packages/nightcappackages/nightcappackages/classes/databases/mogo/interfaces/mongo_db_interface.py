# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
from nightcapcore import Printer
from pymongo import MongoClient, auth
from pymongo.errors import ServerSelectionTimeoutError

class MongoDatabaseInterface:
    client = None

    def __init__(self, ip: str, port: str, username: str = None, password: str = None, authMechanism: str = 'SCRAM-SHA-256'):
        self._connected = False
        self.printer = Printer()
        self.animationDone = False
        self.client = None
        try:
            if(username != None):
                self.connect_authenticated(ip, port, username, password, authMechanism)
            else:
                # raise Exception("Unauthenticated connection")
                print("Trying to use unauthenticated connection")
                self.connect_unauthenticated(ip, port)
        except ServerSelectionTimeoutError as e:
            raise e
        except Exception as e:
            raise e
    
    def connect_authenticated(self, ip: str, port: str, username: str, password: str, authMechanism: str):
        client = MongoClient(str(ip), int(port), username=username, password=password, authMechanism=authMechanism, serverSelectionTimeoutMS=1000,)
        client.server_info() # force connection on a request as the
                            # connect=True parameter of MongoClient seems
                            # to be useless here 
        self.client = client
        return True

    def connect_unauthenticated(self, ip: str, port: str):
        client = MongoClient(str(ip), int(port), serverSelectionTimeoutMS=300)
        client.server_info() # force connection on a request as the
                            # connect=True parameter of MongoClient seems
                            # to be useless here 
        self.client = client
        return True
        
    def transfer(self):
        pass

    def close(self):
        self.client.close()