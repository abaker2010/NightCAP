# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Imports
import json
import os
from typing import cast, final
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

class NightcapPackageImports(object):
    def __init__(self, imports, verbose: bool = True) -> None:
        super().__init__()
        self.imports = imports
        self.printer = Printer()
        self.verbose = verbose
    # def install(self):

    def install(self):
        return self._imports(self.imports)


     # region Collect Imports
    def _imports(self, package: dict = None):
        try:
            _imports = list(package["package_information"]["imports"])

            if _imports != []:
                if self.verbose:
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
                            if self.verbose:
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
                                if self.verbose:
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
                                agree = self.printer.input("Override package? (Y/n)")
                                if agree:
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
                                    agree = self.printer.input("Continue? (Y/n)")
                                    
                                    if agree:
                                        # print("override package")
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
                # print()

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
        if self.verbose:
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
