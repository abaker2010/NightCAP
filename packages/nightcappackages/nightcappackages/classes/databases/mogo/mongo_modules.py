# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
#region Imports
from nightcapcore.singleton.singleton import Singleton
from nightcappackages.classes.databases.mogo.connections.mongo_operation_connector import (
    MongoDatabaseOperationsConnection,
)
#endregion

class MongoModuleDatabase(MongoDatabaseOperationsConnection, metaclass=Singleton):
    """
        
        This class is used interact with the mongo databse

        ...

        Attributes
        ----------
            _db: -> MongoClient
                the connection to the db

        Methods 
        -------
            Accessible 
            -------
                create(self, module: str = None): -> None
                    addes a new module to the database

                read(self): -> Any
                    this will read the database

                update(self): -> pass
                    for override when implemented

                delete(self): -> pass
                    for override when implemented

                find(self, module: str = None): -> Any
                    returns the results of the find query

                find_one(self, module: str = None): -> Any
                    returns the results of the find one query

                check_module_path(self, path: list): -> Any
                    returns the module if exists

                get_all_modules(self): -> Any
                    returns all of the modules

                module_install(self, module: str): -> None
                    tries to install the module
                

                module_try_unintall(self, module: str): -> None
                    tries to uninstall the module
    """
    #region Init
    def __init__(self):
        MongoDatabaseOperationsConnection.__init__(self)
        self._db = self.client[self.conf.config["MONGOSERVER"]["db_name"]][
            "modules"
        ]
    #endregion

    #region Create
    def create(self, module: str = None):
        self._db.insert_one({"type": module})
        self.printer.print_formatted_check(text="Added to modules db")
    #endregion

    #region Read
    def read(self):
        return self._db.find()
    #endregion
    
    #region Update
    def update(self):
        pass
    #endregion

    #region Delete
    def delete(self):
        pass
    #endregion

    #region Find
    def find(self, module: str = None):
        return self._db.find({"type": module})
    #endregion

    #region Find One
    def find_one(self, module: str = None):
        return self._db.find_one({"type": module})
    #endregion

    #region Check Module Path
    def check_module_path(self, path: list):
        return self.find(path[0])
    #endregion

    #region Get All Modules
    def get_all_modules(self):
        _doc = self.read()
        return _doc
    #endregion

    #region Install Module
    def module_install(self, module: str):
        _moduleexists = self.find(module)
        if _moduleexists.count() == 0:
            self.create(module)
        else:
            pass
    #endregion

    #region Uninstall Module
    def module_try_unintall(self, module: str):
        _moduleexists = self.find_one(module)
        # print("module found", _moduleexists)
        self._db.remove(_moduleexists)
        self.printer.print_formatted_additional(
            text="Deleted module entry", leadingTab=3
        )
    #endregion

    # region Not sure if this is working yet
    # def update(self, updatedb: TinyDB):
    # super().update(updatetable=updatedb.table('modules'),localtable=self.db_modules.table('modules'),checkonrow='type', updaterrule=NightcapCoreUpaterRules.Module)
    # endregion
