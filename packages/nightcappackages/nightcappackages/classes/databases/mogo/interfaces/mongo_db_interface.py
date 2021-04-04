# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
#region Import
from nightcapcore import Printer
from pymongo import MongoClient, auth
from pymongo.errors import ServerSelectionTimeoutError
#endregion

class MongoDatabaseInterface:
    """
        
        This class is the base MongoDB Inferface

        ...

        Attributes
        ----------
            ip: -> str
                ip address of the database

            port: -> str
                port for the database

            username: -> str
                username for the database

            password: -> str
                password for the database

            authMechanism: -> str
                authentication type default is SCRAM-SHA-256


        Methods 
        -------
            Accessible 
            -------
                connect_authenticated(self, ip: str, port: str, username: str, password: str, authMechanism: str): -> bool
                    connects to the database via authentication method

                connect_unauthenticated(self, ip: str, port: str): -> bool
                    connects to the database with no security

                transfer(self): -> pass
                    transfer data needs to be done by object that is doing the inheritance

                close(self): -> None    
                    closes the client connection to the databse

            None Accessible
            -------

    """
    client = None
    #region Init
    def __init__(
        self,
        ip: str,
        port: str,
        username: str = None,
        password: str = None,
        authMechanism: str = "SCRAM-SHA-256",
    ):
        self._connected = False
        self.printer = Printer()
        self.animationDone = False
        self.client = None
        try:
            if username != None:
                self.connect_authenticated(ip, port, username, password, authMechanism)
            else:
                # raise Exception("Unauthenticated connection")
                print("Trying to use unauthenticated connection")
                self.connect_unauthenticated(ip, port)
        except ServerSelectionTimeoutError as e:
            raise e
        except Exception as e:
            raise e
    #endregion

    #region Authenticated Connection
    def connect_authenticated(
        self, ip: str, port: str, username: str, password: str, authMechanism: str
    ):
        client = MongoClient(
            str(ip),
            int(port),
            username=username,
            password=password,
            authMechanism=authMechanism,
            serverSelectionTimeoutMS=1000,
        )
        client.server_info()  # force connection on a request as the
        # connect=True parameter of MongoClient seems
        # to be useless here
        self.client = client
        return True
    #endregion

    #region Unauthenticated Connection
    def connect_unauthenticated(self, ip: str, port: str):
        client = MongoClient(str(ip), int(port), serverSelectionTimeoutMS=300)
        client.server_info()  # force connection on a request as the
        # connect=True parameter of MongoClient seems
        # to be useless here
        self.client = client
        return True
    #endregion

    #region Transfer
    def transfer(self):
        pass
    #endregion

    #region Close 
    def close(self):
        self.client.close()
    #endregion
