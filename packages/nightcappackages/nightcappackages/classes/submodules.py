# Copyright 2020 by Aarom Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
from tinydb import TinyDB
from tinydb.queries import Query
from nightcappackages.classes.paths.pathsenum import NightcapPackagesPathsEnum
from nightcappackages.classes.paths.paths import NightcapPackagesPaths
 
class NightcapSubModule():
    def __init__(self):
        self.db_submodules = TinyDB(NightcapPackagesPaths().generate_path(NightcapPackagesPathsEnum.Databases, ['submodules.json']))

    def submodules(self):
        packags = list(map(lambda v : v['type'], self.db_submodules.table('submodules').all()))
        return packags

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
