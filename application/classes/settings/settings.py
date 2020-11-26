# Copyright 2020 by Aarom Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
from application.classes.settings.list_packages.listpackages import NightcapListPackages
from application.classes.base_cmd.base_cmd import NightcapBaseCMD
from application.classes.helpers.screen.screen_helper import ScreenHelper
from application.classes.settings.install_package.install import NightcapInstallPackage
from application.classes.settings.remove_package.remove import NightcapRemovePackage
from application.classes.settings.dev_options.dev_options import NightcapDevOptions
from colorama import Fore, Style

class NightcapSettings(NightcapBaseCMD):
    def __init__(self):
        NightcapBaseCMD.__init__(self,["settings"], None)

    def do_exit(self,line):
        ScreenHelper().clearScr()
        try:
            self.selectedList.remove(self.selectedList[-1])
        except Exception as e:
            pass
        return True

    #region 
    def do_devoptions(self, line):
        NightcapDevOptions(self.selectedList).cmdloop()
    #endregion

    #region Install
    def do_install(self, line):
        NightcapInstallPackage().install_package(line)

    def help_install(self):
        h1 = "Install a new module. Formatting for module creation can be found at:"
        h2 = "https://some_url.com"
        h = '''
         %s %s
        ''' % ((Fore.GREEN + h1),(Fore.YELLOW + h2 + Style.RESET_ALL))
        print(h)
    #endregion

    #region List Packages
    def do_list(self, line):
        NightcapListPackages().list_packages()

    #endregion

    #region Uninstall
    def do_uninstall(self,line):
        print("Uninstall module:",line)
        NightcapRemovePackage().remove_package(line)

    def help_uninstall(self):
        h1 = "Uninstall a module example:"
        h2 = "uninstall [package_name]"
        h = '''
         %s %s
        ''' % ((Fore.GREEN + h1),(Fore.YELLOW + h2 + Style.RESET_ALL))
        print(h)
    #endregion
        