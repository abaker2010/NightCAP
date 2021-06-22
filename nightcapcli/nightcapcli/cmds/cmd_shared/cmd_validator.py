# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Import
from typing import Any
from nightcappackages.classes.databases.mogo import *

# endregion


class NightcapCLIOptionsValidator(object):
    """
    This class is used to help validate user input to the console

    ...

    Attributes
    ----------

        modules_db: -> MongoModuleDatabase
            Instance of the MongoModuleDatabase

        submodules_db: -> MongoSubModuleDatabase
            Instance of the MongoSubModuleDatabase

        packages_db: -> MongoPackagesDatabase
            Instance of the MongoPackagesDatabase

        newSelectedList: -> list
            New selected list that was generated based on the users input that will be used for the [<T>][<T>] in the console

        isvalid: -> bool
            Is used to help validate the users input

        pkg_conf: -> dict
            This is the selected package configuration if any

    Methods
    -------
        Accessible
        -------
            get_package_config(self, path: list): -> dict
                Returns a packages configuration information

        None Accessible
        -------
            _check_module_types(self, path: list): -> bool
                Returns a bool based on if the module exists or not

            _check_sub_module(self, path: list): -> bool
                Returns a bool based on if the submodule exists or not

            _check_packages(self, selected): -> bool
                Returns a bool based on if the package exists or not

            _check_current_path(self, path: list): -> bool
                Returns a bool based on the current path

            _validate(self, line: str, selected: list): -> bool
                Reutns a bool based on if the users input is vaild or not


    """

    # region Init
    def __init__(self, options, selectedList) -> None:
        self.modules_db = MongoModuleDatabase()
        self.submodules_db = MongoSubModuleDatabase()
        self.packages_db = MongoPackagesDatabase()
        self.newSelectedList = []
        self.isvalid = self._validate(options, selectedList)
        self.pkg_conf = None

    # endregion

    # region Package Configuration
    def get_package_config(self, path: list) -> Any:
        self.pkg_conf = self.packages_db.get_package_config(path)
        # print("Found pkg config", self.pkg_conf)
        return self.pkg_conf

    # endregion

    # region Check Sub/Module/Packages Types
    def _check_module_types(self, path: list) -> bool:
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

    # endregion

    # region Check Current Path
    def _check_current_path(self, path: list) -> bool:
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

    # endregion

    # region Validate Input
    def _validate(self, line: str, selected: list) -> bool:

        try:
            _options = []
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
            _cleanedItems = list(filter(lambda item: item != "", _orgItems))
            _combined = selected + _cleanedItems
            ######

            _validCommand = False
            _tmpNewList = []

            # Condition
            ####
            # split = 2, items = 3
            # i/i/i
            if len(_cleanedItems) == 3:
                # print("3 sections")
                if _splitCount == 2:
                    # print("Valid command")
                    if len(_cleanedItems) <= 3:
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
                    if _emptyFront:
                        if len(_combined) <= 3:
                            _tmpNewList = _combined
                            _validCommand = True
                    else:
                        # print("Not empty front needs done")
                        if len(_cleanedItems) <= 3:
                            _tmpNewList = _cleanedItems
                            _validCommand = True
                elif _splitCount == 1:
                    # print("valid command")
                    # print("Split count 1")
                    if _emptyFront:
                        if len(_combined) <= 3:
                            _tmpNewList = _combined
                            _validCommand = True
                    else:
                        # print("Not empty front needs done")
                        if len(_cleanedItems) <= 3:
                            _tmpNewList = _cleanedItems
                            _validCommand = True
            # Condition
            ####
            # split = 0|1, items = 1
            # /i  (combine)
            # i   (add)
            elif len(_cleanedItems) == 1:
                # print("1 section")
                if _splitCount == 1:
                    # print("valid command")
                    if _hasEmpty:
                        if _emptyBack:
                            _tmpNewList = _cleanedItems
                            _validCommand = True
                        elif _emptyFront:
                            if len(_combined) <= 3:
                                _tmpNewList = _combined
                                _validCommand = True
                elif _splitCount == 0:
                    # print("valid command")
                    if len(_combined) <= 3:
                        _tmpNewList = _combined
                        _validCommand = True
            else:
                return False

            # print("Valid command 1", _validCommand)
            # print("Tmp list to check", _tmpNewList)
            if _validCommand:
                if self._check_current_path(_tmpNewList):
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

    # endregion
