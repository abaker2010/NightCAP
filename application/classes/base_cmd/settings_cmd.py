# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
from nightcappackages.classes.helpers.package_installer import NightcapPackageInstallerCommand
from nightcappackages.classes.helpers.package_uninstaller import NightcapPackageUninstallerCommand
from application.classes.settings.list_packages.listpackages import NightcapListPackages
from application.classes.base_cmd.base_cmd import NightcapBaseCMD
from application.classes.settings.dev_options.dev_options import NightcapDevOptions
from application.classes.updater.updater import  NightcapUpdater
from application.classes.helpers.screen.screen_helper import ScreenHelper
from nightcapcore import *
from colorama import Fore, Style

class NightcapSettingsCMD(NightcapBaseCMD):
    def __init__(self):
        NightcapBaseCMD.__init__(self,["settings"],None)

    
    #region 
    def do_devoptions(self, line):
        NightcapDevOptions(self.selectedList).cmdloop()
    #endregion

    #region Install
    def do_install(self, line):
        try:
            invoker = Invoker()
            invoker.set_on_start(NightcapPackageInstallerCommand(line))
            invoker.do_something_important()
        except Exception as e:
            self.printer.print_error(exception=e)

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
        '''\nList the packages that are installed\n'''
        ScreenHelper().clearScr()
        NightcapListPackages().list_packages()

    #endregion

    #region Uninstall
    def do_uninstall(self,line):
        try:
            invoker = Invoker()
            invoker.set_on_start(NightcapPackageUninstallerCommand(line))
            invoker.do_something_important()
        except Exception as e:
            self.printer.print_error(exception=e)

    def help_uninstall(self):
        h1 = "Uninstall a module example:"
        h2 = "uninstall [package_name]"
        h = '''
         %s %s
        ''' % ((Fore.GREEN + h1),(Fore.YELLOW + h2 + Style.RESET_ALL))
        print(h)
    #endregion

    #region Update
    def do_update(self, line):
        '''\nUpdate the project. Usage: update [main|dev]. If no option is specified the default will be used.\n'''
        sline = str(line).lstrip().split(' ')
        print("Line: ", str(line).split(" "))
        try:
            if(len(sline) == 1):
                print("No Verbose")
                if(sline[0] == ''):
                    print("using default / no verbose")
                    NightcapUpdater().update(True)
                elif(sline[0] == 'dev'):
                    print("using dev / no verbose")
                    NightcapUpdater().update(False)
                elif(sline[0] == 'main'):
                    print("Using main / no verbose")
                    NightcapUpdater().update(True)
                else:
                    print("Not an option")
            elif(len(sline) == 2):
                print("Verbose")
                if sline[1] == '-v':
                    if(sline[0] == 'dev'):
                        print("using dev / verbose")
                        NightcapUpdater().update(False, True)
                    elif(sline[0] == 'main'):
                        print("Using main / verbose")
                        NightcapUpdater().update(True, True)
                    else:
                        print("Error with verbose")
                else:
                    print("Error with verbose option")
            else:
                print("To many arguments")
        except Exception as e:
            print("Exception:",e)
    #endregion
        
    #region Server config section
    def do_server(self, line):
        print("Server config changes")

    #endregion