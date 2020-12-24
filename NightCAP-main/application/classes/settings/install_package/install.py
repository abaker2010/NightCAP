# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
import os
import json
from nightcappackages import *
from colorama import Fore, Style
from nightcapcore import *

class NightcapInstallPackage():
    def __init__(self):
        self.packages_db = NightcapPackages()
        self.output = NightcapCoreConsoleOutput()

    def install_package(self, package_path: str):
        try:
            data = None
            with open(os.path.join(package_path, "package_info.json")) as json_file:
                data = json.load(json_file)

            dest = ("Package Usage: " + Fore.YELLOW + data["package_for"]["module"] + "/" + data["package_for"]["submodule"] + Fore.CYAN).center(75, ' ')
            pname = ("Package Name: " + Fore.YELLOW + data["package_information"]["package_name"] + Style.RESET_ALL).center(75, ' ')
            
            self.output.output(("*"*50))
            self.output.output(("INSTALLING"), color=Fore.LIGHTYELLOW_EX)
            self.output.output(("*"*50))
            self.output.output(pname, color=Fore.CYAN)
            self.output.output(dest, color=Fore.CYAN)
            self.output.output(("*"*50))
            NightcapPackageInstaller(data, package_path)
            self.output.output(("*"*50))
        except FileNotFoundError as nf:
            self.output.output("Error installing: Package not found", level=6)
        except Exception as e:
            self.output.output(("Error installing:" + str(e)), level=6)

    