# Copyright 2020 by Aarom Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
from nightcapcore.output.console_output import NightcapCoreConsoleOutput
from ..paths import NightcapPackagesPathsEnum, NightcapPackagesPaths
from tinydb import TinyDB, Query
import shutil

class NightcapPackageUninstaller():
    def __init__(self, package_path: str):
        print("uninstaller")
        self.db_packages = TinyDB(NightcapPackagesPaths().generate_path(NightcapPackagesPathsEnum.Databases, ['packages.json']))
        self.output = NightcapCoreConsoleOutput()
        self.__package_paths = NightcapPackagesPaths()
        
        try:
            split_package_path = package_path.split("/")
            packageExists = self.db_packages.table('packages').search(
                (Query()['package_for']['module'] == split_package_path[0])
                & (Query()['package_for']['submodule'] == split_package_path[1])
                & (Query()['package_information']['package_name'] == split_package_path[2])
            )
            if(len(packageExists) == 0):
                self.output.output("Package does not exist", level=6)
            else:
                uconfirm = self._confim_delete(package_path)
                if(uconfirm.lower() == "y"):
                    packageExists[0].doc_id
                    try:
                        self.db_packages.table('packages').remove(doc_ids=[packageExists[0].doc_id])
                        self._delete(packageExists[0])
                        
                        if(self.db_packages.table('packages').contains(Query()['package_information']['uid'] == packageExists[0]["package_information"]["uid"]) is False):
                            self.output.output("UNINSTALLED")
                    except Exception as e:
                        self.output.output('Didnt Delete: '+str(e), level=6)

        except Exception as e:
            raise Exception("Package not found")

    def _confim_delete(self, package_path: str):
        return self.output.input("ARE YOU SURE YOU WANT TO UNINSTALL %s? [y/n]: " % (package_path)) 
       

    def _delete(self, pkt: dict):
        _path = self.__package_paths.generate_path(NightcapPackagesPathsEnum.PackagesBase, [pkt['package_for']['module'],pkt['package_for']['submodule'], pkt['package_information']['package_name']])
        # self.output.output("Path to delete: " + _path, level=2)
        try:
            shutil.rmtree(_path)
        except OSError as e:
            self.output.output("Error: %s - %s." % (e.filename, e.strerror), level=6)
