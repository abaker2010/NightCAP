# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
from nightcapcore.printers.print import Printer
from nightcapcore import NightcapCoreUpdaterBase, NightcapCoreUpaterRules
from tinydb import TinyDB
from tinydb.queries import Query
from nightcappackages.classes.paths.pathsenum import NightcapPackagesPathsEnum
from nightcappackages.classes.paths.paths import NightcapPackagesPaths
 
class NightcapSubModule(NightcapCoreUpdaterBase):
    def __init__(self):
        super(NightcapSubModule, self).__init__()
        self.db_submodules = TinyDB(NightcapPackagesPaths().generate_path(NightcapPackagesPathsEnum.Databases, ['submodules.json']))
        self.printer = Printer()
        
    def submodules(self):
        packags = list(map(lambda v : v['type'], self.db_submodules.table('submodules').all()))
        return packags

    def check_submodule_path(self, path: list):
        sub = list(map(lambda v : v, self.db_submodules.table('submodules').search(
            (Query()['module'] == path[0]) & (Query()['type'] == path[1])
        )))
        return sub

    def find_submodules(self, module: str):
        subs = list(map(lambda v : v, self.db_submodules.table('submodules').search(
            Query()['module'] == module
        )))
        return subs

    def submodule_install(self, module: str, submodule: str):
        _submoduleexists = self.db_submodules.table('submodules').search(
            (Query()['type'] == submodule) & (Query()['module'] == module)
        )

        if(len(_submoduleexists) == 0):
            _modules = self.db_submodules.table('submodules').all()
            if(len(_modules) == 0):
                _t = {'module' : module, 'type' : submodule}
            else:
                _t = {'module' : module, 'type' : submodule}
            self.db_submodules.table('submodules').insert(_t)

    def submodule_try_uninstall(self, module: str, submodule: str):
        _submoduleexists = self.db_submodules.table('submodules').search(
            (Query()['type'] == submodule) & (Query()['module'] == module)
        )
        self.db_submodules.table('submodules').remove(doc_ids=[_submoduleexists[0].doc_id])
        self.printer.print_formatted_check(text="Deleted package entry")

    def update(self, updatedb: TinyDB):
        super().update(updatetable=updatedb.table("submodules"),localtable=self.db_submodules.table("submodules"),checkonrow='module', checkonrowtwo='type', updaterrule=NightcapCoreUpaterRules.Submodule)
        # self.printer.item_2(text="updating db", optionalText='submodules.json')
        # self.printer.item_2(text="Checking entries: from update", leadingText='~')