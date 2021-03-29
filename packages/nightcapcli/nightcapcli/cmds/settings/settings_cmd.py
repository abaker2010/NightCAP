# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
from nightcapcli.cmds.cmd_shared.network_config_cmd import NightcapMongoNetworkSettingsCMD
from nightcapcli.base.base_cmd import NightcapBaseCMD
from nightcapcli.cmds.settings.cmd_dev_options import NightcapDevOptions
from nightcapcli.generator.listpackages import NightcapListPackages
from nightcapcli.updater.updater import NightcapUpdater
from nightcappackages.classes.helpers.package_installer import NightcapPackageInstallerCommand
from nightcappackages.classes.helpers.package_uninstaller import NightcapPackageUninstallerCommand
from nightcapcore import *
from colorama import Fore, Style

class NightcapSettingsCMD(NightcapBaseCMD):
    def __init__(self, configuration: NightcapCLIConfiguration):
        NightcapBaseCMD.__init__(self,["settings"],configuration)

    def help_devoptions(self):
        self.printer.help(text="Developer Options")
    #region 
    def do_devoptions(self, line):
        NightcapDevOptions(self.selectedList, self.config).cmdloop()
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
        self.printer.help(text="Install a new module. Formatting for module creation can be found at", optionalText='https://some_url.com')
    #endregion

    #region List Packages
    def help_list(self):
        self.printer.help(text="List installed packages")

    def do_list(self, line):
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
        self.printer.help(text="Uninstall a module example", optionalText='uninstall [package_path]')
    #endregion

    #region Update
    def help_update(self):
        self.printer.help(text="Update the program, if there is no option specified the default will be used.", optionalText='update [main|dev] [-v]')

    def do_update(self, line):
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
    def help_server(self):
        self.printer.help(text='Configure a server')
        self.printer.help(text='Usage: server <web|database>')

    def complete_server(self, text, line, begidx, endidx):
        return [i for i in ('web','database') if i.startswith(text)]

    def do_server(self, line):
        try:
            NightcapMongoNetworkSettingsCMD(line, self.config).cmdloop()
        except Exception as e:
            self.printer.print_error(exception=e)

    #endregion