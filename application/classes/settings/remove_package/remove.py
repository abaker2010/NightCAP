# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
from nightcappackages import *
from colorama import Fore, Style
from nightcapcore import *

class NightcapRemovePackage():
    def __init__(self):
        # self.packages_db = NightcapPackages()
        self.printer = Printer()

    def remove_package(self, package_path: str):
        try:
            data = package_path.split("/")
            
            self.printer.print_underlined_header_undecorated(text="UNINSTALLING")
            # self.printer.print_formatted_additional(text="Package:", optionaltext=data[0] + "/" + data[1] + "/" + data[2])

            # dest = ("Package Usage: " + Fore.YELLOW + data[0] + "/" + data[1] + Fore.CYAN).center(75, ' ')
            # pname = ("Package Name: " + Fore.YELLOW + data[2] + Style.RESET_ALL).center(75, ' ')
            
            # self.output.output(("*"*50))
            # self.output.output("UNINSTALLING")
            # self.output.output(("*"*50))


            # self.output.output(pname, color=Fore.CYAN)
            # self.output.output(dest, color=Fore.CYAN)
            # self.output.output(("*"*50))
            NightcapPackageUninstaller(package_path)
            # self.output.output(("*"*50))
        except Exception as e:
            self.printer.print_error(exception=e)
            # self.output.output(("Error uninstalling:" + str(e)), level=6)

    

