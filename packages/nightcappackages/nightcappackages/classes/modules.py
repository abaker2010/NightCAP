# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
from typing import Mapping
from nightcapcore.printers.print import Printer
from nightcapcore import NightcapCoreUpdaterBase
from nightcapcore import NightcapCoreUpaterRules
from nightcappackages.classes.paths.pathsenum import NightcapPackagesPathsEnum
from nightcappackages.classes.paths.paths import NightcapPackagesPaths
from tinydb import TinyDB, Query

class NightcapModules(NightcapCoreUpdaterBase):
    def __init__(self) -> None:
        super(NightcapModules, self).__init__()
        self.db_modules = TinyDB(NightcapPackagesPaths().generate_path(NightcapPackagesPathsEnum.Databases, ['modules.json']))
        self.printer = Printer()
        
    def insert(self, obj: Mapping):
        self.db_modules.table("modules").insert(obj)

    def tables(self):
        return self.db_modules.tables()

    def module_types(self):
        types = list(map(lambda v : v['type'], self.db_modules.table('modules').all()))
        return types 

    def check_module_path(self, path: list):
        return self.db_modules.table("modules").search(
            (Query()['type'] == path[0])
        )

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
        self.printer.print_formatted_additional(text="Deleted module entry", leadingTab=3)
        
    def update(self, updatedb: TinyDB):
        super().update(updatetable=updatedb.table('modules'),localtable=self.db_modules.table('modules'),checkonrow='type', updaterrule=NightcapCoreUpaterRules.Module)
    
    
    