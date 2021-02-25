# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
from colorama import Fore
from nightcapcore.printers.print import Printer
from nightcappackages.classes.modules import NightcapModules
from nightcappackages.classes.submodules import NightcapSubModule
from ..paths import NightcapPackagesPathsEnum, NightcapPackagesPaths
from application.classes.helpers.screen.screen_helper import ScreenHelper
from tinydb import TinyDB, Query
import shutil

class NightcapPackageUninstaller():
    def __init__(self, package_path: str):
        self.db_packages = TinyDB(NightcapPackagesPaths().generate_path(NightcapPackagesPathsEnum.Databases, ['packages.json']))
        self.printer = Printer()
        self.__package_paths = NightcapPackagesPaths()
        
        try:
            split_package_path = package_path.split("/")
            packageExists = self.db_packages.table('packages').search(
                (Query()['package_for']['module'] == split_package_path[0])
                & (Query()['package_for']['submodule'] == split_package_path[1])
                & (Query()['package_information']['package_name'] == split_package_path[2])
            )
            ##region Working DO NOT REMOVE
            if(len(packageExists) == 0):
                ScreenHelper().clearScr()
                self.printer.print_formatted_delete(text="Package does not exist")
            else:
                uconfirm = self._confim_delete(package_path)
                ScreenHelper().clearScr()
                if(uconfirm.lower() == "y"):
                    self.printer.print_underlined_header_undecorated(text="UNINSTALLED CONFIRMED")
                    packageExists[0].doc_id
                    try:
                        self.db_packages.table('packages').remove(doc_ids=[packageExists[0].doc_id])
                        self._delete(packageExists[0])
                        
                        if(self.db_packages.table('packages').contains(Query()['package_information']['uid'] == packageExists[0]["package_information"]["uid"]) is False):
                            

                            packages = self.db_packages.table('packages').search(
                                    (Query()['package_for']['module'] == split_package_path[0])
                                    & (Query()['package_for']['submodule'] == split_package_path[1])
                                )

                            # If there are no packages then remove the submodule
                            if(len(packages) == 0):
                                # print("No packages left in module/submodule")
                                NightcapSubModule().submodule_try_uninstall(split_package_path[0], split_package_path[1])
                                # If there are no submodules then remove the module
                                if(len(NightcapSubModule().find_submodules(split_package_path[0])) == 0):
                                    # print("remove module")
                                    NightcapModules().module_try_unintall(split_package_path[0])

                            self.printer.print_formatted_check(text="UNINSTALLED", vtabs=1, endingBreaks=1)

                    except Exception as e:
                        self.printer.print_error(exception=e)
            ##endregion 

        except Exception as e:
            raise Exception("Package not found")

    def _confim_delete(self, package_path: str):
        return self.printer.input("Are you sure you want to uninstall: %s? [y/n]: " % (package_path), questionColor=Fore.RED)
       

    def _delete(self, pkt: dict):
        _path = self.__package_paths.generate_path(NightcapPackagesPathsEnum.PackagesBase, [pkt['package_for']['module'],pkt['package_for']['submodule'], pkt['package_information']['package_name']])
        try:
            shutil.rmtree(_path)
            self.printer.print_formatted_check(text="Deleted Files")
        except OSError as e:
            self.printer.print_error(exception=Exception("Error: %s - %s." % (e.filename, e.strerror)))
