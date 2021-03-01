# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
from tinydb import TinyDB, Query
from colorama import Fore, Style
from nightcapcore import *
from .paths import NightcapPackagesPathsEnum, NightcapPackagesPaths

class NightcapPackages(NightcapCoreUpdaterBase): 
    def __init__(self):
        super(NightcapPackages, self).__init__()
        self.__package_paths = NightcapPackagesPaths()
        self.db_packages = TinyDB(NightcapPackagesPaths().generate_path(NightcapPackagesPathsEnum.Databases, ['packages.json']))

    #region Find Packages
    def find_packages(self, module: str, submodule: str):
        # print("Finding packages based on:", module, submodule)
        _packages = list(map(lambda v : v, self.db_packages.table('packages').search(
            (Query()['package_for']['module'] == module) & (Query()['package_for']['submodule'] == submodule)
        )))

        return _packages

    #endregion


    #region Package Params
    def package_params(self,selected: list):
        npackages = self.db_packages.table('packages').search(
            (Query()['package_for']['module'] == selected[0])
            & (Query()['package_for']['submodule'] == selected[1])
            & (Query()['package_information']['package_name'] == selected[2])
        )   
        return npackages[0]["package_information"]["entry_file_optional_params"]

    # def get_package(self, package_path: list):
    #     npackages = self.db_packages.table('packages').search(
    #         (Query()['package_for']['module'] == package_path[0])
    #         & (Query()['package_for']['submodule'] == package_path[1])
    #         & (Query()['package_information']['package_name'] == package_path[2])
    #     )   
    #     return npackages[0]

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
 
# DB file to be used for update:  <nightcappackages.classes.packages.NightcapPackages object at 0x7fe63624c9a0>
# DB file to be used to add global:  /var/folders/xk/95x183fd35bdp7069kx3wkx40000gn/T/tmp6_aib3q3/NightCAP-dev/EXAMPLE_MODULE/test_module/package_info.json
# /var/folders/xk/95x183fd35bdp7069kx3wkx40000gn/T/tmp6_aib3q3/NightCAP-dev/packages/nightcapcore/nightcapcore/database/projects_db.json updater file
# adding
# DB file to be used for update:  <nightcappackages.classes.packages.NightcapPackages object at 0x7fe63626f280>
# DB file to be used to add global:  /var/folders/xk/95x183fd35bdp7069kx3wkx40000gn/T/tmp6_aib3q3/NightCAP-dev/packages/nightcapcore/nightcapcore/database/projects_db.json
# /var/folders/xk/95x183fd35bdp7069kx3wkx40000gn/T/tmp6_aib3q3/NightCAP-dev/packages/nightcapcore/nightcapcore/database/protocol_links.json updater file
# adding
# DB file to be used for update:  <nightcappackages.classes.packages.NightcapPackages object at 0x7fe63624c9a0>
# DB file to be used to add global:  /var/folders/xk/95x183fd35bdp7069kx3wkx40000gn/T/tmp6_aib3q3/NightCAP-dev/packages/nightcapcore/nightcapcore/database/protocol_links.json
# /var/folders/xk/95x183fd35bdp7069kx3wkx40000gn/T/tmp6_aib3q3/NightCAP-dev/packages/nightcappackages/nightcappackages/classes/databases/submodules.json updater file
# adding
# DB file to be used for update:  <nightcappackages.classes.packages.NightcapPackages object at 0x7fe63626f280>
# DB file to be used to add global:  /var/folders/xk/95x183fd35bdp7069kx3wkx40000gn/T/tmp6_aib3q3/NightCAP-dev/packages/nightcappackages/nightcappackages/classes/databases/submodules.json
# /var/folders/xk/95x183fd35bdp7069kx3wkx40000gn/T/tmp6_aib3q3/NightCAP-dev/packages/nightcappackages/nightcappackages/classes/databases/packages.json updater file
# adding
# DB file to be used for update:  <nightcappackages.classes.packages.NightcapPackages object at 0x7fe63624c9a0>
# DB file to be used to add global:  /var/folders/xk/95x183fd35bdp7069kx3wkx40000gn/T/tmp6_aib3q3/NightCAP-dev/packages/nightcappackages/nightcappackages/classes/databases/packages.json
# /var/folders/xk/95x183fd35bdp7069kx3wkx40000gn/T/tmp6_aib3q3/NightCAP-dev/packages/nightcappackages/nightcappackages/classes/databases/modules.json updater file
# adding
# DB file to be used for update:  <nightcappackages.classes.packages.NightcapPackages object at 0x7fe63626f280>
# DB file to be used to add global:  /var/folders/xk/95x183fd35bdp7069kx3wkx40000gn/T/tmp6_aib3q3/NightCAP-dev/packages/nightcappackages/nightcappackages/classes/databases/modules.json
# /var/folders/xk/95x183fd35bdp7069kx3wkx40000gn/T/tmp6_aib3q3/NightCAP-dev/application/classes/database/projects.json updater file
# adding
# DB file to be used for update:  <nightcappackages.classes.packages.NightcapPackages object at 0x7fe63624c9a0>
# DB file to be used to add global:  /var/folders/xk/95x183fd35bdp7069kx3wkx40000gn/T/tmp6_aib3q3/NightCAP-dev/application/classes/database/projects.json
# Removing tmp dir
