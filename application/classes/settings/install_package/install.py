# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
from application.classes.helpers.screen.screen_helper import ScreenHelper
import os
import json
from nightcapcore.printers.print import Printer
from nightcappackages import *
from colorama import Fore, Style
from nightcapcore import *

class NightcapInstallPackage():
    def __init__(self):
        self.packages_db = NightcapPackages()
        self.printer = Printer()

    def install_package(self, package_path: str):
        try:
            data = None
            with open(os.path.join(package_path, "package_info.json")) as json_file:
                data = json.load(json_file)

            # dest = ("Package Usage: " + Fore.YELLOW + data["package_for"]["module"] + "/" + data["package_for"]["submodule"] + Fore.CYAN).center(75, ' ')
            # pname = ("Package Name: " + Fore.YELLOW + data["package_information"]["package_name"] + Style.RESET_ALL).center(75, ' ')
            
            ScreenHelper().clearScr()
            self.printer.print_underlined_header_undecorated(text="INSTALLING")
            self.printer.print_formatted_additional(text="Package: " + data["package_for"]["module"] + "/" + data["package_for"]["submodule"] + "/" + data["package_information"]["package_name"])

            NightcapPackageInstaller(data, package_path)
        except FileNotFoundError as nf:
            self.printer.print_error(exception=nf)
        except Exception as e:
            self.printer.print_error(exception=e)

    