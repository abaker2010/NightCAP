# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Imports
from nightcapcore.command.command import Command
from colorama import Fore
from nightcapcore import Printer
from tqdm.auto import tqdm
import requests
import os
from nightcappackages import *
# endregion

class NightcapPackageUpdateDownloaderHelper(Command):
    # region Init
    def __init__(self, url: str, tmppath: str, filename: str = "update.ncb", verbose: bool = False):
        self.printer = Printer()
        self.verbose = verbose
        self.url = url
        self.filename = filename
        self.tmppath = tmppath

    def execute(self) -> None:
        
        try:
            if self.verbose:
                self.printer.item_1("Downloading Update")
                self.printer.print_header(
                    "Progress", leadingText="[+]", leadingBreaks=1, endingBreaks=1)
            resp = requests.get(
                self.url, stream=True
            )
            total = int(resp.headers.get("content-length", 0))

            description = (
                Fore.LIGHTMAGENTA_EX + "\t[-] Downloading "
            )
            with open(os.path.join(self.tmppath, self.filename), "wb") as file, tqdm(
                desc=description,
                total=total,
                unit="iB",
                unit_scale=True,
                unit_divisor=1024,
                ncols = 100
            ) as bar:
                for data in resp.iter_content(chunk_size=1024):
                    size = file.write(data)
                    bar.update(size)

            return (True, self.tmppath, self.filename)
        except Exception as e:
            self.printer.print_error(e)
            raise e

    
        

    