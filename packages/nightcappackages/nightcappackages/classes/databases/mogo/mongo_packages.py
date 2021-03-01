# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Import
# from application.classes.base_cmd.base_cmd import NightcapBaseCMD
from colorama.ansi import Fore, Style
from nightcappackages.classes.databases.mogo.interfaces.mogo_operations import MongoDatabaseOperationsInterface
from nightcappackages.classes.databases.mogo.mongo_connection import MongoDatabaseConnection
from nightcapcore.decorators.singleton import Singleton
import sys
import subprocess
import pkg_resources

@Singleton
class MogoPackagesDatabase(MongoDatabaseConnection, MongoDatabaseOperationsInterface):
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

    def delete(self):
        pass


    def check_package_path(self, path: list):
        # return self.db_packages.table('packages').search(
        #     (Query()['package_for']['module'] == path[0])
        #     & (Query()['package_for']['submodule'] == path[1])
        #     & (Query()['package_information']['package_name'] == path[2])) 
        print("Check package path needs done")
        _module = path[0]
        _submodule = path[1]
        _package = path[2]
        _ = self._db.find_one({
            "$and" : [{
            "package_for.module" : {'$eq': _module},
            "package_for.submodule" : {'$eq' : _submodule},
            "package_information.package_name" : {'$eq' : _package}
        }]})
        print(_)
        return False if _ == None else True

    def package_params(self,selected: list):
        _module = selected[0]
        _submodule = selected[1]
        # __package__
        _npackages = self._db.find({
            "$and" : [{
            "package_for.module" : {'$eq': _module},
            "package_for.submodule" : {'$eq' : _submodule}
        }]})
        # npackages = self.db_packages.table('packages').search(
        #     (Query()['package_for']['module'] == selected[0])
        #     & (Query()['package_for']['submodule'] == selected[1])
        #     & (Query()['package_information']['package_name'] == selected[2])
        # )   
        # return npackages[0]["package_information"]["entry_file_optional_params"]

    def get_package_config(self,parentmodules: list):
        _module = parentmodules[0]
        _submodule = parentmodules[1]
        _package = parentmodules[2]
        print(_module)
        print(_submodule)
        print(_package)
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

    #region Find Packages
    def find_package(self, package: dict = None):
        return self._db.find_one(package)
    #endregion

    #region Install
    def install(self, package: dict = None):
        _puid = package['package_information']['uid']
        # self.printer.print_formatted_check(text="Looking for puid: " + _puid)
        if(self.find_package(package) == None):
            try:
                self._collect_imports(package)
                self.create(package)
            except Exception as e:
                self.printer.print_error(e)
        else:
            self.printer.print_formatted_check(text="Package Already Installed")
    #endregion

    #region Collect Imports
    def _collect_imports(self, package: dict = None):
        try:
            _imports = list(package['package_information']['imports'])
            # print("Imports needed for the program", _imports)
            
            if(_imports == []):
                print("add package to db")
            else:
                self.printer.print_underlined_header_undecorated(text="Installing Required Packages")

                installed_packages_dict = {}
                installed_packages = pkg_resources.working_set
                for i in installed_packages:
                    installed_packages_dict[i.key] = {"version":i.version}
                for pkg in _imports:

                    _ver = None if pkg['version'] == '' else pkg['version']
                    
                    if pkg['package'] not in installed_packages_dict.keys():
                        try:
                            self._install_import(pkg)
                        except Exception as e:
                            self.printer.print_error(e)
                    else:
                        
                        if(pkg['version'] != ''):
                            _ver = str(installed_packages_dict[pkg['package']]['version'])
                            _rver = str(pkg['version'])
                            if(_rver == _ver):
                                # print("version required is the same/older")
                                self.printer.print_formatted_check(text="Installed: " + pkg['package'], optionaltext=str(pkg['version']))
                            elif(_rver != _ver):
                                # print("version required is the same/older")
                                self.printer.print_formatted_additional(text="Collison: " + pkg['package'])
                                self.printer.print_formatted_additional(text="Required Version", optionaltext=str(pkg['version']), leadingTab=3)
                                self.printer.print_formatted_additional(text="Installed Version", optionaltext=str(installed_packages_dict[pkg['package']]['version']), leadingTab=3)
                                agree = input(Fore.LIGHTGREEN_EX + "\n\t\tOverride package? (Y/n): " + Style.RESET_ALL).lower()
                                yes = self.conf.currentConfig.get('NIGHTCAPCORE', 'yes').split()
                                if agree in yes:
                                    self.printer.print_formatted_delete(text="(Confirm) This will replace the currently installed pip package.")
                                    self.printer.print_formatted_additional(text=("Existing: %s :: %s, Replacement: %s :: %s") % (str(pkg['package']), str(installed_packages_dict[pkg['package']]['version']),str(pkg['package']), str(pkg['version'])))
                                    agree = input(Fore.RED + "\n\t\tContinue? (Y/n): " + Style.RESET_ALL).lower()
                                    if agree in yes:
                                        print("override package")
                                        self._install_import(pkg)

                            else:
                                print("version required is greater")
                print()
        except Exception as e:
            raise e
    #endregion

    #region install imports
    def _install_import(self, imprt: dict = None):
        _pkg = None
        _ver = "Any" if imprt['version'] == '' else imprt['version']
        if(imprt['version'] == ''):
            _pkg = imprt['package']
        else:
            _pkg = imprt['package'] + "==" + imprt['version']
        
        self.printer.print_formatted_additional(text="Installing", optionaltext=imprt['package'] + " ver. " + _ver, textColor=Fore.LIGHTYELLOW_EX)
        print("current command to use", _pkg)
        
        try:
            python = sys.executable
            subprocess.check_call(['sudo', '-H', python, '-m', 'pip', 'install', _pkg, '--force-reinstall'], stdout=subprocess.DEVNULL)
        except Exception as e:
            raise e
    #endregion

    #region get all packages
    def get_all_packages(self):
        return self.read()
    #endregion


        