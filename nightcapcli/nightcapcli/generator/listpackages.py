# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Imports
from nightcappackages import *
from colorama import Fore, Style
from nightcapcore import *
from nightcappackages.classes.databases.mogo.mongo_packages import MongoPackagesDatabase

# endregion


class NightcapListPackages(object):
    """

    This class is used to print the installed packages

    ...

    Attributes
    ----------
        packages_db: -> MongoPackagesDatabase
            Allows access to the MongoPackagesDatabase

        priner: -> Printer
            Allows access to the console printer


    Methods
    -------
        Accessible
        -------
            list_packages(self): -> None
                Prints the installed packages to the user

    """

    # region Init
    def __init__(self) -> None:
        super().__init__()
        self.packages_db = MongoPackagesDatabase()
        self.priner = Printer()

    # endregion

    # region List Packages
    def list_packages(self) -> None:
        # print("\n\t\tInstalled packages")
        # print("\t\t", "-" * 20, "\n", sep="")
        self.priner.print_underlined_header_undecorated(
            "Installed Packages", endingBreaks=1
        )
        _packages = list(map(lambda v: v, self.packages_db.get_all_packages()))
        if _packages == []:
            # print(Fore.YELLOW + "\t\tNo Packages Installed\n", Style.RESET_ALL)
            self.priner.print_error(Exception("No Packages Installed"))
        else:
            for p in _packages:
                print(
                    Fore.YELLOW,
                    "\t- ",
                    p["package_for"]["module"],
                    "/",
                    p["package_for"]["submodule"],
                    "/",
                    p["package_information"]["package_name"],
                    Fore.LIGHTCYAN_EX,
                    "\tver: ",
                    p["package_information"]["version"],
                    Fore.LIGHTMAGENTA_EX,
                    "  author: ",
                    p["author_info"]["creator"],
                    sep="",
                )
                self.priner.item_3(
                    p["package_information"]["details"],
                    endingBreaks=1,
                    leadingTab=2,
                    leadingText="[?] - ",
                )
                # print(Fore.GREEN, "\t\t", p["package_information"]["details"], "\n")

    # endregion
