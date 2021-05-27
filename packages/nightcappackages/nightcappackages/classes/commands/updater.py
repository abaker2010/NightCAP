# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Imports

from nightcapcore import *
import shutil
from colorama import Fore, Style
from nightcapcore import Printer
import requests
from tqdm.auto import tqdm
import os
import tempfile
import shutil
import urllib
import json
import time
import sys
from nightcappackages import *
from nightcapcore import NightcapCLIConfiguration
from nightcappackages.classes.commands.installer import NightcapPackageInstallerCommand
from nightcappackages.classes.commands.uninstaller import NightcapPackageUninstallerCommand
from nightcappackages.classes.databases.mogo.mongo_packages import MongoPackagesDatabase
# endregion


class NightcapPackageUpdaterCommand(Command):
    # region Init
    def __init__(self, config: NightcapCLIConfiguration, main: bool, verbose: bool = False):
        self.tmpdir = None
        self.currentDir = os.getcwd()
        self.updateFile = "update.ncb"
        self.tmpUpdatePaths = []
        self.excludedPaths = []
        self.dbPaths = []
        self._excludeExt = (".json", ".pcapng", "LICENSE", ".md")
        self._dbExt = ".json"
        self._dbExclude = "EXAMPLE_MODULE"
        self.updateCalled = False
        self.isMainBranch = None
        # self.tmpUpdateLocation = None
        self.installLocation = os.path.dirname(
            __file__).split("/application")[0]
        self.printer = Printer()
        self.verbose = False
        self.config = config
        self.main = main
        self.verbose = verbose
        self.yes = self.config.config.get("NIGHTCAPCORE", "yes").split()


    # endregion

    # region Execute
    def execute(self) -> None:
        self.updateCalled = True
        self.isMainBranch = self.main
        self.verbose = self.verbose
        try:
            self.printer.print_underlined_header(
                "Updating NightCAP", underline="*", endingBreaks=1, leadingText=""
            )
            if self.verbose == False:
                self.printer.print_header(
                    leadingText='[-]', text='Please wait...')

            _available = tuple(self._check_version())

            # print("config  main: ", self.config.mainbranch)
            # print("expected: ", self.isMainBranch)


            # reigon needs fixed 

            if _available[0] == False:
                self.printer.print_formatted_check("Running the most current version", endingBreaks=1)
            else:
                self.printer.print_formatted_additional("Update Available")
                agree = input(
                    Fore.LIGHTGREEN_EX
                    + "\n\t\tWould you like to update now? (Y/n): "
                    + Style.RESET_ALL
                ).lower()

                if agree in self.yes or len(agree) == 0:
                    print("Update me")
                    # self.mongo_server.initialize_database()
                    # self.printer.print_formatted_additional(text="Rebooting...")
                    # os.execv(sys.argv[0], sys.argv)
                    self.__create_tmp()
                    self._get_version(_available[1], _available[2])
                    self.__remove_tmp()

                    self.config.config.set('BUILD_DATA', 'main_branch', _available[0])
                    self.config.config.set('BUILD_DATA', 'build', _available[1])
                    self.config.config.set('BUILD_DATA', 'version', _available[2])

                    self.config.Save()
                    
                    self.printer.print_formatted_additional('Restarting Please Wait...')
                    # os.execv(sys.argv[0], sys.argv)
                else:
                    raise KeyboardInterrupt()
            


            # if _available[0] == False and self.config.mainbranch == self.isMainBranch:
            #     self.printer.print_formatted_check(
            #         "Current version is already updated", endingBreaks=1)
            # elif _available[0] == False and self.config.mainbranch != self.isMainBranch:
            #     self.printer.print_formatted_additional(
            #         "Updating the branch", endingBreaks=1)
            # else:
            #     self.printer.print_formatted_additional(
            #         "Full Update", endingBreaks=1)
            #     # self.printer.print_error(Exception("New Version Available"))
            #     # self.__create_tmp()
            #     # self._get_version(_available[1], _available[2])
            #     # self.__remove_tmp()

            # self.config.config.set('BUILD_DATA', 'main_branch', _available[0])
            # self.config.config.set('BUILD_DATA', 'build', _available[1])
            # self.config.config.set('BUILD_DATA', 'version', _available[2])
            
            # # self.config.mainbranch = bool(_available[0])
            # self.config.Save()
            self.printer.print_header(
                "Update Complete", leadingColor=Fore.MAGENTA, leadingText='[~]', leadingTab=1, titleColor=Fore.CYAN, endingBreaks=1)
            # endregion


            # restart after the config is updated.
            # self.printer.print_formatted_additional('Restarting Please Wait...')
            # os.execv(sys.argv[0], sys.argv)

        except KeyboardInterrupt as e:
            self.printer.print_error(Exception("User Terminated"))
            self.__remove_tmp()
            self.updateCalled = False
        except Exception as ee:
            self.printer.print_error(ee)
            self.__remove_tmp()
    # endregion

    # region Del
    def __del__(self):
        # try:
        #     self.__remove_tmp()
        # except:
        pass
    # endregion

    # region Get Remote Version
    def _check_version(self):
        self.printer.print_formatted_additional("Getting Remote Versions")
        _url = "https://raw.githubusercontent.com/abaker2010/NightCAPVersions/main/versions.json"

        try:
            r = urllib.request.urlopen(_url)
            status_code = r.getcode()

            if status_code == 200:
                _versions = json.load(r)

                _current_build = int(self.config.buildNumber)
                _current_version = int(self.config.versionNumber)

                if self.isMainBranch:
                    _remote_version = int(_versions['stable']['version'])
                    _remote_build = int(_versions['stable']['build'])
                else:
                    _remote_version = int(_versions['dev']['version'])
                    _remote_build = int(_versions['dev']['build'])

                if self.config.mainbranch == self.isMainBranch and _current_build == _remote_build and _current_version == _remote_version:
                    return (False, _remote_build, _remote_version)
                else:
                    return (True, _remote_build, _remote_version)

        except Exception as e:
            self.printer.print_error(Exception("Error getting versions.json"))
            self.printer.print_error(e)

    # endregion

    # region Check for next version
    # Versions will be created on a build 1-10 scale before the version number itselfs increments
    # this will be build accordingly for now. If there is a change this will be done within a build update

    def _get_version(self, build: str, version: str):
        # if self.verbose == True:
        self.printer.print_formatted_additional("Checking for new version")

        if self.isMainBranch:
            _url = "https://github.com/abaker2010/NightCAPVersions/raw/main/%s/%s/update.ncb" % (
                str(build), str(version))
        else:
            _url = "https://github.com/abaker2010/NightCAPVersions/raw/main/%s/%s/update-dev.ncb" % (
                str(build), str(version))

        print("Getting url: ", _url)
        self.printer.print_formatted_additional("Updating via branch", optionaltext="Main" if self.isMainBranch else "Dev")
        status_code = 404

        try:
            r = urllib.request.urlopen(_url)
            status_code = r.getcode()

            if status_code == 200:

                # working just commented out for now
                _new_version = self.__get_update(_url)
                if _new_version:
                    _u_path = os.path.join(self.tmpdir, self.updateFile)
                    # self._update(str(_u_path))
                    # return NightcapUpdateHelper(str(_u_path)).update()
                    # return True
                    return self._update(str(_u_path))

            else:
                self.printer.print_error(
                    Exception("Error code: " + str(status_code)))
                return False
        except urllib.request.HTTPError as e:
            # if self.verbose == True:
            # self.printer.print_error(e)
            if status_code == 404:
                print(e)
                self.printer.print_error(
                    Exception("Error getting update. File Not found."))
                self.printer.print_formatted_additional(_url)
            #     self.printer.print_formatted_check("Running the current version", leadingBreaks=1, endingBreaks=1)
            # else:
            #     self.printer.print_formatted_check("Running the current version", leadingTab=1, leadingBreaks=1, endingBreaks=1)
            return False

    # endregion

    # region Tmp dir functions
    def __create_tmp(self):
        self.tmpdir = tempfile.mkdtemp()
        # if self.verbose:
        self.printer.print_underlined_header("Preparing")
        self.printer.item_1("Creating tmp dir " + self.tmpdir)

    def __remove_tmp(self):
        self.printer.print_underlined_header("Clean Up")
        # if self.verbose:
        self.printer.print_header("Removing tmp dir", endingBreaks=1)
        shutil.rmtree(self.tmpdir)
        self.tmpUpdatePaths = []
        self.tmpUpdateLocation = None

    # endregion

    # region Get update from Github
    def __get_update(self, url: str):
        try:
            if self.verbose:
                self.printer.item_1("Downloading Update")
                self.printer.print_header(
                    "Progress", leadingText="[+]", leadingBreaks=1, endingBreaks=1)
            if self.isMainBranch:
                resp = requests.get(
                    url, stream=True
                )
                # os.path.join(self.tmpdir, "NightCAP-main")
                self.tmpdir = self.tmpdir
            else:
                resp = requests.get(
                    url, stream=True
                )
                # os.path.join(self.tmpdir, "NightCAP-dev")
                self.tmpdir = self.tmpdir
            total = int(resp.headers.get("content-length", 0))

            description = (
                Fore.LIGHTMAGENTA_EX + "[-] Using main branch: update.ncb"
                if self.isMainBranch
                else Fore.LIGHTMAGENTA_EX + "[-] Using dev branch"
            )
            with open(os.path.join(self.tmpdir, self.updateFile), "wb") as file, tqdm(
                desc=description,
                total=total,
                unit="iB",
                unit_scale=True,
                unit_divisor=1024,
            ) as bar:
                for data in resp.iter_content(chunk_size=1024):
                    size = file.write(data)
                    bar.update(size)

            return True
        except Exception as e:
            self.printer.print_error(e)
            return False

    # endregion

    # region Update
    def _update(self, path: str):
        if ".ncb" in str(path).split(os.sep)[-1]:

            self.printer.print_underlined_header(
                "Starting Update", leadingBreaks=1)
            self.printer.print_formatted_additional(
                "Update File Path", optionaltext=path, endingBreaks=1)

            # _cleaned = NightcapCleanHelper().clean()

            # if _cleaned:
            self.printer.print_underlined_header("Unpacking Backup")
            # tmpdir = tempfile.mkdtemp()

            # shutil.copy(str(path), self.tmpdir)
            name = os.path.basename(str(path))
            new_name = name.replace(".ncb", ".zip")
            dir = os.path.dirname(str(path))

            os.rename(os.path.join(self.tmpdir, name),
                      os.path.join(self.tmpdir, new_name))

            shutil.unpack_archive(os.path.join(
                self.tmpdir, new_name), os.path.join(self.tmpdir, "updater"), "zip")
            shutil.unpack_archive(os.path.join(self.tmpdir, "updater", "installers.zip"), os.path.join(
                self.tmpdir, "updater", "installers"), "zip")
            self.printer.print_formatted_check("Successfully unpacked backup")

            _installers_path = os.path.join(
                self.tmpdir, "updater", "installers")
            _r_paths = self._restore_installers_paths(_installers_path)
            self.printer.print_underlined_header("Checking Packages")
            for _r in _r_paths:
                # self._restore_installers(_r)
                self.printer.print_formatted_additional("Checking", optionaltext=str(_r['name']))
                self.printer.print_formatted_additional(str(_r['path']))

                _new_name = str(_r['path']).replace(".ncp", ".zip")
                
                os.rename(str(_r['path']), _new_name)

                shutil.unpack_archive(_new_name, os.path.join(
                    self.tmpdir, str(_r['name'])), "zip")

                os.rename(_new_name, str(_r['path']))

                for root, dirs, files in os.walk(os.path.join(self.tmpdir, str(_r['name'])), topdown=False):
                    for name in files:
                        if name == 'package_info.json':
                            with open(os.path.join(root, name)) as json_file:
                                _package = json.load(json_file)
                            _isUpdatble = False
                            _pkexists = MongoPackagesDatabase().check_package_path(
                                [_package['package_for']['module'], _package['package_for']['submodule'], _package["package_information"]["package_name"]])

                            if _pkexists == False:
                                self.printer.print_formatted_additional(
                                    "Installing package")
                                invoker = Invoker()
                                invoker.set_on_start(
                                    NightcapPackageInstallerCommand(str(_r['path'])))
                                invoker.execute()
                            else:

                                _current_package = MongoPackagesDatabase().get_package_config(
                                    [_package['package_for']['module'], _package['package_for']['submodule'], _package["package_information"]["package_name"]])
                                if _current_package['package_information']['version'] == _package['package_information']['version']:
                                    self.printer.print_formatted_check(
                                        "Current version installed", optionaltext=_package['package_information']['version'])
                                else:
                                    self.printer.print_formatted_additional(
                                        "Update Package")
                                    invoker = Invoker()
                                    invoker.set_on_start(NightcapPackageUninstallerCommand(
                                        "/".join([_package['package_for']['module'], _package['package_for']['submodule'], _package["package_information"]["package_name"]]), True))
                                    invoker.execute()
                                    
                                    invoker.set_on_start(
                                    NightcapPackageInstallerCommand(str(_r['path'])))
                                    invoker.execute()
                                    ScreenHelper().clearScr()

                # time.sleep(3)

            # self.printer.item_1("Cleaning Up", leadingBreaks=1, endingBreaks=1)
            # # shutil.rmtree(self.tmpdir)
            # self.printer.print_formatted_check("Restore Completed", leadingBreaks=1, endingBreaks=1)
            return True
            # else:
            #     self.printer.print_error(Exception("There was an error when cleaning, please view above for more details."))
            #     return False
        else:
            self.printer.print_error(
                Exception("Please check the backup file. Inforrect file type used"))
            return False

    def _restore_installers_paths(self, location: str):
        _installers = []

        for root, dirs, files in os.walk(location):
            for file in files:
                if file.endswith('.ncp'):
                    _installers.append({"name": file.replace(
                        ".ncp", ''), "path": os.path.join(root, file)})
        return _installers

    # endregion
