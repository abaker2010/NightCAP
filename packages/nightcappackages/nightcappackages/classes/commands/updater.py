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
import os
import shutil
import json
from nightcappackages import *
from nightcapcore import NightcapCLIConfiguration
from nightcappackages.classes.commands.installer import NightcapPackageInstallerCommand
from nightcappackages.classes.commands.uninstaller import NightcapPackageUninstallerCommand
from nightcappackages.classes.helpers.check_version import NightcapPackageVersionCheckHelper
from nightcappackages.classes.helpers.get_updater import NightcapPackageUpdateDownloaderHelper
from nightcappackages.classes.databases.mogo.mongo_packages import MongoPackagesDatabase
from nightcappackages.classes.helpers.tmp_files import NightcapTmpFileHelper
# endregion


class NightcapPackageUpdaterCommand(Command):
    # region Init
    def __init__(self, config: NightcapCLIConfiguration, main: bool, verbose: bool = False):
        self.currentDir = os.getcwd()
        self.updateFile = "update.ncb"
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

            _available = tuple(NightcapPackageVersionCheckHelper(self.isMainBranch, self.config.mainbranch, self.config.buildNumber, self.config.versionNumber).check())

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

                    if self.isMainBranch:
                        _url = "https://github.com/abaker2010/NightCAPVersions/raw/main/%s/%s/update.ncb" % (
                            str(_available[1]), str(_available[2]))
                    else:
                        _url = "https://github.com/abaker2010/NightCAPVersions/raw/main/%s/%s/update-dev.ncb" % (
                            str(_available[1]), str(_available[2]))
                    _tmpfile = NightcapTmpFileHelper()

                    try:
                        _tmpfile.create()
                        print(_tmpfile.tmp_location)
                        _updater = tuple(NightcapPackageUpdateDownloaderHelper(_url, _tmpfile.tmp_location, verbose=True).get())
                        print(_updater)
                        if _updater[0] == True:
                            print("loc", str(_updater[1]))
                            self._update(str(_updater[1]), str(_updater[2]))

                    except Exception as e:
                    
                        raise e
                    finally:
                        _tmpfile.delete()
                        pass


                    self.config.config.set('BUILD_DATA', 'main_branch', str(self.isMainBranch))
                    self.config.config.set('BUILD_DATA', 'build', _available[1])
                    self.config.config.set('BUILD_DATA', 'version', _available[2])
                    
                    self.config.buildNumber = _available[1]
                    self.config.versionNumber = _available[2]
                    self.config.mainbranch = _available[0]
            self.config.Save()
            self.printer.print_header(
                "Update Complete", leadingColor=Fore.MAGENTA, leadingText='[~]', leadingTab=1, titleColor=Fore.CYAN, endingBreaks=1)
            # endregion

        except KeyboardInterrupt as e:
            self.printer.print_error(Exception("User Terminated"))
            self.updateCalled = False
        except Exception as ee:
            self.printer.print_error(ee)
        finally:
            agree = input(
                    Fore.LIGHTGREEN_EX
                    + "\n\t\tManual restart is required. Press Enter when ready: "
                    + Style.RESET_ALL
                ).lower()

    # region Update
    def _update(self, tmppath: str, filename: str):
        if ".ncb" in filename:

            self.printer.print_underlined_header(
                "Starting Update", leadingBreaks=1)

            self.printer.print_underlined_header("Unpacking Backup")

            name = os.path.basename(str(filename))
            new_name = name.replace(".ncb", ".zip")


            os.rename(os.path.join(tmppath, name),
                      os.path.join(tmppath, new_name))

            shutil.unpack_archive(os.path.join(
                tmppath, new_name), os.path.join(tmppath, "updater"), "zip")
            shutil.unpack_archive(os.path.join(tmppath, "updater", "installers.zip"), os.path.join(
                tmppath, "updater", "installers"), "zip")
            self.printer.print_formatted_check("Successfully unpacked backup")

            _installers_path = os.path.join(
                tmppath, "updater", "installers")
            _r_paths = self._restore_installers_paths(_installers_path)
            self.printer.print_underlined_header("Checking Packages")
            for _r in _r_paths:
                self.printer.print_formatted_additional("Checking", optionaltext=str(_r['name']))

                _new_name = str(_r['path']).replace(".ncp", ".zip")
                
                os.rename(str(_r['path']), _new_name)

                shutil.unpack_archive(_new_name, os.path.join(
                    tmppath, str(_r['name'])), "zip")

                os.rename(_new_name, str(_r['path']))

                for root, dirs, files in os.walk(os.path.join(tmppath, str(_r['name'])), topdown=False):
                    for name in files:
                        if name == 'package_info.json':
                            with open(os.path.join(root, name)) as json_file:
                                _package = json.load(json_file)
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
            return True
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
