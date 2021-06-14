# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Imports
import json
import os
from nightcappackages.classes.helpers.package_ncp import NightcapPackageInstallerHelper
from nightcappackages.classes.helpers.package_imports import NightcapPackageImports
from nightcappackages.classes.databases.mogo.mongo_modules import MongoModuleDatabase
from nightcappackages.classes.databases.mogo.mongo_packages import MongoPackagesDatabase
from nightcappackages.classes.databases.mogo.mongo_submodules import (
    MongoSubModuleDatabase,
)
from nightcappackages.classes.paths import (
    NightcapPackagesPaths,
)
from nightcapcore import *
import shutil
# endregion


class NightcapPackageInstallerCommand(Command):
    """

    This class is used to install packages

    ...

    Attributes
    ----------
        _package_paths: -> NightcapPackagesPaths
            used for package installation path

        _db: -> MongoPackagesDatabase
            for an instance to the MongoDB database

        _printer: -> Printer
            allows us to print to the console

        _package: -> dict
            the package information that will be used to be installed


    Methods
    -------
        Accessible
        -------
            execute(self) -> None:
                executes the installer



        None Accessible
        -------
            _copy(self, pkt: dict, src: str): -> None
                copies data to the the needed locations

            _imports(self, package: dict = None): -> bool
                gets needed imports for the programs

            _install_import(self, imprt: dict = None, reinstall: bool = False): -> bool
                installs the collected imports
    """

    # region Init
    def __init__(self, package_path: str, clear: bool = False, verbose: bool = False) -> None:
        self._package_paths = NightcapPackagesPaths()
        self._db = MongoPackagesDatabase()
        self.printer = Printer()
        self._package = None
        self._package_path = package_path
        self._clearScreen = clear
        self.verbose = verbose
    # endregion

    # region Execute
    def execute(self) -> None:
        try:
            # unpacking package 
            shutil.copyfile(self._package_path, '/tmp/ncp_installer.ncp')
            shutil.unpack_archive('/tmp/ncp_installer.ncp', '/tmp/ncp_installer/', 'zip') 

            _base_path = ''
            for root, dirs, files in os.walk("/tmp/ncp_installer"):
                for name in dirs:
                    if 'src' not in name:
                        _base_path = os.path.join(root, name)

            try:
                with open(
                    os.path.join(_base_path, "package_info.json")
                ) as json_file:
                    self._package = json.load(json_file)
                if self._clearScreen:
                    ScreenHelper().clearScr()
                # self.printer.print_underlined_header_undecorated("INSTALLING")
                # self.printer.print_formatted_additional(
                #     text="Package: "
                #     + self._package["package_for"]["module"]
                #     + "/"
                #     + self._package["package_for"]["submodule"]
                #     + "/"
                #     + self._package["package_information"]["package_name"]
                # )
            except FileNotFoundError as nf:
                self.printer.print_error(nf)
            except Exception as e:
                self.printer.print_error(e)

            try:
                npuid = self._package["package_information"]["uid"]
            except Exception as e:
                raise Exception("Package signature error")

            try:
                MongoModuleDatabase().module_install(self._package["package_for"]["module"])
            except Exception as e:
                self.printer.print_error(e)
            try:
                MongoSubModuleDatabase().submodule_install(
                    self._package["package_for"]["module"],
                    self._package["package_for"]["submodule"],
                )
            except Exception as e:
                raise e

            _imports = NightcapPackageImports(self._package, verbose=self.verbose).install()
            if _imports:
                if self._db.install(self._package):
                    NightcapPackageInstallerHelper(_base_path, self._package_path, self._package_paths, self._package).copy_installer()
        except Exception as e:
            self.printer.print_error(e)
        finally:
            try:
                os.remove('/tmp/ncp_installer.ncp')
                shutil.rmtree('/tmp/ncp_installer')
            except:
                self.printer.print_error(Exception("Error removing ncp_installer files"))
    # endregion
