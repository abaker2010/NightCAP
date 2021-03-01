# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# from application.classes.helpers.printers.subprinters.errors import ErrorPrinter
# from application.classes.helpers.printers.print import Printer
from colorama import Fore, Style
from nightcapcore import Printer, NightcapCoreRemoteDocs
# from nightcappackages import NightcapPackages
from nightcappackages.classes.databases.mogo.mongo_packages import MongoPackagesDatabase
import requests
from tinydb.database import TinyDB
from tqdm.auto import tqdm
from zipfile import ZipFile
import os
import stat
import tempfile
import re
import shutil
from nightcappackages import *

# @Singleton
class NightcapUpdater:
    #region Init
    def __init__(self):
        print("Calling update for system")
        print("Updater Instance Created")
        self.tmpdir = None
        self.currentDir = os.getcwd()
        self.updateFile = "update.zip"
        self.tmpUpdatePaths = []
        self.excludedPaths = []
        self.dbPaths = []
        self._excludeExt = (".json", ".pcapng", "LICENSE", ".md")
        self._dbExt = (".json")
        self._dbExclude = "EXAMPLE_MODULE"
        self.updateCalled = False
        self.isMainBranch = None
        self.tmpUpdateLocation = None
        self.installLocation = os.path.dirname(__file__).split('/application')[0]
        self.printer = Printer()
        self.verbose = False
    #endregion

    def __del__(self):
        self.printer.print_formatted_check(text="Updater dest called")

    #region Main Updater Function: does all of the heavy lifting
    def update(self, main: bool, verbose: bool = False):
        self.updateCalled = True
        self.isMainBranch = main
        self.verbose = verbose
        try:
            self.printer.print_underlined_header(text="Updating NightCAP", underline="*", endingBreaks=1, leadingText='')
            if(self.verbose == False):
                print(Fore.LIGHTGREEN_EX, "\t[-] Please wait...")
            self.__create_tmp()
            self.__get_update() # working just commented out for now
            self.__unpackupdate() # working just commented out for now 
            self.__prepare_data()
            # self.__move_data()
            # self.__change_permission()
            self.__combine_db_files()
            self.__remove_tmp()
        except KeyboardInterrupt as e:
            print("User terminated")
            # self.__remove_tmp()
            self.updateCalled = False
        except Exception as ee:
            print("Error:", ee)
            # self.__remove_tmp()
    #endregion

    #region Tmp dir functions
    def __create_tmp(self):
        self.tmpdir = tempfile.mkdtemp()
        if(self.verbose):
            self.printer.print_underlined_header(text="Preparing")
            self.printer.item_1(text="Creating tmp dir " + self.tmpdir)
            
        

    def __remove_tmp(self):
        self.printer.print_underlined_header(text="Clean Up")
        if(self.verbose):
            self.printer.print_header(text="Removing tmp dir")
        shutil.rmtree(self.tmpdir)
        self.tmpUpdatePaths = []
        self.tmpUpdateLocation = None
    #endregion

    #region Get update from Github
    def __get_update(self):
        if(self.verbose):
            self.printer.item_1(text="Downloading Update")
            self.printer.print_header(text="Progress",leadingText='[+]', endingBreaks=1)
        if self.isMainBranch:
            resp = requests.get("https://github.com/abaker2010/NightCAP/archive/main.zip", stream=True)
            self.tmpUpdateLocation = os.path.join(self.tmpdir, "NightCAP-main")
        else:
            resp = requests.get("https://github.com/abaker2010/NightCAP/archive/Dev.zip", stream=True)
            self.tmpUpdateLocation = os.path.join(self.tmpdir, "NightCAP-dev")
        total = int(resp.headers.get('content-length', 0))

        description = Fore.LIGHTMAGENTA_EX + "[-] Using main branch: update.zip" if self.isMainBranch else Fore.LIGHTMAGENTA_EX + "[-] Using dev branch"
        with open(os.path.join(self.tmpdir,self.updateFile), 'wb') as file, tqdm(
            desc=description,
            total=total,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for data in resp.iter_content(chunk_size=1024):
                size = file.write(data)
                bar.update(size)
    #endregion

    #region Unpacking Github update 
    def __unpackupdate(self):
        with ZipFile(os.path.join(self.tmpdir,self.updateFile), 'r') as zip: 
            if(self.verbose):
                self.printer.print_underlined_header(text="Extracting Files", leadingBreaks=2)
            zip.extractall(self.tmpdir) 
            self.printer.item_1(text="tmp -> " + self.tmpdir)
        if(self.verbose):
            self.printer.item_1(text="Done extracting")
        
    #endregion
    
    #region Change Permissions 
    def __change_permission(self):
        os.chmod(os.path.join(self.installLocation, "nightcap.py"), 0o755)
    #endregion 

    #region Combining Files 
    def __combine_db_files(self):
        self.printer.print_underlined_header(text="Trying to combine the db files")

        # the best way to do this would be to make the db's allow for a new file to be passed to it and 
        # make it do the heavy lifting 
        # could do a custom Object += Object for the db's

        for udb in self.dbPaths:
            try:
                if(self.verbose):
                    self.printer.item_1(text="Updater file", optionalText=str(udb).replace(self.tmpdir, "{tmp}"), leadingBreaks=1)
                if(str(udb).endswith("projects_db.json")):
                    self.printer.print_formatted_check("Skipping", leadingTab=3)
                    # NightcapCoreProject().update(TinyDB(udb))
                #     if(self.verbose):
                #         print("Skipping DB:", "Projects_DB")
                #         print("*"*20,"\n")
                elif(str(udb).endswith("packages.json")):
                    self.printer.print_formatted_check("Skipping: Mongo Updater Needed", leadingTab=3)
                    # MogoPackagesDatabase.instance().update()
                #     if(self.verbose):
                #         print("Skipping DB:", "Packages")
                #         print("*"*20,"\n")
                elif(str(udb).endswith("submodules.json")):
                    self.printer.print_formatted_check("Skipping: Mongo Updater Needed", leadingTab=3)
                    # NightcapSubModule().update(TinyDB(udb))
                #     # print("Updater needed")
                #     if(self.verbose):
                #         print("Skipping DB:", "Submodules")
                elif(str(udb).endswith("modules.json")):
                    self.printer.print_formatted_check("Skipping: Mongo update needed", leadingTab=3)
                    # NightcapModules().update(TinyDB(udb))
                elif(str(udb).endswith("protocol_links.json")):
                    NightcapCoreRemoteDocs().update(TinyDB(udb))
                else:
                    raise Exception("Error with file" + str(udb).replace(self.tmpdir, "Tmp -> "))
                    # try:
                    #     raise  ValueError('A very specific bad thing happened.')
                    # except Exception as e:
                    #     self.errorPrinter.print_error(exception=e, msgColor=Fore.MAGENTA)
                        # self.errorPrinter.print_error(exception=e)
                    # self.errorPrinter.print_error("Error with file:", optionaltext=str(udb).replace(self.tmpdir, "Tmp -> "))
            except Exception as e:
                self.printer.print_error(exception=e, errColor=Fore.LIGHTRED_EX)
    #endregion

    #region prepare data Files 
    def __prepare_data(self):
        for path, subdirs, files in os.walk(self.tmpUpdateLocation):
            for name in files:
                full_path = os.path.join(path, name)
                if str(name).endswith(self._dbExt):
                    if self._dbExclude not in str(full_path):
                        self.dbPaths.append(full_path)
                elif str(name).endswith(self._excludeExt):
                   self.excludedPaths.append(full_path)
                # elif str(name).endswith(self._dbExt):
                #     self.dbPaths.append(os.path.join(path, name))
                else:
                    self.tmpUpdatePaths.append(full_path)
    #endregion

    #region move data
    def __move_data(self):
        print("Moving data")
        print(self.tmpUpdateLocation)
        print(self.installLocation)  
        newPath = lambda s: re.sub(self.tmpUpdateLocation, self.installLocation, s)
        for tpath in self.tmpUpdatePaths:
            self.__move_file(tpath, newPath(tpath))
    #endregion

    #region move Files 
    def __move_file(self, tmpPath: str, installPath: str):
        print("Moving file from", tmpPath, "->", installPath)
        os.replace(tmpPath, installPath)
        print("*" * 10)
    #endregion
        
    #region OnClose modifications 
    def onCloseModifications(self):
        newPath = lambda s: re.sub(self.tmpUpdateLocation, self.installLocation, s)
        print("Files to exclude")
        for tpath in self.excludedPaths:
            print(tpath)
            print(newPath(tpath))
            print("*" * 10)
        # self.__remove_tmp()
    #endregion
