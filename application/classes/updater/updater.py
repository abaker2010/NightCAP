# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
from colorama import Fore, Style
import requests
from tqdm.auto import tqdm
from zipfile import ZipFile
import os
import tempfile
import re
import shutil
from nightcapcore.decorators.singleton import Singleton 

@Singleton
class NightcapUpdater:
    
    def __init__(self):
        print("Calling update for system")
        print("Updater Instance Created")
        self.tmpdir = None
        self.currentDir = os.getcwd()
        self.updateFile = "update.zip"
        self.tmpUpdatePaths = []
        self.excludedPaths = []
        self._excludeExt = (".json", ".pcapng")
        self.updateCalled = False
        self.isMainBranch = None

    def update(self, main: bool):
        self.updateCalled = True
        self.isMainBranch = main

        try:
            self.__create_tmp()
            self.__get_update() # working just commented out for now
            self.__unpackupdate() # working just commented out for now 
            self.__move_data()
        except KeyboardInterrupt as e:
            print("User terminated")
            self.__remove_tmp()
            self.updateCalled = False

    def __create_tmp(self):
        self.tmpdir = tempfile.mkdtemp()
        print("Creating tmp dir: ", self.tmpdir)

    def __remove_tmp(self):
        print("Removing tmp dir")
        shutil.rmtree(self.tmpdir)

    def __get_update(self):
        if self.isMainBranch:
            print("Using main branch")
            resp = requests.get("https://github.com/abaker2010/NightCAP/archive/main.zip", stream=True)
        else:
            print("Using dev branch")
            resp = requests.get("https://github.com/abaker2010/NightCAP/archive/Dev.zip", stream=True)
        total = int(resp.headers.get('content-length', 0))
        with open(os.path.join(self.tmpdir,self.updateFile), 'wb') as file, tqdm(
            desc="update.zip",
            total=total,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for data in resp.iter_content(chunk_size=1024):
                size = file.write(data)
                bar.update(size)

    def __unpackupdate(self):
        with ZipFile(os.path.join(self.tmpdir,self.updateFile), 'r') as zip: 
            print('Extracting all the files now...') 
            zip.extractall(self.tmpdir) 
            print(self.tmpdir)
            print('Done!')

    def __move_file(self, tmpPath: str, installPath: str):
        # print("Moving file from", tmpPath, "->", installPath)
        os.replace(tmpPath, installPath)
        # print("*" * 10)
    
    def __move_data(self):
        print("Listing of files in tmp dir")

        tmpUpdateLocation = os.path.join(self.tmpdir, "NightCAP-dev")
        # installLocation = os.getcwd()
        installLocation = os.path.dirname(__file__).split('/application')[0]

        print(tmpUpdateLocation)
        print(installLocation)
        print(os.path.dirname(__file__).split('/application')[0])

        for path, subdirs, files in os.walk(tmpUpdateLocation):
            for name in files:
                print(os.path.join(path, name)) 
                if str(name).endswith(self._excludeExt):
                   self.excludedPaths.append(os.path.join(path, name))
                else:
                    self.tmpUpdatePaths.append(os.path.join(path, name))
                    

        # print("Tmp path:", tmpUpdateLocation)
        # print(installLocation)
        newPath = lambda s: re.sub(tmpUpdateLocation, installLocation, s)

        # print("Files to move")
        for tpath in self.tmpUpdatePaths:
            self.__move_file(tpath, newPath(tpath))
            
        
    
    def onCloseModifications(self):
        
        tmpUpdateLocation = os.path.join(self.tmpdir, "NightCAP-main")
        installLocation = os.getcwd()
        newPath = lambda s: re.sub(tmpUpdateLocation, installLocation, s)
        
        print("Files to exclude")
        for tpath in self.excludedPaths:
            print(tpath)
            print(newPath(tpath))
            print("*" * 10)

        # Right here is where the excluded json files will need to be merged with the existing files 
        self.__remove_tmp()
