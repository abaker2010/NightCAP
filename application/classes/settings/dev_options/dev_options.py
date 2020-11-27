# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
import os
import json
import hashlib
from application.classes.base_cmd.base_cmd import NightcapBaseCMD
from application.classes.helpers.screen.screen_helper import ScreenHelper
from application.classes.settings.install_package.install import NightcapInstallPackage
from application.classes.settings.remove_package.remove import NightcapRemovePackage
from colorama import Fore, Style

class NightcapDevOptions(NightcapBaseCMD):
    def __init__(self,selectedList: list):
        self.selectedList = selectedList
        self.selectedList.append("dev")
        NightcapBaseCMD.__init__(self,self.selectedList)

    def do_exit(self,line):
        ScreenHelper().clearScr()
        try:
            self.selectedList.remove(self.selectedList[-1])
        except Exception as e:
            pass
        return True

    #region 
    def do_genPackageUID(self,package_path: str):
        data = None
        with open(os.path.join(package_path, "package_info.json")) as json_file:
            data = json.load(json_file)
            print(json.dumps(data, indent=4))

        print("\n\nData that we will need")
        package_name = data["package_information"]["package_name"]
        package_module = data["package_for"]["module"]
        package_submodule = data["package_for"]["submodule"]

        package = (package_module + "/" + package_submodule + "/" + package_name)
        hash = hashlib.sha256(package.encode()).hexdigest()
        print(hash)
        print("\n\n")

        data["package_information"]["uid"] = hash

        print(data)
        with open(os.path.join(package_path, "package_info.json"), 'w') as outfile:
            json.dump(data, outfile)

        print("\n\n")


    def help_genPackageUID(self):
        h1 = "Generate UID for custom package:"
        h2 = "\tUsage ~ genPackageUID /path/to/package_info.json"
        # h3 = "set param:\tparams [PARAM] [PARAMVALUE]"
        p = '''
         %s 
         %s
        ''' % (
            (Fore.GREEN + h1),
            (Fore.YELLOW + h2 + Style.RESET_ALL),
            # (Fore.YELLOW + h3 + Style.RESET_ALL),
            )
        print(p)
    #endregion 