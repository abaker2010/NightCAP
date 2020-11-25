# Copyright 2020 by Aarom Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
from nightcappackages.classes.submodules import NightcapSubModule
from nightcappackages.classes.modules import NightcapModules
from ..packages import NightcapPackagesPathsEnum, NightcapPackagesPaths
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
        print("installer for packages")
        self.__package_paths = NightcapPackagesPaths()
        self.db_packages = TinyDB(NightcapPackagesPaths().generate_path(NightcapPackagesPathsEnum.Databases, ['packages.json']))
        self.output = NightcapCoreConsoleOutput()

        try:
            npuid = package['package_information']['uid']
        except Exception as e:
            raise Exception("Package signature error")

        try:
            NightcapModules().module_install(package['package_for']['module'])
        except  Exception as e:
            self.output.output("Error with module: " + str(e), level=6)
        try:
            NightcapSubModule().submodule_install(package['package_for']['module'], package['package_for']['submodule'])
        except  Exception as e:
            self.output.output("Error with submodule: " + str(e), level=6)
            exit
    
    #region Checking for package in db
        packageExists = self.db_packages.table('packages').search(
            (Query()['package_information']['uid'] == npuid)
        )

        if(len(packageExists) == 0):
            try:
                _imports = dict(package['package_information']['imports'])
                if _imports:   
                    self.output.output("Collecting packages")
                    self.output.output("-"*len("Collecting packages"))
                    _installed = {}
                    for pkg in pkg_resources.working_set:
                        _installed[pkg.key] = pkg.version
                    
                    for pkg, ver in _imports.items():
                        _pkg_iv = pkg + "==" + ver
                        if pkg in _installed.keys():
                            self.output.output("[+] Installed: " + _pkg_iv)
                        else:
                            self.output.output("\t[!] Installing: " + _pkg_iv, color=Fore.YELLOW)
                            # add the -Iv flag 
                            try:
                                python = sys.executable
                                subprocess.check_call(['sudo', python, '-m', 'pip', 'install', '-Iv', _pkg_iv], stdout=subprocess.DEVNULL)
                            except subprocess.CalledProcessError as e:
                                if e.returncode == 1:
                                    self.output.output("Permission Denied: Please reopen the program as an administrator", level=5)
                                else:
                                    self.output.output("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output), level=6)
                else:
                    print("No packages to import/download")
                    

            except Exception as imperro:
                self.output.output(str(imperro), level=6)
            
            self.db_packages.table('packages').insert(package)
            self.output.output("[-] Installing source code")
            self._copy(package, package_path)
            self.output.output("[+] Installed\n", level=1)
        else:
            self.output.output("Error package already exists. Uninstall the package first", level=6)
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
                self.output.output('Package not copied. Error: %s' % str(e), level=6)