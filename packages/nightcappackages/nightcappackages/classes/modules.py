# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
from typing import Mapping
from nightcappackages.classes.paths.pathsenum import NightcapPackagesPathsEnum
from nightcappackages.classes.paths.paths import NightcapPackagesPaths
# from nightcappackages.classes.submodules import NightcapSubModule

from tinydb import TinyDB, Query

class NightcapModules():
    def __init__(self):
        self.db_modules = TinyDB(NightcapPackagesPaths().generate_path(NightcapPackagesPathsEnum.Databases, ['modules.json']))
    
    def insert(self, obj: Mapping):
        self.db_modules.table("modules").insert(obj)

    def tables(self):
        return self.db_modules.tables()

    def module_types(self):
        types = list(map(lambda v : v['type'], self.db_modules.table('modules').all()))
        return types 

    def get_all_modules(self):
        return self.db_modules.table("modules").all()

    def module_install(self, module: str):
        #region Checking for module type in db
        _moduleexists = self.db_modules.table('modules').search(
            (Query()['type'] == module)
        )

        if(len(_moduleexists) == 0):
            _modules = self.db_modules.table('modules').all()
            if(len(_modules) == 0):
                _t = {'type' : module}
            else:
                _t = {'type' : module}
            self.db_modules.table('modules').insert(_t)
        #endregion
    
    def module_try_unintall(self, module: str):
        _moduleexists = self.db_modules.table('modules').search((Query()['type'] == module))
        self.db_modules.table('modules').remove(doc_ids=[_moduleexists[0].doc_id])
        
    def __has_module(self, module: str):
        return self.db_modules.table("modules").search(Query()["type"] == module)

    def update(self,updatedb: TinyDB):
        print("\t","updating db: projects_db.json")
        print("\t","updater tables:", updatedb.tables())
        modules = updatedb.table('modules').all()
        if(modules == []):
            print("No Modules to add")
        else:
            for module in updatedb.table('modules').all():
                print(module)
                if(self.__has_module(module['type']) == []):
                    self.insert(module)
                else:
                    print("Not inserting module")
        print("\t","user tables:", self.db_modules.tables())

        # for module in self.db_modules.table('modules').all():
        #     print(module)
        #     print(self.__has_module(module['type']))
    
    