# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
#region Imports
import os
import sys
from nightcapcli.cmds.cmd_shared.network_config_cmd import (
    NightcapMongoNetworkSettingsCMD,
)
from nightcapcli.base.base_cmd import NightcapBaseCMD
from nightcapcli.cmds.settings.cmd_dev_options import NightcapDevOptions
from nightcapcli.generator.listpackages import NightcapListPackages
from nightcapcli.updater.updater import NightcapUpdater
from nightcappackages.classes.helpers.package_installer import (
    NightcapPackageInstallerCommand,
)
from nightcappackages.classes.helpers.package_uninstaller import (
    NightcapPackageUninstallerCommand,
)
from nightcapcore import *
#endregion

class NightcapSettingsCMD(NightcapBaseCMD):
    """
        (User CLI Object)
        
        This class is used as the cli for the user settings

        ...

        Attributes
        ----------


        Methods 
        -------
            Accessible 
            -------

                help_devoptions(self): -> None
                    Override for the devoptions help command

                do_devoptions(self, line): -> None
                    Allows the user to enter into the devoptions cmd

                help_install(self): -> None  
                    Override for the install help command

                do_install(self, line): -> None         
                    Allows the user to install new packages

                help_list(self): -> None
                    Override for the list help command

                do_list(self, line): -> None
                    Lists all of the packages installed 

                help_uninstall(self): -> None
                    Override for the uninstall help command

                do_uninstall(self, line): -> None
                    Uninstall a package based on the path passed in

                help_update(self): -> None
                    Override for the update help command

                do_update(self, line): -> None
                    Allows the user to update the program Dev/Main

                complete_server(self, text, line, begidx, endidx): -> None
                    Tab auto compelete options for the server command

                help_server(self): -> None
                    Override for the server help command

                do_server(self, line): -> None
                    Allows the user to enter into the server cmd 

                complete_verbosity(self, text, line, begidx, endidx): -> None
                    Tab auto complete options for the verbosity command

                help_verbosity(self): -> None
                    Override for the verbose help command

                do_verbosity(self, line): -> None
                    Allows the user to change the verbostiy of the output shown in the console

    """
    #region Init
    def __init__(self):
        NightcapBaseCMD.__init__(self, ["settings"])
    #endregion

    #region Dev Options
    def help_devoptions(self):
        self.printer.help("Developer Options")

    def do_devoptions(self, line):
        NightcapDevOptions(self.selectedList).cmdloop()

    # endregion

    # region Install
    def do_install(self, line):
        try:
            invoker = Invoker()
            invoker.set_on_start(NightcapPackageInstallerCommand(line))
            invoker.do_something_important()
        except Exception as e:
            self.printer.print_error(e)

    def help_install(self):
        self.printer.help(
            "Install a new module. Formatting for module creation can be found at",
            "https://some_url.com",
        )

    # endregion

    # region List Packages
    def help_list(self):
        self.printer.help("List installed packages")

    def do_list(self, line):
        ScreenHelper().clearScr()
        NightcapListPackages().list_packages()

    # endregion

    # region Uninstall
    def do_uninstall(self, line):
        try:
            invoker = Invoker()
            invoker.set_on_start(NightcapPackageUninstallerCommand(line))
            invoker.do_something_important()
        except Exception as e:
            self.printer.print_error(e)

    def help_uninstall(self):
        self.printer.help(
            "Uninstall a module example", "uninstall [package_path]"
        )

    # endregion

    # region Update
    def help_update(self):
        self.printer.help(
            "Update the program, if there is no option specified the default will be used.",
            "update [main|dev] [-v]",
        )

    def do_update(self, line):
        sline = str(line).lstrip().split(" ")
        print("Line: ", str(line).split(" "))
        try:
            if len(sline) == 1:
                print("No Verbose")
                if sline[0] == "":
                    print("using default / no verbose")
                    NightcapUpdater().update(True)
                elif sline[0] == "dev":
                    print("using dev / no verbose")
                    NightcapUpdater().update(False)
                elif sline[0] == "main":
                    print("Using main / no verbose")
                    NightcapUpdater().update(True)
                else:
                    print("Not an option")
            elif len(sline) == 2:
                print("Verbose")
                if sline[1] == "-v":
                    if sline[0] == "dev":
                        print("using dev / verbose")
                        NightcapUpdater().update(False, True)
                    elif sline[0] == "main":
                        print("Using main / verbose")
                        NightcapUpdater().update(True, True)
                    else:
                        print("Error with verbose")
                else:
                    print("Error with verbose option")
            else:
                print("To many arguments")
        except Exception as e:
            print("Exception:", e)

    # endregion
  
    #region Verbosity
    def complete_verbosity(self, text, line, begidx, endidx):
        return [i for i in ("normal", "debug") if i.startswith(text)]

    def help_verbosity(self):
        self.printer.help("Configure verbosity level", endingBreaks=0)
        self.printer.help("Usage: verbosity <normal|debug>",leadingBreaks=0)

    def do_verbosity(self, line):
        print("change the verbosity")
        try:
            if line != '':
                if 'normal' == str(line).lower().strip():
                    print("set to normal")
                    self.verbosity = False
                    self.config.config.set('NIGHTCAPCORE', "verbose", "false")
                    self.config.Save()
                elif 'debug' == str(line).lower().strip():
                    print("set to debug")
                    self.verbosity = True
                    self.config.config.set('NIGHTCAPCORE', "verbose", "true")
                    self.config.Save()
            else:
                raise Exception("Error with level, for more information use: help verbosity")
            
            self.printer.print_formatted_additional(text="Rebooting...")
            os.execv(sys.argv[0], sys.argv)
        except Exception as e:
            self.printer.print_error(e)
            
    #endregion

    # region Server config section
    def complete_server(self, text, line, begidx, endidx):
        return [i for i in ("web", "database") if i.startswith(text)]

    def help_server(self):
        self.printer.help("Configure a server")
        self.printer.help("Usage: server <web|database>")

    def do_server(self, line):
        try:
            NightcapMongoNetworkSettingsCMD(line).cmdloop()
        except Exception as e:
            self.printer.print_error(e)

    # endregion
