# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
from colorama import Fore, Style
# from tqdl import download
import requests
from tqdm.auto import tqdm
import tempfile
import shutil

class NightcapUpdater:
    def __init__(self):
        print("Calling update for system")
        self.tmpdir = None
    
    def update(self):
        try:
            self.__create_tmp()
            self.__get_update()
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
        with open(self.tmpdir + "update.zip", 'wb') as file, tqdm(
            desc="update.zip",
            total=total,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for data in resp.iter_content(chunk_size=1024):
                size = file.write(data)
                bar.update(size)


    # def __get_update(self):
    #     try:
    #         print("Downloading Update")
    #         print("Tmp Folder: ", self.tmpdir)
    #         download("https://github.com/abaker2010/NightCAP/archive/main.zip", self.tmpdir + "update.zip")
    #         # response = requests.get("https://github.com/abaker2010/NightCAP/archive/main.zip")
    #     except Exception as err:
    #         print(f'Other error occurred: {err}')  # Python 3.6
    #     else:
    #         print("Download completed successfully!")
        # for url in ['https://api.github.com', 'https://api.github.com/invalid']:
        #     try:
        #         response = requests.get(url)

        #         # If the response was successful, no Exception will be raised
        #         response.raise_for_status()
            # except HTTPError as http_err:
            #     print(f'HTTP error occurred: {http_err}')  # Python 3.6
            # except Exception as err:
            #     print(f'Other error occurred: {err}')  # Python 3.6
        #     else:
        #         print('Success!')

