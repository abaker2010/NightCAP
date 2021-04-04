# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Imports
import os
import json
import hashlib
from nightcapcli.base.base_cmd import NightcapBaseCMD
from nightcapcore.configuration import NightcapCLIConfiguration
from colorama import Fore, Style

# endregion


class NightcapDevOptions(NightcapBaseCMD):
    """
    (User CLI Object)

    This class is used as a child class in the settings for developer options

    ...

    Attributes
    ----------
        ** Not including the ones from NightcapBaseCMD
            selectedList: -> list
                The current selected console path

    Methods
    -------
        Accessible
        -------
            help_genPackageUID(self): -> None
                Override for the genPackageUID commands help

            do_genPackageUID(self, package_path: str): -> None
                this will sign the package that the user passes into the program to be used later for installation

    """

    # region Init
    def __init__(self, selectedList: list):
        self.selectedList = selectedList
        self.selectedList.append("dev")
        NightcapBaseCMD.__init__(self, self.selectedList)

    # endregion

    # region Do genPackageUID
    def do_genPackageUID(self, package_path: str):
        try:
            data = None
            with open(os.path.join(package_path, "package_info.json")) as json_file:
                data = json.load(json_file)
                print(json.dumps(data, indent=4))

            print("\n\nData that we will need")
            package_name = data["package_information"]["package_name"]
            package_module = data["package_for"]["module"]
            package_submodule = data["package_for"]["submodule"]

            package = package_module + "/" + package_submodule + "/" + package_name
            hash = hashlib.sha256(package.encode()).hexdigest()
            print(hash)
            print("\n\n")

            data["package_information"]["uid"] = hash

            print(data)
            with open(os.path.join(package_path, "package_info.json"), "w") as outfile:
                json.dump(data, outfile)

            print("\n\n")
        except Exception as e:
            print(e)

    # endregion

    # region Help genPackageUID
    def help_genPackageUID(self):
        h1 = "Generate UID for custom package:"
        h2 = "\tUsage ~ genPackageUID /path/to/package_info.json"
        # h3 = "set param:\tparams [PARAM] [PARAMVALUE]"
        p = """
         %s 
         %s
        """ % (
            (Fore.GREEN + h1),
            (Fore.YELLOW + h2 + Style.RESET_ALL),
            # (Fore.YELLOW + h3 + Style.RESET_ALL),
        )
        print(p)

    # endregion
