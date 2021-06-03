# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Imports
from nightcappackages import *
from nightcapcore import Printer
from colorama import Fore, Style
from nightcappackages.classes.databases.mogo.mongo_modules import MongoModuleDatabase
from nightcappackages.classes.databases.mogo.mongo_packages import MongoPackagesDatabase
from nightcappackages.classes.databases.mogo.mongo_submodules import (
    MongoSubModuleDatabase,
)

# endregion


class NightcapOptionGenerator(object):
    """

    This class is used to help validate user input to the console

    ...

    Attributes
    ----------
        selectedList: -> list:
            Used for the current path of the program

        printer: -> Printer
            Allows access to the console printer


    Methods
    -------
        Accessible
        -------
            completed_options(self): -> list
                Tab auto complete for the options at the current path

            options(self, isDetailed=False): -> None
                This is used to select an option or to get the list of options that are available to be used

            option_help(self): -> None
                Override for the options help


        None Accessible
        -------


    """

    # region Init
    def __init__(self, selectedList) -> None:
        super().__init__()
        self.selectedList = selectedList
        self.printer = Printer()

    # endregion

    # region Tab options complete
    def completed_options(self) -> list:
        vals = []
        # print("List to use to find m/sm/p:", self.selectedList)

        if len(self.selectedList) == 0:
            # print("finding options")
            vals = list(
                map(lambda v: v["type"], MongoModuleDatabase().get_all_modules())
            )
        elif len(self.selectedList) == 1:
            # print("finding with", self.selectedList)
            vals = list(
                map(
                    lambda v: v["type"],
                    MongoSubModuleDatabase().find_submodules(self.selectedList[0]),
                )
            )
        elif len(self.selectedList) == 2:
            # print("Trying to find submodule options")
            vals = MongoPackagesDatabase().packages(self.selectedList, False)
        else:
            print("should be for packages")

        _cvals = []
        if len(vals) == 0:
            _cvals.append("No Pacakges Installed")
        else:
            # if(isDetailed):
            #     for v in vals:
            #         print("\t", v)
            # else:
            #     _join = Fore.YELLOW + " | " + Style.RESET_ALL
            #     _vals = list(map(lambda v: Fore.CYAN + v + Style.RESET_ALL, vals))
            if len(vals) != 0:
                for v in vals:
                    _cvals.append(v)
        return _cvals

    # endregion

    # region Options
    def options(self, isDetailed=False) -> None:

        vals = []
        opt = True
        # print("List to use to find m/sm/p:", self.selectedList)

        if len(self.selectedList) == 0:
            # print("finding options")
            vals = list(
                map(
                    lambda v: v["type"]
                    + Fore.LIGHTMAGENTA_EX
                    + " ("
                    + str(
                        NightcapInstalledPackageCounter().count_from_selected_module(
                            v["type"]
                        )
                    )
                    + ")"
                    + Style.RESET_ALL,
                    MongoModuleDatabase().get_all_modules(),
                )
            )
        elif len(self.selectedList) == 1:
            # print("finding with", self.selectedList)
            vals = list(
                map(
                    lambda v: v["type"]
                    + Fore.LIGHTMAGENTA_EX
                    + " ("
                    + str(
                        NightcapInstalledPackageCounter().count_from_selected_submodule(
                            self.selectedList[0], v["type"]
                        )
                    )
                    + ")"
                    + Style.RESET_ALL,
                    MongoSubModuleDatabase().find_submodules(self.selectedList[0]),
                )
            )
        elif len(self.selectedList) == 2:
            # print("Trying to find submodule options")
            vals = MongoPackagesDatabase().packages(self.selectedList, isDetailed)
        else:
            print("should be for packages")

        _cvals = []
        if len(vals) == 0:
            _cvals.append("No Pacakges Installed")
        else:
            if isDetailed:
                for v in vals:
                    print("\t", v)
            else:
                _join = Fore.YELLOW + " | " + Style.RESET_ALL
                _vals = list(map(lambda v: Fore.CYAN + v + Style.RESET_ALL, vals))
                if len(vals) != 0:
                    if len(vals) > 1:
                        for v in _vals:
                            _cvals.append(v)
                            _cvals.append(_join)
                        _cvals = _cvals[:-1]
                    else:
                        for v in _vals:
                            _cvals.append(v)

        self.printer.item_1(
            "".join(_cvals), "", leadingTab=1, leadingText="", vtabs=1, endingBreaks=1, seperator=''
        )

    # endregion

    # region Options Help
    def option_help(self) -> None:
        print(
            """
        Modules that are available to use to investigate pcap files.
        View modules using the 'options' command
            Optional detailed view with command: options detailed
        
            ~ Usage: use [module]
        """
        )

    # endregion
