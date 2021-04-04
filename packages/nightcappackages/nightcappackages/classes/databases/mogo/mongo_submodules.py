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

class MongoSubModuleDatabase(MongoDatabaseOperationsConnection, metaclass=Singleton):
    """
        
        This class is used to help validate user input to the console

        ...

        Attributes
        ----------
            _db: -> MongoClient

        Methods 
        -------
            Accessible 
            -------
                create(self, module: str = None, submodule: str = None): -> None
                    tries to insert a submodule into the db

                read(self): -> Any
                    returns all items in the db

                update(self): -> pass
                    Child will implement

                delete(self) -> pass
                    Child will implement

                find(self, module: str = None, submodule: str = None): -> dict
                    returns a dict if the submodules are found

                find_one(self, module: str = None, submodule: str = None): -> dict
                    returns a dict if the submodule is found

                find_submodules(self, module: str = None): -> dict
                    find all submodules of a module type

                check_submodule_path(self, path: list): -> dict
                    checks the submodules path

                submodule_install(self, module: str, submodule: str): -> None
                    tries to install the submodule
                
                submodule_try_uninstall(self, module: str, submodule: str): -> None
                    tries to uninstall the submodule
    """
    #region Init
    def __init__(self):
        MongoDatabaseOperationsConnection.__init__(self)
        self._db = self.client[self.conf.config["MONGOSERVER"]["db_name"]][
            "submodules"
        ]
    #endregion

    #region Create
    def create(self, module: str = None, submodule: str = None):
        self._db.insert_one({"module": module, "type": submodule})
        self.printer.print_formatted_check(text="Added to submodules db")
    #endregion

    #region Read
    def read(self):
        return self._db.find()
    #endregion

    #region Update
    def update(self):
        # def update(self, updatedb: TinyDB):
        # super().update(updatetable=updatedb.table("submodules"),localtable=self.db_submodules.table("submodules"),checkonrow='module', checkonrowtwo='type', updaterrule=NightcapCoreUpaterRules.Submodule)
        pass
    #endregion

    #region Delete
    def delete(self):
        pass
    #endregion

    #region Find
    def find(self, module: str = None, submodule: str = None):
        return self._db.find(
            {"$and": [{"module": {"$eq": module}}, {"type": {"$eq": submodule}}]}
        )
    #endregion

    #region Find One
    def find_one(self, module: str = None, submodule: str = None):
        return self._db.find_one({"module": module, "submodule": submodule})
    #endregion

    #region Find Submodules
    def find_submodules(self, module: str = None):
        # print("Trying to find submodules in db", module)
        return self._db.find({"module": module})
    #endregion

    #region Check submodule path
    def check_submodule_path(self, path: list):
        # return self.find_one(path[0], path[1])
        # print("submodule path to find", path)
        _subpath = self._db.find(
            {"$and": [{"module": {"$eq": path[0]}}, {"type": {"$eq": path[1]}}]}
        )
        # print("Submodules path", _subpath.count())
        return _subpath
    #endregion

    #region Install Submodule
    def submodule_install(self, module: str, submodule: str):
        _submoduleexists = self.find(module, submodule)
        if _submoduleexists.count() == 0:
            self.create(module, submodule)
        else:
            pass
    #endregion

    #region Uninstall Submodule
    def submodule_try_uninstall(self, module: str, submodule: str):
        _submoduleexists = self.find_one(module, submodule)
        self._db.remove(_submoduleexists)
        self.printer.print_formatted_additional(
            text="Deleted submodule entry", leadingTab=3
        )
    #endregion
