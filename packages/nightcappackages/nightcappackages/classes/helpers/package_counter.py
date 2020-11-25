# Copyright 2020 by Aarom Baker.
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

    def count_from_selected_submodule(self, module: str, submodule: str):
        return len(list(map(lambda v : v, NightcapPackages().find_packages(module, submodule))))
