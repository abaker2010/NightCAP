# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Imports
import json
import os
from nightcappackages.classes.databases.mogo.mongo_modules import MongoModuleDatabase
from nightcappackages.classes.databases.mogo.mongo_packages import MongoPackagesDatabase
from nightcappackages.classes.databases.mogo.mongo_submodules import (
    MongoSubModuleDatabase,
)
from nightcappackages.classes.paths import (
    NightcapPackagesPathsEnum,
    NightcapPackagesPaths,
)
from nightcapcore import *
from colorama import Fore, Style
import sys
import subprocess
import pkg_resources
import shutil
import errno

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
    def __init__(self, package_path: str) -> None:
        self._package_paths = NightcapPackagesPaths()
        self._db = MongoPackagesDatabase()
        self.printer = Printer()
        self._package = None
        self._package_path = package_path

    # endregion

    # region Execute
    def execute(self) -> None:
        try:
            with open(
                os.path.join(self._package_path, "package_info.json")
            ) as json_file:
                self._package = json.load(json_file)
            ScreenHelper().clearScr()
            self.printer.print_underlined_header_undecorated("INSTALLING")
            self.printer.print_formatted_additional(
                text="Package: "
                + self._package["package_for"]["module"]
                + "/"
                + self._package["package_for"]["submodule"]
                + "/"
                + self._package["package_information"]["package_name"]
            )
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

        _imports = self._imports(self._package)
        if _imports:
            if self._db.install(self._package):
                self._copy(self._package, self._package_path)
                self.printer.print_formatted_check(
                    text="INSTALLED", leadingTab=1, endingBreaks=1, leadingBreaks=1
                )
            else:
                self.printer.print_formatted_delete(text="Could not copy files")

    # endregion

    # region Copy
    def _copy(self, pkt: dict, src: str):
        _path = self._package_paths.generate_path(
            NightcapPackagesPathsEnum.PackagesBase,
            [
                pkt["package_for"]["module"],
                pkt["package_for"]["submodule"],
                pkt["package_information"]["package_name"],
            ],
        )
        try:
            shutil.copytree(src, _path)
        except OSError as e:
            # If the error was caused because the source wasn't a directory
            if e.errno == errno.ENOTDIR:
                shutil.copy(src, _path)
            else:
                self.printer.print_formatted_delete(
                    text="Package not copied. Error: %s" % str(e)
                )

    # endregion

    # region Collect Imports
    def _imports(self, package: dict = None):
        try:
            _imports = list(package["package_information"]["imports"])

            if _imports != []:
                self.printer.print_underlined_header_undecorated(
                    "Installing Required Packages"
                )

                installed_packages_dict = {}
                installed_packages = pkg_resources.working_set
                for i in installed_packages:
                    installed_packages_dict[i.key] = {"version": i.version}

                for pkg in _imports:

                    _ver = None if pkg["version"] == "" else pkg["version"]

                    if pkg["package"] not in installed_packages_dict.keys():
                        try:
                            _success = self._install_import(pkg)
                            if _success:
                                self.printer.print_formatted_check(
                                    text="Installed", leadingTab=3
                                )
                            else:
                                self.printer.print_formatted_delete(
                                    text="Not Installed", leadingTab=3
                                )
                        except Exception as e:
                            self.printer.print_error(e)
                    else:
                        if pkg["version"] != "":
                            _ver = str(
                                installed_packages_dict[pkg["package"]]["version"]
                            )
                            _rver = str(pkg["version"])
                            if _rver == _ver:
                                # print("version required is the same/older")
                                self.printer.print_formatted_check(
                                    text="Installed: " + pkg["package"],
                                    optionaltext=str(pkg["version"]),
                                )
                            elif _rver != _ver:
                                # print("version required is the same/older")
                                self.printer.print_formatted_additional(
                                    text="Collison: " + pkg["package"]
                                )
                                self.printer.print_formatted_additional(
                                    text="Required Version",
                                    optionaltext=str(pkg["version"]),
                                    leadingTab=3,
                                )
                                self.printer.print_formatted_additional(
                                    text="Installed Version",
                                    optionaltext=str(
                                        installed_packages_dict[pkg["package"]][
                                            "version"
                                        ]
                                    ),
                                    leadingTab=3,
                                )
                                agree = input(
                                    Fore.LIGHTGREEN_EX
                                    + "\n\t\tOverride package? (Y/n): "
                                    + Style.RESET_ALL
                                ).lower()
                                yes = self._db.conf.config.get(
                                    "NIGHTCAPCORE", "yes"
                                ).split()
                                if agree in yes:
                                    self.printer.print_formatted_delete(
                                        text="(Confirm) This will replace the currently installed pip package."
                                    )
                                    self.printer.print_formatted_additional(
                                        text=(
                                            "Existing: %s :: %s, Replacement: %s :: %s"
                                        )
                                        % (
                                            str(pkg["package"]),
                                            str(
                                                installed_packages_dict[pkg["package"]][
                                                    "version"
                                                ]
                                            ),
                                            str(pkg["package"]),
                                            str(pkg["version"]),
                                        )
                                    )
                                    agree = input(
                                        Fore.RED
                                        + "\n\t\tContinue? (Y/n): "
                                        + Style.RESET_ALL
                                    ).lower()
                                    if agree in yes:
                                        print("override package")
                                        _success = self._install_import(
                                            pkg, reinstall=True
                                        )
                                        if _success:
                                            self.printer.print_formatted_check(
                                                text="Installed", leadingTab=3
                                            )
                                        else:
                                            self.printer.print_formatted_delete(
                                                text="Not Installed", leadingTab=3
                                            )
                                    else:
                                        return False

                            else:
                                print("version required is greater")
                print()

            return True
        except Exception as e:
            self.printer.print_error(e)
            return False

    # endregion

    # region install imports
    def _install_import(self, imprt: dict = None, reinstall: bool = False):
        _pkg = None
        _ver = "Any" if imprt["version"] == "" else imprt["version"]
        if imprt["version"] == "":
            _pkg = imprt["package"]
        else:
            _pkg = imprt["package"] + "==" + imprt["version"]
        self.printer.print_formatted_additional(
            text="Installing",
            optionaltext=imprt["package"] + " ver. " + _ver,
            textColor=Fore.LIGHTYELLOW_EX,
        )

        try:
            python = sys.executable
            if reinstall:
                subprocess.check_call(
                    [python, "-m", "pip", "install", _pkg, "--force-reinstall"],
                    stdout=subprocess.DEVNULL,
                )
            else:
                subprocess.check_call(
                    [python, "-m", "pip", "install", "-Iv", _pkg],
                    stdout=subprocess.DEVNULL,
                )

            return True
        except Exception as e:
            self.printer.print_error(e)
            return False

    # endregion
