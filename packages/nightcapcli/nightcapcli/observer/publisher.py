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
from nightcappackages.classes.databases.mogo.mongo_submodules import (
    MongoSubModuleDatabase,
)
from nightcapcore import Singleton
from nightcapcore.printers.print import Printer


class NightcapCLIPublisher(NightcapCLIPublisherBase, metaclass=Singleton):
    def __init__(self):
        NightcapCLIPublisherBase.__init__(self, ["basecli"])

        self.modules_db = MongoModuleDatabase()
        self.submodules_db = MongoSubModuleDatabase()
        self.packages_db = MongoPackagesDatabase()
        self.printer = Printer()
        self.selectedList = []
        # ----------------------

        self.directions = {"nextstep": [], "additionalsteps": [], "remove": 0}

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
        return (
            False
            if self.submodules_db.check_submodule_path(path).count() == 0
            else True
        )

    def _check_packages(self, selected):
        # print("Checking package")
        return self.packages_db.check_package_path(selected)

    def _check_current_path(self, path: list):
        if len(path) == 1:
            return self._check_module_types(path)
        elif len(path) == 2:
            return self._check_module_types(path) & self._check_sub_module(path)
        elif len(path) == 3:
            return (
                self._check_module_types(path)
                & self._check_sub_module(path)
                & self._check_packages(path)
            )
        return False

    # listA: selected list
    # # listB: tmp list
    # def _get_next_steps(self, listA: list, listB: list):
    #     print("Comparing")
    #     print(listA)
    #     print(listB)

    def _get_pop(self, list: list):
        _pop = 0

        if self.selectedList == []:
            # print("check remove: return 0")
            return 0
        else:
            if len(self.selectedList) == 1:
                # print("check remove: return 1")
                return 1
            elif len(self.selectedList) == 2:
                if self.selectedList[0] != list[0]:
                    # print("List[0] Dif")
                    _pop = 2
                elif self.selectedList[1] != list[1]:
                    # print("List[1] Dif")
                    _pop = 1

                # print("check remove: return 2, pop", _pop)
                return _pop
            elif len(self.selectedList) == 3:
                # print("check remove: return 3")
                return 3

    def _validate(self, line: str, selected: list):
        try:
            _options = []
            self.directions = {"nextstep": [], "additionalsteps": [], "remove": 0}

            _splitCount = 0
            if "/" in line:
                _options = line.split("/")
                _splitCount = line.count("/")
                # print("line was split")
                # self.postNeeded = len(_options)
            else:
                _options = [line]

            # for filtering
            _orgItems = _options
            _hasEmpty = "" in _orgItems
            _emptyFront = "" == _orgItems[0]
            _emptyBack = "" == _orgItems[-1]
            # cleans list
            _userWanting = list(filter(lambda item: item != "", _orgItems))
            _combinedLists = selected + _userWanting
            ######

            _validCommand = False
            _tmpNewList = []

            # Condition
            ####
            # split = 2, items = 3
            # i/i/i
            # region 3 Items
            if len(_userWanting) == 3:
                # print("3 sections")
                if _splitCount == 2:
                    # print("Valid command")
                    if len(_userWanting) <= 3:
                        _tmpNewList = _userWanting
                        _validCommand = True
                        self.directions["nextstep"] = [_tmpNewList[0]]
                        self.directions["additionalsteps"] = _tmpNewList[1::]
            # endregion
            # Condition
            ####
            # split = 2, items = 2
            # /i/i  (combine)
            # split = 1, items = 2
            # i/i   (replace)
            # region 2 Items
            elif len(_userWanting) == 2:
                # print("2 sections")
                if _splitCount == 2:
                    # print("valid command")
                    # print("Split count 2")
                    if _emptyFront:
                        if len(_combinedLists) <= 3:
                            _tmpNewList = _combinedLists
                            _validCommand = True
                            self.directions["nextstep"] = [_tmpNewList[0]]
                            self.directions["additionalsteps"] = _tmpNewList[1::]
                    else:
                        # print("Not empty front needs done")
                        if len(_userWanting) <= 3:
                            _tmpNewList = _userWanting
                            _validCommand = True
                            self.directions["additionalsteps"] = _tmpNewList[1::]
                            self.directions["nextstep"] = [_tmpNewList[0]]
                            self.directions["remove"] = self._get_pop(_tmpNewList)
                elif _splitCount == 1:
                    # print("valid command")
                    # print("Split count 1")
                    # /i/i (combine)
                    if _emptyFront:
                        if len(_combinedLists) <= 3:
                            _tmpNewList = _combinedLists
                            _validCommand = True
                            self.directions["nextstep"] = [_tmpNewList[0]]
                            self.directions["additionalsteps"] = _tmpNewList[1::]
                    else:
                        # print("Not empty front needs done")
                        # i/i (replace)
                        if len(_userWanting) <= 3:
                            _tmpNewList = _userWanting
                            _validCommand = True
                            self.directions["nextstep"] = [_tmpNewList[0]]
                            self.directions["additionalsteps"] = _tmpNewList[1::]
                            self.directions["remove"] = self._get_pop(_tmpNewList)
            # endregion
            # Condition
            ####
            # split = 0|1, items = 1
            # /i  (combine)
            # i   (add)
            # region 1 Item
            elif len(_userWanting) == 1:
                # print("1 section")
                # print("User passed 1 item to add")
                if _splitCount == 1:
                    # print("Has split")
                    if _hasEmpty:
                        if _emptyBack:
                            _tmpNewList = _userWanting
                            _validCommand = True
                            self.directions["nextstep"] = _tmpNewList
                            self.directions["remove"] = self._get_pop(_tmpNewList)
                        elif _emptyFront:
                            if len(_combinedLists) <= 3:
                                _tmpNewList = _combinedLists
                                _validCommand = True
                                self.directions["nextstep"] = _tmpNewList
                elif _splitCount == 0:
                    # print("valid command")
                    # print("Has NO split")
                    if len(_combinedLists) <= 3:
                        _tmpNewList = _combinedLists
                        _validCommand = True
                        self.directions["nextstep"] = _tmpNewList
            # endregion
            else:
                return False
        except Exception as e:
            # print(e)
            raise e

        # print("Valid command 1", _validCommand)
        # print("Tmp list to check", _tmpNewList)
        if _validCommand:
            if self._check_current_path(_tmpNewList):
                # print("Current path of program:", selected)
                # print("Path determined to be valid:", _tmpNewList)
                # print("Directions:", self.directions)
                # self._get_next_steps(self.selectedList, _tmpNewList)
                # self.validatedList = _tmpNewList
                # print('*'*10)
                # print("Selected", '/'.join(selected))
                # print("validated", '/'.join(self.validatedList))
                if "/".join(self.selectedList) == "/".join(_tmpNewList):
                    raise Exception("Already at the location")
                else:
                    return True
            else:
                return False
        else:
            return False
