# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Import 
from nightcappackages import *
from application.classes.helpers.screen.screen_helper import ScreenHelper
# endregion

class NightcapCLIOptionsValidator():
    def __init__(self, options, selectedList):
        self.modules_db = NightcapModules()
        self.submodules_db = NightcapSubModule()
        self.packages_db = NightcapPackages()
        self.newSelectedList = []
        self.isvalid = self._validate(options, selectedList)
        
    def _check_module_types(self, line):
        # print("Trying to find", line)
        if(line in self.modules_db.module_types()):
            ScreenHelper().clearScr()
            return True
        else:
            return False

    def _check_sub_module(self, line):
        if(line in self.submodules_db.submodules()):
            ScreenHelper().clearScr()
            return True
        else:
            return False

    def _check_packages(self, line, selected):
        print(self.packages_db.packages(selected))
        if(line in self.packages_db.packages(selected)):
            ScreenHelper().clearScr()
            return True
        else:
            return False

    def _validate(self, line: str, selected: list):

        try:
            _options = []
            _splitCount = 0
            if('/' in line):
                _options = line.split('/')
                _splitCount = line.count('/')
                # print("line was split")
                # self.postNeeded = len(_options)
            else:
                _options = [line]

            # for filtering
            _orgItems = _options
            _hasEmpty = '' in _orgItems
            _emptyFront = '' == _orgItems[0]
            _emptyBack = '' == _orgItems[-1]
            # cleans list
            _cleanedItems = list(filter(lambda item: item != '', _orgItems))
            _combined = selected + _cleanedItems
            ######

            print("Options", _options)
            print('Selected', selected)
            print("_hasEmpty", _hasEmpty)
            print("_emptyFront", _emptyFront)
            print("_emptyBack", _emptyBack)
            print("_cleanedItems selected", _cleanedItems)
            print("_splitcount", _splitCount)
            print("*" * 10, end="\n\n")
            
            print("Has empty", _hasEmpty)
            if len(_cleanedItems) == 3:
                print("3 sections")
                if _splitCount == 2:
                    print("Valid command")
                    if(len(_cleanedItems) <= 3):
                        self.newSelectedList = _cleanedItems
                        return True
                    else:
                        return False
                else:
                    return False
            elif len(_cleanedItems) == 2:
                print("2 sections")
                if _splitCount == 2:
                    print("valid command")
                    print("Split count 2")
                    if(_emptyFront):
                        if(len(_combined) <=3):
                            self.newSelectedList =  _combined
                            return True
                        else:
                            print("To long")
                            return False
                    else:
                        print("Not empty front needs done")
                        if(len(_cleanedItems) <= 3):
                            self.newSelectedList = _cleanedItems
                            return True
                        else:
                            return False
                elif _splitCount == 1:
                    print("valid command")
                    print("Split count 1")
                    if(_emptyFront):
                        if(len(_combined) <=3):
                            self.newSelectedList =  _combined
                            return True
                        else:
                            print("To long")
                            return False
                    else:
                        print("Not empty front needs done")
                        if(len(_cleanedItems) <= 3):
                            self.newSelectedList = _cleanedItems
                            return True
                        else:
                            return False
                else:
                    print("Split count 0")
                    return False
            elif len(_cleanedItems) == 1:
                print("1 section")
                if _splitCount == 1:
                    print("valid command")
                    if(_hasEmpty):
                        if(_emptyBack):
                            self.newSelectedList = _cleanedItems
                            return True
                        elif(_emptyFront):
                            if(len(_combined) <= 3):
                                self.newSelectedList = _combined
                                return True
                            else:
                                return False
                elif _splitCount == 0:
                    print("valid command")
                    if(len(_combined) <= 3):
                        self.newSelectedList = _combined
                        return True
                    else:
                        print("To many selected")
                        return False
                else:
                    return False
            else:
                return False
            return False
        except Exception as e:
            print("Error eith options validation", e)
            return False