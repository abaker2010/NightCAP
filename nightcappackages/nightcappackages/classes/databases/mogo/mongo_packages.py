# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Import
from typing import Any
from bson.objectid import ObjectId
from colorama.ansi import Fore, Style
from nightcapcore.singleton.singleton import Singleton
from nightcappackages.classes.databases.mogo.connections.mongo_operation_connector import (
    MongoDatabaseOperationsConnection,
)
from nightcappackages.classes.paths.pathsenum import NightcapPackagesPathsEnum
from nightcappackages.classes.paths.paths import NightcapPackagesPaths
from pymongo.cursor import Cursor

# endregion


class MongoPackagesDatabase(MongoDatabaseOperationsConnection, metaclass=Singleton):
    """

    This class is used to interact with the packages database

    ...

    Attributes
    ----------
        _db: -> MongoClient
            MongoClient

    Methods
    -------
        Accessible
        -------
            create(self, pkg: dict): -> None
                Allows the users to insert an entry

            read(self): -> Any
                reads the db

            delete(self, puid: ObjectId): -> None
                delete an entry

            get_package_run_path(self, pkg_config: dict = None): -> str
                get the package run path for the system

            check_package_path(self, path: list): -> bool
                check if the package exists

            package_params(self, selected: list): -> None
                prints out the package params

            get_package_config(self, parentmodules: list): -> dict
                gets the package configuration

            packages(self, parentmodules: list, isDetailed: bool = False): -> Any
                returns a list of packages if any

            find_package(self, package: dict = None): -> dict
                trys to find a package

            find_packages(self, module: str = None, submodule: str = None): -> dict
                tries to find many packages

            install(self, package: dict = None): -> bool
                will try to install a new package

            get_all_packages(self): -> dict
                returns all of the packages installed
    """

    # region Init
    def __init__(self) -> None:
        MongoDatabaseOperationsConnection.__init__(self)
        self._db = self.client[self.conf.config["MONGOSERVER"]["db_name"]]["packages"]

    # endregion

    # region Create
    def create(self, pkg: dict) -> None:
        self._db.insert_one(pkg)

    # endregion

    # region Read
    def read(self) -> Cursor:
        return self._db.find()

    # endregion

    # region Update
    def update(self) -> None:
        pass

    # endregion

    # region Delete
    def delete(self, puid: ObjectId) -> None:
        self._db.delete_one({"_id": puid})

    # endregion

    def drop(self) -> None:
        self._db.drop()
        

    # region Get package run path
    def get_package_run_path(self, pkg_config: dict = None):
        _path = NightcapPackagesPaths().generate_path(
            NightcapPackagesPathsEnum.PackagesBase,
            [
                pkg_config["package_for"]["module"],
                pkg_config["package_for"]["submodule"],
                pkg_config["package_information"]["package_name"],
                pkg_config["package_information"]["entry_file"],
            ],
        )
        return _path

    # endregion

    # region Check package path
    def check_package_path(self, path: list) -> bool:
        _module = path[0]
        _submodule = path[1]
        _package = path[2]
        _ = self._db.find_one(
            {
                "$and": [
                    {
                        "package_for.module": {"$eq": _module},
                        "package_for.submodule": {"$eq": _submodule},
                        "package_information.package_name": {"$eq": _package},
                    }
                ]
            }
        )
        return False if _ == None else True

    # endregion

    # region Package params
    def package_params(self, selected: list) -> Cursor:
        _module = selected[0]
        _submodule = selected[1]
        _package = selected[2]
        print("Finding package params")
        print(_module)
        print(_submodule)
        print(_package)
        # __package__
        _npackages = self._db.find(
            {
                "$and": [
                    {
                        "package_for.module": {"$eq": _module},
                        "package_for.submodule": {"$eq": _submodule},
                    }
                ]
            }
        )

    # endregion

    # region Get package config
    def get_package_config(self, parentmodules: list) -> Any:
        _module = parentmodules[0]
        _submodule = parentmodules[1]
        _package = parentmodules[2]
        return self._db.find_one(
            {
                "$and": [
                    {
                        "package_for.module": {"$eq": _module},
                        "package_for.submodule": {"$eq": _submodule},
                        "package_information.package_name": {"$eq": _package},
                    }
                ]
            }
        )

    # endregion

    # region Get Options Packages
    def packages(self, parentmodules: list, isDetailed: bool = False) -> list:
        _module = parentmodules[0]
        _submodule = parentmodules[1]
        _npackages = self._db.find(
            {
                "$and": [
                    {
                        "package_for.module": {"$eq": _module},
                        "package_for.submodule": {"$eq": _submodule},
                    }
                ]
            }
        )

        npackages = []
        for _npkg in _npackages:
            npackages.append(_npkg)

        if isDetailed:
            _packages = list(map(lambda v: v, npackages))
            packages = []
            h = """%s (%s) %s|%s %s %s| %s""" % (
                (Fore.GREEN + "Package Name" + Fore.CYAN),
                ("Version"),
                (Fore.BLUE),
                (Fore.CYAN),
                ("Developer"),
                (Fore.BLUE),
                (Fore.YELLOW + "Details" + Style.RESET_ALL),
            )
            h1 = Fore.CYAN + "-" * len(h) + Style.RESET_ALL
            packages.append("\n")
            packages.append(h)
            packages.append(h1)
            for pkt in _packages:
                h1 = pkt["package_information"]["package_name"]
                h2 = pkt["package_information"]["details"]
                h3 = pkt["package_information"]["version"]
                h4 = pkt["author_info"]["creator"]
                p = """\t%s (%s) %s|%s %s %s| %s""" % (
                    (Fore.GREEN + h1 + Fore.CYAN),
                    (h3),
                    (Fore.BLUE),
                    (Fore.CYAN),
                    (h4),
                    (Fore.BLUE),
                    (Fore.YELLOW + h2 + Style.RESET_ALL),
                )
                packages.append(p)
        else:
            packages = list(
                map(lambda v: v["package_information"]["package_name"], list(npackages))
            )
        return packages

    # endregion

    # region Find Package
    def find_package(self, package: dict = None) -> Any:
        return self._db.find_one(package)

    # endregion

    # region Find Packages
    def find_packages(self, module: str = None, submodule: str = None) -> Cursor:
        return self._db.find(
            {
                "$and": [
                    {
                        "package_for.module": {"$eq": module},
                        "package_for.submodule": {"$eq": submodule},
                    }
                ]
            }
        )

    # endregion

    # region Install
    def install(self, package: dict = None) -> bool:
        _puid = package["package_information"]["uid"]
        if self.find_package(package) == None:
            try:
                self.create(package)
                return True
            except Exception as e:
                self.printer.print_error(e)
                return False
        else:
            self.printer.print_formatted_additional(text="Package Already Installed (Not Replacing)", textColor=Fore.LIGHTRED_EX, endingBreaks=1)
            return False

    # endregion

    # region get all packages
    def get_all_packages(self) -> Cursor:
        return self.read()

    # endregion
