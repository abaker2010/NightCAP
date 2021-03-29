# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
from nightcapcore.singleton.singleton import Singleton
from nightcappackages.classes.databases.mogo.connections.mongo_operation_connector import (
    MongoDatabaseOperationsConnection,
)


class MongoModuleDatabase(MongoDatabaseOperationsConnection, metaclass=Singleton):
    def __init__(self):
        MongoDatabaseOperationsConnection.__init__(self)
        self._db = self.client[self.conf.currentConfig["MONGOSERVER"]["db_name"]][
            "modules"
        ]

    def create(self, module: str = None):
        self._db.insert_one({"type": module})
        self.printer.print_formatted_check(text="Added to modules db")

    def read(self):
        return self._db.find()

    def update(self):
        pass

    def delete(self):
        pass

    def find(self, module: str = None):
        return self._db.find({"type": module})

    def find_one(self, module: str = None):
        return self._db.find_one({"type": module})

    def check_module_path(self, path: list):
        return self.find(path[0])

    def get_all_modules(self):
        _doc = self.read()
        return _doc

    def module_install(self, module: str):
        _moduleexists = self.find(module)
        if _moduleexists.count() == 0:
            self.create(module)
        else:
            pass

    def module_try_unintall(self, module: str):
        _moduleexists = self.find_one(module)
        # print("module found", _moduleexists)
        self._db.remove(_moduleexists)
        self.printer.print_formatted_additional(
            text="Deleted module entry", leadingTab=3
        )

    # region Not sure if this is working yet
    # def update(self, updatedb: TinyDB):
    # super().update(updatetable=updatedb.table('modules'),localtable=self.db_modules.table('modules'),checkonrow='type', updaterrule=NightcapCoreUpaterRules.Module)
    # endregion
