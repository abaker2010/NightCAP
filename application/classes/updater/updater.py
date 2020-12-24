# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
from colorama import Fore, Style
# from tqdl import download
import requests
from tqdm.auto import tqdm
from zipfile import ZipFile
import os
import tempfile
import shutil

class NightcapUpdater:
    def __init__(self):
        print("Calling update for system")
        self.tmpdir = None
        self.currentDir = os.getcwd()
        self.updateFile = os.path.join("" if self.tmpdir == None else self.tmpdir, "update.zip")
    
    def update(self):
        try:
            self.__create_tmp()
            self.__get_update()
            self.__unpackupdate()
            self.__move_data()
            self.__remove_tmp()
        except KeyboardInterrupt as e:
            print("User terminated")
            self.__remove_tmp()

    def __create_tmp(self):
        self.tmpdir = tempfile.mkdtemp()
        print("Creating tmp dir: ", self.tmpdir)

    def __remove_tmp(self):
        print("Removing tmp dir")
        shutil.rmtree(self.tmpdir)

    def __get_update(self):
        resp = requests.get("https://github.com/abaker2010/NightCAP/archive/main.zip", stream=True)
        total = int(resp.headers.get('content-length', 0))
        with open(self.updateFile, 'wb') as file, tqdm(
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
        with ZipFile(self.updateFile, 'r') as zip: 
            # printing all the contents of the zip file 
            zip.printdir() 
            # extracting all the files 
            print('Extracting all the files now...') 
            zip.extractall() 
            print('Done!') 
    
    def __move_data(self):
        print("Moving file from update")
        
