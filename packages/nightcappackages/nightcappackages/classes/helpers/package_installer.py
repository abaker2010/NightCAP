# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
from nightcappackages.classes.databases.mogo.mongo_modules import MongoModuleDatabase
from nightcappackages.classes.databases.mogo.mongo_packages import MongoPackagesDatabase
from nightcappackages.classes.databases.mogo.mongo_submodules import MongoSubModuleDatabase
from nightcappackages.classes.paths import NightcapPackagesPathsEnum, NightcapPackagesPaths
from application.classes.helpers.screen.screen_helper import ScreenHelper
from nightcapcore import *
from tinydb import TinyDB, Query
from colorama import Fore, Style
import sys
import subprocess
import pkg_resources
import shutil
import errno

class NightcapPackageInstaller():
    def __init__(self, package: dict, package_path: str):
        self.__package_paths = NightcapPackagesPaths()
        self.db_packages = TinyDB(NightcapPackagesPaths().generate_path(NightcapPackagesPathsEnum.Databases, ['packages.json']))
        self.printer = Printer()

        try:
            npuid = package['package_information']['uid']
        except Exception as e:
            raise Exception("Package signature error")

        try:
            
            MongoModuleDatabase.instance().module_install(package['package_for']['module'])
        except  Exception as e:
            self.printer.print_error(exception=e)
            # self.output.output("Error with module: " + str(e), level=6)
        try:
            MongoSubModuleDatabase.instance().submodule_install(package['package_for']['module'], package['package_for']['submodule'])
        except  Exception as e:
            self.printer.print_error(exception=e)
            # self.output.output("Error with submodule: " + str(e), level=6)
            exit
    
    #region Checking for package in db
        MongoPackagesDatabase.instance().install(package)
        # packageExists = self.db_packages.table('packages').search(
        #     (Query()['package_information']['uid'] == npuid)
        # )

        # if(len(packageExists) == 0):
        #     try:
        #         _imports = dict(package['package_information']['imports'])
        #         if _imports:   
        #             self.printer.print_underlined_header_undecorated(text="Collecting packages")
        #             _installed = {}
        #             for pkg in pkg_resources.working_set:
        #                 _installed[pkg.key] = pkg.version
                    
        #             for pkg, ver in _imports.items():
        #                 _pkg_iv = pkg + "==" + ver
        #                 if pkg in _installed.keys():
        #                     self.printer.print_formatted_check(text="Installed" + _pkg_iv)
        #                 else:
                            
        #                     self.printer.print_formatted_additional(text="Installing" + _pkg_iv)
        #                     try:
        #                         python = sys.executable
        #                         subprocess.check_call(['sudo', python, '-m', 'pip', 'install', '-Iv', _pkg_iv], stdout=subprocess.DEVNULL)
        #                     except subprocess.CalledProcessError as e:
        #                         if e.returncode == 1:
        #                             self.printer.print_formatted_delete(text="Permission Denied: Please reopen the program as an administrator")
        #                         else:
        #                             self.printer.print_formatted_delete(text="command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
                
        #     except Exception as imperro:
        #         self.printer.print_error(exception=imperro)
            
        #     self.db_packages.table('packages').insert(package)
        #     self.printer.print_formatted_additional(text="Installing source code")
        #     self._copy(package, package_path)
        #     self.printer.print_formatted_check(text="Installed", endingBreaks=1)
        # else:
        #     self.printer.print_error(Exception("Error package already exists. Uninstall the package first"))
        #     # self.output.output("Error package already exists. Uninstall the package first", level=6)
        #endregion

    def _copy(self, pkt: dict, src: str): 
        _path = self.__package_paths.generate_path(NightcapPackagesPathsEnum.PackagesBase, [pkt['package_for']['module'],pkt['package_for']['submodule'], pkt['package_information']['package_name']])
        try:
            shutil.copytree(src, _path)
        except OSError as e:
            # If the error was caused because the source wasn't a directory
            if e.errno == errno.ENOTDIR:
                shutil.copy(src, _path)
            else:
                self.printer.print_formatted_delete(text='Package not copied. Error: %s' % str(e))
                # self.output.output('Package not copied. Error: %s' % str(e), level=6)