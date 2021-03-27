#!/usr/bin/env python3.8
# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
from os import sendfile
from nightcapcli.observer.publisher_base import NightcapCLIPublisherBase
from nightcappackages.classes.databases.mogo.mongo_modules import MongoModuleDatabase
from nightcappackages.classes.databases.mogo.mongo_packages import MongoPackagesDatabase
from nightcappackages.classes.databases.mogo.mongo_submodules import MongoSubModuleDatabase
from nightcapcore import Singleton
from nightcapcore.printers.print import Printer

class NightcapCLIPublisher(NightcapCLIPublisherBase, metaclass=Singleton):
    def __init__(self):
        NightcapCLIPublisherBase.__init__(self,['basecli'])

        self.modules_db = MongoModuleDatabase()
        self.submodules_db = MongoSubModuleDatabase()
        self.packages_db = MongoPackagesDatabase()
        self.printer = Printer()
        self.selectedList = []

    def set_list(self, list: list = []):
        self.selectedList = list

    def isValid(self, options, selectedList):
        return self._validate(options, selectedList)

    def get_package_config(self, path: list):
        self.pkg_conf = self.packages_db.get_package_config(path)
        # print("Found pkg config", self.pkg_conf)
        return self.pkg_conf
        
    def _check_module_types(self, path: list):
        return False if self.modules_db.check_module_path(path).count() == 0 else True

    def _check_sub_module(self, path: list):
        # print("Checking submodule", path)
        return False if self.submodules_db.check_submodule_path(path).count() == 0 else True

    def _check_packages(self, selected):
        # print("Checking package")
        return self.packages_db.check_package_path(selected)

    def _check_current_path(self, path: list):
        if(len(path) == 1):
            return self._check_module_types(path)
        elif(len(path) == 2):
            return self._check_module_types(path) & self._check_sub_module(path)
        elif(len(path) == 3):
            return self._check_module_types(path) & self._check_sub_module(path) & self._check_packages(path)
        return False

    def compare(self):
        if self.selectedList == []:
            return {'add': len(self.newSelectedList)}

        else:
            _add = 0
            print("Comparing New Selected List:", self.newSelectedList)
            print("Comparing Selected List:", self.selectedList)
            for i in range(len(self.newSelectedList)):
                print("* Trying to compare items")
                try:
                    if self.selectedList[i] != self.newSelectedList[i]:
                        print('Different:', self.selectedList[i],  self.newSelectedList[i])
                        _add += 1
                    else:
                        print('Same:', self.selectedList[i],  self.newSelectedList[i])
                except IndexError as e:
                    _add += 1
                except Exception as e:
                    self.printer.print_error(exception=e)
                i += 1
            return {'add': _add}
            


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

            _validCommand  = False
            _tmpNewList = []

            # Condition
            ####
            # split = 2, items = 3
            # i/i/i
            if len(_cleanedItems) == 3:
                # print("3 sections")
                if _splitCount == 2:
                    # print("Valid command")
                    if(len(_cleanedItems) <= 3):
                        _tmpNewList = _cleanedItems
                        _validCommand = True
            # Condition
            ####
            # split = 2, items = 2
            # /i/i  (combine)
            # i/i   (replace)
            elif len(_cleanedItems) == 2:
                # print("2 sections")
                if _splitCount == 2:
                    # print("valid command")
                    # print("Split count 2")
                    if(_emptyFront):
                        if(len(_combined) <=3):
                            _tmpNewList =  _combined
                            _validCommand = True
                    else:
                        # print("Not empty front needs done")
                        if(len(_cleanedItems) <= 3):
                            _tmpNewList = _cleanedItems
                            _validCommand =  True
                elif _splitCount == 1:
                    # print("valid command")
                    # print("Split count 1")
                    if(_emptyFront):
                        if(len(_combined) <=3):
                            _tmpNewList =  _combined
                            _validCommand =  True
                    else:
                        # print("Not empty front needs done")
                        if(len(_cleanedItems) <= 3):
                            _tmpNewList = _cleanedItems
                            _validCommand =  True
            # Condition
            ####
            # split = 0|1, items = 1
            # /i  (combine)
            # i   (add)
            elif len(_cleanedItems) == 1:
                # print("1 section")
                if _splitCount == 1:
                    # print("valid command")
                    if(_hasEmpty):
                        if(_emptyBack):
                            _tmpNewList = _cleanedItems
                            _validCommand =  True
                        elif(_emptyFront):
                            if(len(_combined) <= 3):
                                _tmpNewList = _combined
                                _validCommand =  True
                elif _splitCount == 0:
                    # print("valid command")
                    if(len(_combined) <= 3):
                        _tmpNewList = _combined
                        _validCommand =  True
            else:
                return False

            # print("Valid command 1", _validCommand)
            # print("Tmp list to check", _tmpNewList)
            if(_validCommand):
                if(self._check_current_path(_tmpNewList)):
                    self.newSelectedList = _tmpNewList
                    return True
                else:
                    # print("Error with path")
                    return False
            else:
                return False
        except Exception as e:
            print("Error with options validation", e)
            return False