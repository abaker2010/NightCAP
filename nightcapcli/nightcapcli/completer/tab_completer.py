# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
#region Imports
import re
from nightcappackages.classes.databases.mogo import MongoModuleDatabase, MongoPackagesDatabase, MongoSubModuleDatabase
from pymongo.common import validate
#endregion

class NightcapTabCompleter(object):

    def __init__(self) -> None:
        super().__init__()

    def complete(self, selected: list, text: str, line: str):
        
        if '/' in line:
            _split = [i for i in line.split('/') if i != '']

            if len(selected) == 0:
                if len(_split) == 1:
                    vals = list(
                        map(
                            lambda v: v["type"],
                            MongoSubModuleDatabase().find_submodules(_split[0]),
                        )
                    )
                
                    return [
                            i
                            for i in vals
                            if i.startswith(text)
                        ]
                elif len(_split) == 2:
                    
                    _sub_exists = list(
                        map(
                            lambda v: v["type"],
                            MongoSubModuleDatabase().find_submodules(_split[0]),
                        )
                    )

                    if _split[1] not in _sub_exists:
                        return [i for i in _sub_exists if i.startswith(_split[1])]
                    else:
                        
                        _ = MongoPackagesDatabase().packages(_split, False)
                        return [
                            i
                            for i in _
                            if i.startswith(text)
                        ]
        
        else:
            if len(selected) == 0: 
                _ = list(
                    map(lambda v: v["type"], MongoModuleDatabase().get_all_modules())
                )

                if _ == []:
                    return ["No Packages Installed", " "]
                else:
                    return [
                            i
                            for i in _
                            if i.startswith(text)
                        ]
            elif len(selected) == 1: 
                _ = list(
                        map(
                            lambda v: v["type"],
                            MongoSubModuleDatabase().find_submodules(selected[0]),
                        )
                    )

                return [
                        i
                        for i in _
                        if i.startswith(text)
                    ]
            elif len(selected) == 2: 
                _ = MongoPackagesDatabase().packages(selected, False)
                
                return [
                        i
                        for i in _
                        if i.startswith(text)
                    ]
