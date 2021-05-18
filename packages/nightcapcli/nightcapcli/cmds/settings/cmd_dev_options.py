# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Imports
import os
import json
import hashlib
from pathlib import Path
import shutil
from checksumdir import dirhash
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
    def __init__(self, selectedList: list, channelID: str = None):
        self.selectedList = selectedList
        # self.selectedList.append("dev")
        NightcapBaseCMD.__init__(self, self.selectedList, channelid=channelID)

    # endregion

    # region make archive
    def make_archive(self, source, destination):
        base = os.path.basename(destination)
        name = base.split('.')[0]
        format = base.split('.')[1]
        archive_from = os.path.dirname(source)
        archive_to = os.path.basename(source.strip(os.sep))
        shutil.make_archive(name, format, archive_from, archive_to)
        shutil.move('%s.%s'%(name,format), destination)
    # endregion

    # region Do genPackageUID
    def do_genPackageUID(self, package_path: str):
        try:
        
            with open(os.path.join(package_path, "package_info.json")) as json_file:
                data = json.load(json_file)

            package_name = data["package_information"]["package_name"]
            package_module = data["package_for"]["module"]
            package_submodule = data["package_for"]["submodule"]

            package = package_module + "/" + package_submodule + "/" + package_name
            hash = hashlib.sha256(package.encode()).hexdigest()
            data["package_information"]["uid"] = hash
            
            _out_file = package_module + "-" + package_submodule + "-" + package_name + "-" + str(data["package_information"]["version"]).replace('.','-')
            _base = os.path.join(Path(package_path).parent, _out_file)

            with open(os.path.join(package_path, "package_info.json"), "w") as outfile:
                json.dump(data, outfile)

            self.printer.print_underlined_header("Trying to sign package")
            self.printer.print_formatted_additional("Please wait...")
            self.printer.print_formatted_additional("Path to be used", optionaltext=package_path)
            self.printer.print_formatted_additional("Package Being Created", optionaltext=_out_file + ".ncp")

            self.make_archive(package_path, str(_base)+'.zip')
            os.rename(str(_base) + ".zip", str(_base) + ".ncp")
            
            with open(str(_base) + ".ncp", "rb") as f:
                file_hash = hashlib.md5()
                chunk = f.read(8192)
                while chunk:
                    file_hash.update(chunk)
                    chunk = f.read(8192)
            self.printer.print_formatted_check("Done", endingBreaks=1)
            
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
