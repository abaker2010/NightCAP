# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
#region Imports
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
#endregion

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
    #region Init
    def __init__(self, package_path: str) -> None:
        self.printer = Printer()
        self.__package_paths = NightcapPackagesPaths()
        self._package_path = package_path
        self._db = MongoPackagesDatabase()
        self._ex = self._db.check_package_path(package_path.split("/"))
    #endregion

    #region Execute
    def execute(self) -> None:
        try:
            split_package_path = self._package_path.split("/")
            if self._ex == False:
                ScreenHelper().clearScr()
                self.printer.print_formatted_delete(text="Package does not exist")
            else:
                _package = MongoPackagesDatabase().get_package_config(
                    self._package_path.split("/")
                )
                self.printer.print_formatted_other(
                    "Module", split_package_path[0]
                )
                self.printer.print_formatted_other(
                    "Submodule", split_package_path[1]
                )
                self.printer.print_formatted_other(
                    "Package", split_package_path[2]
                )
                uconfirm = self._confim_delete(self._package_path)
                ScreenHelper().clearScr()
                if uconfirm.lower() == "y":
                    try:
                        self.printer.print_underlined_header_undecorated("UNINSTALLED CONFIRMED")
                        self.printer.print_formatted_other(
                            "Package",
                            str(_package["_id"]),
                            leadingText="~",
                        )

                        try:
                            try:
                                self._db.delete(ObjectId(_package["_id"]))
                                MongoSubModuleDatabase().submodule_try_uninstall(
                                    split_package_path[0], split_package_path[1]
                                )
                                # If there are no submodules then remove the module
                                if (
                                    MongoSubModuleDatabase()
                                    .find_submodules(split_package_path[0])
                                    .count()
                                    == 0
                                ):
                                    MongoModuleDatabase().module_try_unintall(
                                        split_package_path[0]
                                    )
                                self._delete(_package)
                                self.printer.print_formatted_check(
                                    text="UNINSTALLED",
                                    vtabs=1,
                                    endingBreaks=1,
                                    leadingTab=1,
                                )
                            except Exception as e:
                                self.printer.print_error(e)

                        except Exception as e:
                            self.printer.print_error(e)
                    except Exception as e:
                        self.printer.print_error(e)

        except Exception as e:
            raise Exception("Package not found")
    #endregion

    #region Confirm Delete
    def _confim_delete(self, package_path: str):
        return self.printer.input(
            "Are you sure you want to uninstall? [y/n]: ", questionColor=Fore.RED
        )
    #endregion

    #region Delete
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
    #endregion