# Copyright 2020 by Aarom Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
from tinydb import TinyDB, Query
from colorama import Fore, Style
from nightcapcore import *
from .paths import NightcapPackagesPathsEnum, NightcapPackagesPaths

class NightcapPackages(): 
    def __init__(self):
        self.__package_paths = NightcapPackagesPaths()
        self.db_packages = TinyDB(NightcapPackagesPaths().generate_path(NightcapPackagesPathsEnum.Databases, ['packages.json']))
        self.output = NightcapCoreConsoleOutput()

    #region Find Packages
    def find_packages(self, module: str, submodule: str):
        _packages = list(map(lambda v : v, self.db_packages.table('packages').search(
            (Query()['package_for']['module'] == module) & (Query()['package_for']['submodule'] == submodule)
        )))

        return _packages

    #endregion

    #region Get Packages
    def packages(self,parentmodules: list,isDetailed: bool = False):
        npackages = self.db_packages.table('packages').search(
            (Query()['package_for']['module'] == parentmodules[0])
            & (Query()['package_for']['submodule'] == parentmodules[1]))   

        if(isDetailed):
            _packages = list(map(lambda v : v, npackages))
            packages = []
            h = '''%s (%s) %s|%s %s %s| %s''' % (
                    (Fore.GREEN + "Package Name" + Fore.CYAN),
                    ("Version"),
                    (Fore.BLUE),
                    (Fore.CYAN),
                    ("Developer"),
                    (Fore.BLUE),
                    (Fore.YELLOW + "Details" + Style.RESET_ALL),
                )
            h1 = (Fore.CYAN + "-"*len(h) +Style.RESET_ALL)
            packages.append("\n")
            packages.append(h)
            packages.append(h1)
            for pkt in _packages:
                h1 = pkt['package_information']['package_name']
                h2 = pkt['package_information']['details']
                h3 = pkt['package_information']['version']
                h4 = pkt['author_info']['creator']
                p = '''\t%s (%s) %s|%s %s %s| %s''' % (
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
            packages = list(map(lambda v : v['package_information']['package_name'], npackages))
        return packages
    #endregion

    #region Package Params
    def package_params(self,selected: list):
        npackages = self.db_packages.table('packages').search(
            (Query()['package_for']['module'] == selected[0])
            & (Query()['package_for']['submodule'] == selected[1])
            & (Query()['package_information']['package_name'] == selected[2])
        )   
        return npackages[0]["package_information"]["entry_file_optional_params"]

    def get_package(self, package_path: list):
        npackages = self.db_packages.table('packages').search(
            (Query()['package_for']['module'] == package_path[0])
            & (Query()['package_for']['submodule'] == package_path[1])
            & (Query()['package_information']['package_name'] == package_path[2])
        )   
        return npackages[0]

    def get_package_run_path(self, package: list):
        npackages = self.db_packages.table('packages').search(
            (Query()['package_for']['module'] == package[0])
            & (Query()['package_for']['submodule'] == package[1])
            & (Query()['package_information']['package_name'] == package[2])
        )
        pkt = npackages[0]
        _path = self.__package_paths.generate_path(NightcapPackagesPathsEnum.PackagesBase, [pkt["package_for"]["module"],pkt["package_for"]["submodule"], \
        pkt["package_information"]["package_name"],pkt["package_information"]["entry_file"]])
        return _path

    #endregion

        