# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Imports
import os
import glob
from colorama import Fore
from nightcapcore import Printer
from nightcappackages.classes.databases.mogo.mongo_modules import MongoModuleDatabase
from nightcappackages.classes.databases.mogo.mongo_packages import MongoPackagesDatabase
from nightcappackages.classes.databases.mogo.mongo_submodules import (
    MongoSubModuleDatabase,
)
from nightcappackages.classes.paths import (
    NightcapPackagesPaths,
    NightcapPackagesPathsEnum,
)
from bson.objectid import ObjectId
from nightcapcore import *
import shutil

# endregion


class NightcapPackageUninstallerCommand(Command):
    """

    This class is used to uninstall packages

    ...

    Attributes
    ----------
        printer: -> Printer
            allows us to print to the console

        __package_paths: -> NightcapPackagesPaths
            the package installation path

        _db: -> MongoPackagesDatabase
            allows us to remove the entry for the package from the database

    Methods
    -------
        Accessible
        -------
            execute(self): -> None
                run uninstall commands



        None Accessible
        -------
            _confim_delete(self, package_path: str): -> None
                Confirms deletion

            _delete(self, pkt: dict): -> None
                tries to uninstalls the package

    """

    # region Init
    def __init__(self, package_path: str, override: bool = False) -> None:
        self.printer = Printer()
        self.__package_paths = NightcapPackagesPaths()
        self._package_path = package_path
        self._split_package_path = package_path.split("/")
        self._db = MongoPackagesDatabase()
        self._ex = self._db.check_package_path(package_path.split("/"))
        self._override = override

    # endregion

    # region Execute
    def execute(self) -> None:
        try:
            if self._ex == False:
                raise Exception("Package does not exist")
            else:
                _package = MongoPackagesDatabase().get_package_config(
                    self._package_path.split("/")
                )
                if self._override:
                    uconfirm = True
                else:
                    uconfirm = self._confim_delete(self._package_path)
                if uconfirm: 
                    self.printer.print_header_w_option("Trying to Uninstall", self._package_path)

                    self.printer.item_1("ID", str(_package["_id"]), leadingText='[~]', seperator=" : ")

                    #region Removing Package
                    try:

                        #region Deleting Package from DB
                        self._db.delete(ObjectId(_package["_id"]))
                        #endregion

                        #region Deleteing Files
                        self._delete(_package)
                        #enregion

                        #region Removing Submodules
                        MongoSubModuleDatabase().submodule_try_uninstall(
                            self._split_package_path[0], self._split_package_path[1]
                        )
                        #endregion

                        #region Removing Modules
                        if (
                                MongoSubModuleDatabase()
                                .find_submodules(self._split_package_path[0])
                                .count()
                                == 0
                            ):
                            MongoModuleDatabase().module_try_unintall(
                                    self._split_package_path[0]
                                )
                        #endregion

                        self._rm_installer(self._split_package_path)
                    except Exception as e:
                        raise e
                    #endregion

                else:
                    raise Exception("User Cancled Uninstall")
            self.printer.print_formatted_check(
                                    text="UNINSTALLED",
                                    vtabs=1,
                                    endingBreaks=1,
                                    leadingTab=1,
                                )

        except Exception as e:
            raise e

    # endregion

    # region Copy
    def _rm_installer(self, installer: list):
        _path = self.__package_paths.generate_path(
            NightcapPackagesPathsEnum.Installers,[
                "-".join([
            installer[0],
            installer[1],
            installer[2], '*'])
            ]
        )

        _files = glob.glob(_path)
        for f in _files:
            try:
                os.remove(f)
            except Exception as e:
                self.printer.print_error(e)


    # endregion 

    # region Confirm Delete
    def _confim_delete(self, package_path: str):
        return self.printer.input(
            "Are you sure you want to uninstall? [Y/n]: ", questionColor=Fore.RED
        )

    # endregion

    # region Delete
    def _delete(self, pkt: dict):
        _path = self.__package_paths.generate_path(
            NightcapPackagesPathsEnum.PackagesBase,
            [
                pkt["package_for"]["module"],
                pkt["package_for"]["submodule"],
                pkt["package_information"]["package_name"],
            ],
        )
        # print("Path to delete the installed file", _path)
        try:
            shutil.rmtree(_path)
            self.printer.print_formatted_check(text="Deleted Files")
        except OSError as e:
            self.printer.print_error(
                Exception("Error: %s - %s." % (e.filename, e.strerror))
            )

    # endregion
