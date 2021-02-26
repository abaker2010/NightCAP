# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
from nightcappackages.classes import NightcapSubModule, NightcapPackages

class NightcapInstalledPackageCounter():
    def __init__(self):
        pass
        
    def count_from_selected_module(self, module: str):
        _count = 0
        _submodules = list(map(lambda v : v['type'], NightcapSubModule().find_submodules(module)))
        for _sm in _submodules:
            _count += len(list(map(lambda v : v, NightcapPackages().find_packages(module, _sm))))
        return _count

    def count_from_selected_submodule(self, path: list):
        try:
            print("list to use to find submodule", path)

            return len(list(map(lambda v : v, NightcapPackages().find_packages(path[0], path[1]))))
            
        except Exception as e:
            print(e)
            return []
        # return len(list(map(lambda v : v, NightcapPackages().find_packages(path[0], path[1]))))
