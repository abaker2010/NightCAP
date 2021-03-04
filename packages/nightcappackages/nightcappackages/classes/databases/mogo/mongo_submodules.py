# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Import
# from application.classes.base_cmd.base_cmd import NightcapBaseCMD
from nightcappackages.classes.databases.mogo.interfaces.mogo_operations import MongoDatabaseOperationsInterface
from nightcappackages.classes.databases.mogo.mongo_connection import MongoDatabaseConnection
from nightcapcore.decorators.singleton import Singleton

@Singleton
class MongoSubModuleDatabase(MongoDatabaseConnection, MongoDatabaseOperationsInterface):
    def __init__(self):
        MongoDatabaseConnection.__init__(self)
        MongoDatabaseOperationsInterface.__init__(self)
        self._db = self.client[self.conf.currentConfig['MONGOSERVER']['db_name']]['submodules']

    def create(self, module: str = None, submodule: str = None):
        self._db.insert_one({'module' : module, 'type' : submodule})
        self.printer.print_formatted_check(text="Added to submodules db")

    def read(self):
        return self._db.find()
        

    def update(self):
        # def update(self, updatedb: TinyDB):
        # super().update(updatetable=updatedb.table("submodules"),localtable=self.db_submodules.table("submodules"),checkonrow='module', checkonrowtwo='type', updaterrule=NightcapCoreUpaterRules.Submodule)
        pass

    def delete(self):
        pass

    def find(self, module: str = None, submodule: str = None):
        return self._db.find({
        "$and" : [
            {'module' : {"$eq": module}},
            {'type' : {"$eq": submodule}}
        ]})

    def find_one(self, module: str = None, submodule: str = None):
        return self._db.find_one({'module' : module, 'submodule' : submodule})

    def find_submodules(self, module: str = None):
        # print("Trying to find submodules in db", module)
        return self._db.find({"module" : module})

    def check_submodule_path(self, path: list):
        # return self.find_one(path[0], path[1])
        # print("submodule path to find", path)
        _subpath = self._db.find({
            "$and" : [
                {'module' : {"$eq" : path[0]}},
                {'type' : {"$eq" : path[1]}}
            ]
        })
        # print("Submodules path", _subpath.count())
        return _subpath

    def submodule_install(self, module: str, submodule: str):
        _submoduleexists = self.find(module, submodule)
        if(_submoduleexists.count() == 0):
            self.create(module, submodule)
        else:
            pass
    
    def submodule_try_uninstall(self, module: str, submodule: str):
        _submoduleexists = self.find_one(module, submodule)
        self._db.remove(_submoduleexists)
        self.printer.print_formatted_additional(text="Deleted submodule entry", leadingTab=3)