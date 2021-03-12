# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Import
# from application.classes.base_cmd.base_cmd import NightcapBaseCMD
from bson.objectid import ObjectId
from colorama.ansi import Fore, Style
from nightcappackages.classes.databases.mogo.interfaces.mogo_operations import MongoDatabaseOperationsInterface
from nightcappackages.classes.databases.mogo.mongo_connection import MongoDatabaseConnection
from nightcapcore.decorators.singleton import Singleton
from nightcappackages.classes.paths.pathsenum import NightcapPackagesPathsEnum
from nightcappackages.classes.paths.paths import NightcapPackagesPaths

@Singleton
class MongoPackagesDatabase(MongoDatabaseConnection, MongoDatabaseOperationsInterface):
    def __init__(self):
        MongoDatabaseConnection.__init__(self)
        MongoDatabaseOperationsInterface.__init__(self)
        self._db = self.client[self.conf.currentConfig['MONGOSERVER']['db_name']]['packages']

    def create(self, pkg: dict):
        self._db.insert_one(pkg)

    def read(self):
        return self._db.find()

    def update(self):
        # super().update(updatetable=updatedb.table('packages'),localtable=self.db_packages.table('packages'),checkonrow='package_information',checkonrowtwo='uid', updaterrule=NightcapCoreUpaterRules.Package)
        pass

    def delete(self, puid: ObjectId):
        self._db.delete_one({'_id' : puid})

    
    def get_package_run_path(self, pkg_config: dict = None):
        _path = NightcapPackagesPaths().generate_path(NightcapPackagesPathsEnum.PackagesBase, [pkg_config["package_for"]["module"],pkg_config["package_for"]["submodule"], \
        pkg_config["package_information"]["package_name"],pkg_config["package_information"]["entry_file"]])
        return _path

    def check_package_path(self, path: list):
        _module = path[0]
        _submodule = path[1]
        _package = path[2]
        _ = self._db.find_one({
            "$and" : [{
            "package_for.module" : {'$eq': _module},
            "package_for.submodule" : {'$eq' : _submodule},
            "package_information.package_name" : {'$eq' : _package}
        }]})
        return False if _ == None else True

    def package_params(self,selected: list):
        _module = selected[0]
        _submodule = selected[1]
        _package = selected[2]
        print("Finding package params")
        print(_module)
        print(_submodule)
        print(_package)
        # __package__
        _npackages = self._db.find({
            "$and" : [{
            "package_for.module" : {'$eq': _module},
            "package_for.submodule" : {'$eq' : _submodule}
        }]})

    def get_package_config(self,parentmodules: list):
        _module = parentmodules[0]
        _submodule = parentmodules[1]
        _package = parentmodules[2]
        return self._db.find_one({
            "$and" : [{
            "package_for.module" : {'$eq': _module},
            "package_for.submodule" : {'$eq' : _submodule},
            "package_information.package_name" : {'$eq' : _package}
        }]})

    #region Get Options Packages
    def packages(self,parentmodules: list,isDetailed: bool = False):
        _module = parentmodules[0]
        _submodule = parentmodules[1]
        _npackages = self._db.find({
            "$and" : [{
            "package_for.module" : {'$eq': _module},
            "package_for.submodule" : {'$eq' : _submodule}
        }]})

        npackages = []
        for _npkg in _npackages:
            npackages.append(_npkg)
        
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
            packages = list(map(lambda v : v['package_information']['package_name'], list(npackages)))
        return packages
    #endregion

    #region Find Package
    def find_package(self, package: dict = None):
        return self._db.find_one(package)
    #endregion

    #region Find Packages
    def find_packages(self, module: str = None, submodule: str = None):
        return self._db.find({
            "$and" : [{
            "package_for.module" : {'$eq': module},
            "package_for.submodule" : {'$eq' : submodule}
        }]})
    #endregion

    #region Install
    def install(self, package: dict = None):
        _puid = package['package_information']['uid']
        if(self.find_package(package) == None):
            try:
                self.create(package)
                return True
            except Exception as e:
                self.printer.print_error(e)
                return False
        else:
            self.printer.print_formatted_check(text="Package Already Installed")
            return False
    #endregion

    #region get all packages
    def get_all_packages(self):
        return self.read()
    #endregion


        