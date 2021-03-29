# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# from nightcappackages.classes import NightcapPackages
from nightcappackages.classes.databases.mogo.mongo_packages import MongoPackagesDatabase
from nightcappackages.classes.databases.mogo.mongo_submodules import (
    MongoSubModuleDatabase,
)


class NightcapInstalledPackageCounter:
    def __init__(self):
        pass

    def count_from_selected_module(self, module: str):
        return MongoSubModuleDatabase().find_submodules(module).count()

    def count_from_selected_submodule(self, module: str, submodule: str):
        try:
            return MongoPackagesDatabase().find_packages(module, submodule).count()
        except Exception as e:
            print(e)
            return []
