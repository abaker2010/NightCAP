# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
from colorama import Fore
from nightcapcore import Printer
from nightcappackages.classes.databases.mogo.mongo_modules import MongoModuleDatabase
from nightcappackages.classes.databases.mogo.mongo_packages import MongoPackagesDatabase
from nightcappackages.classes.databases.mogo.mongo_submodules import MongoSubModuleDatabase
from nightcappackages.classes.paths import NightcapPackagesPaths, NightcapPackagesPathsEnum
from application.classes.helpers.screen.screen_helper import ScreenHelper
from tinydb import TinyDB, Query
from bson.objectid import ObjectId
import shutil

class NightcapPackageUninstaller():
    def __init__(self, package_path: str):
        self.db_packages = TinyDB(NightcapPackagesPaths().generate_path(NightcapPackagesPathsEnum.Databases, ['packages.json']))
        self.printer = Printer()
        self.__package_paths = NightcapPackagesPaths()
        # print("Package path to find", package_path.split("/"))
        self._db =  MongoPackagesDatabase.instance()
        _ex = self._db.check_package_path(package_path.split("/"))
        # print("Package exists", _ex)
        try:
            split_package_path = package_path.split("/")
            # packageExists = self.db_packages.table('packages').search(
            #     (Query()['package_for']['module'] == split_package_path[0])
            #     & (Query()['package_for']['submodule'] == split_package_path[1])
            #     & (Query()['package_information']['package_name'] == split_package_path[2])
            # )
            ##region Working DO NOT REMOVE
            if(_ex == False):
                ScreenHelper().clearScr()
                self.printer.print_formatted_delete(text="Package does not exist")
            else:
                _package = MongoPackagesDatabase.instance().get_package_config(package_path.split("/"))
                self.printer.print_formatted_other(text='Module', optionaltext=split_package_path[0])
                self.printer.print_formatted_other(text='Submodule', optionaltext=split_package_path[1])
                self.printer.print_formatted_other(text='Package', optionaltext=split_package_path[2])
                uconfirm = self._confim_delete(package_path)
                ScreenHelper().clearScr()
                if(uconfirm.lower() == "y"):
                    try:
                        self.printer.print_underlined_header_undecorated(text="UNINSTALLED CONFIRMED")
                        self.printer.print_formatted_other(text='Package', optionaltext=str(_package['_id']), leadingText="~")

                        try:
                            try:
                                print("should delete from table")
                                self._db.delete(ObjectId(_package['_id']))
                                # print("No packages left in module/submodule")
                                MongoSubModuleDatabase.instance().submodule_try_uninstall(split_package_path[0], split_package_path[1])
                                # If there are no submodules then remove the module
                                if(MongoSubModuleDatabase.instance().find_submodules(split_package_path[0]).count() == 0):
                                    # print("remove module")
                                    MongoModuleDatabase.instance().module_try_unintall(split_package_path[0])

                                self._delete(_package)
                                self.printer.print_formatted_check(text="UNINSTALLED", vtabs=1, endingBreaks=1)
                            except Exception as e:
                                self.printer.print_error(exception=e)
                            
                            # self.db_packages.table('packages').remove(doc_ids=[str(_package['_id'])])
                            # self._delete(packageExists[0])
                            
                            # if(self.db_packages.table('packages').contains(Query()['package_information']['uid'] == packageExists[0]["package_information"]["uid"]) is False):
                                

                            #     packages = self.db_packages.table('packages').search(
                            #             (Query()['package_for']['module'] == split_package_path[0])
                            #             & (Query()['package_for']['submodule'] == split_package_path[1])
                            #         )

                            #     # If there are no packages then remove the submodule
                            #     if(len(packages) == 0):
                            #         # print("No packages left in module/submodule")
                            #         MongoSubModuleDatabase.instance().submodule_try_uninstall(split_package_path[0], split_package_path[1])
                            #         # If there are no submodules then remove the module
                            #         if(MongoSubModuleDatabase.instance().find_submodules(split_package_path[0]).count() == 0):
                            #             # print("remove module")
                            #             MongoModuleDatabase.instance().module_try_unintall(split_package_path[0])

                            #     self.printer.print_formatted_check(text="UNINSTALLED", vtabs=1, endingBreaks=1)

                        except Exception as e:
                            self.printer.print_error(exception=e)
                    except  Exception as e:
                        self.printer.print_error(exception=e)
            ##endregion 

        except Exception as e:
            raise Exception("Package not found")

    def _confim_delete(self, package_path: str):
        return self.printer.input("Are you sure you want to uninstall? [y/n]: ", questionColor=Fore.RED)
       

    def _delete(self, pkt: dict):
        _path = self.__package_paths.generate_path(NightcapPackagesPathsEnum.PackagesBase, [pkt['package_for']['module'],pkt['package_for']['submodule'], pkt['package_information']['package_name']])
        print("Path to delete the installed file", _path)
        try:
            shutil.rmtree(_path)
            self.printer.print_formatted_check(text="Deleted Files")
        except OSError as e:
            self.printer.print_error(exception=Exception("Error: %s - %s." % (e.filename, e.strerror)))
