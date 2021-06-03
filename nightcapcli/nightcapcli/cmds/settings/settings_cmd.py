# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Imports
from typing import List
from nightcapcli.cmds.settings.servers_cmd import NightcapMongoServerSettingsCMD
from nightcapcli.cmds.settings.network_cmd import NightcapNetworkCMD
from nightcapcli.cmds.settings.backup_cmd import NightcapBackups
from nightcapcli.base.base_cmd import NightcapBaseCMD
from nightcapcli.cmds.settings.cmd_dev_options import NightcapDevOptions
from nightcapcli.generator.listpackages import NightcapListPackages
from nightcappackages.classes.commands import NightcapPackageInstallerCommand, NightcapPackageUninstallerCommand, NightcapUpdaterRebootCommand, NightcapPackageUpdaterCommand
from nightcapcore.invoker import Invoker
from nightcapcore.helpers import ScreenHelper

# endregion


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

    # region Init
    def __init__(self, channelID: str = None) -> None:
        NightcapBaseCMD.__init__(self, ["settings"], channelid=channelID)

    # endregion

    # region Networking Options
    def help_network(self) -> None:
        self.printer.help("Select the protocol to use for requests")

    def do_network(self, line) -> None:
        NightcapNetworkCMD("networking-main").cmdloop()

    # endregion

    # region Dev Options
    def help_backups(self) -> None:
        self.printer.help("Backup/Restore options for your instance of the NightCAP DB")

    def do_backups(self, line) -> None:
        NightcapBackups(["settings", "backups"], "backups-main").cmdloop()

    # endregion


    # region Dev Options
    def help_devoptions(self) -> None:
        self.printer.help("Developer Options")

    def do_devoptions(self, line) -> None:
        NightcapDevOptions(["settings", "dev"], "devoptions").cmdloop()

    # endregion

    # region Install
    def do_install(self, line) -> None:
        try:
            invoker = Invoker()
            invoker.set_on_start(NightcapPackageInstallerCommand(line))
            invoker.execute()
        except Exception as e:
            self.printer.print_error(e)

    def help_install(self) -> None:
        self.printer.help(
            "Install a new module. Formatting for module creation can be found at",
            "https://some_url.com",
        )

    # endregion

    # region List Packages
    def help_list(self) -> None:
        self.printer.help("List installed packages")

    def do_list(self, line) -> None:
        ScreenHelper().clearScr()
        NightcapListPackages().list_packages()

    # endregion

    # region Uninstall
    def do_uninstall(self, line) -> None:
        try:
            invoker = Invoker()
            invoker.set_on_start(NightcapPackageUninstallerCommand(line))
            invoker.execute()
        except Exception as e:
            self.printer.print_error(e)

    def help_uninstall(self) -> None:
        self.printer.help("Uninstall a module example", "uninstall [package_path]")

    # endregion

    # region Update
    def help_update(self) -> None:
        self.printer.help(
            "Update the program, if there is no option specified the default will be used.",
            "update [main|dev] [-v]",
        )

    def complete_update(self, text, line, begidx, endidx) -> None:
        _ = ["dev", "main"]
        return [i for i in _ if i.startswith(text)]

    def do_update(self, line) -> None:
        sline = str(line).lstrip().split(" ")
        invoker = Invoker()
        invoker.set_on_finish(NightcapUpdaterRebootCommand())
        
        try:
            if len(sline) == 1:
                # print("No Verbose")
                if sline[0] == "":
                    # print("using default / no verbose")
                    invoker.set_on_start(NightcapPackageUpdaterCommand(self.config, True))
                elif sline[0] == "dev":
                    # print("using dev / no verbose")
                    invoker.set_on_start(NightcapPackageUpdaterCommand(self.config, False))
                elif sline[0] == "main":
                    # print("Using main / no verbose")
                    invoker.set_on_start(NightcapPackageUpdaterCommand(self.config, True))
                else:
                    self.printer.print_error(Exception("Option not allowed"))
                invoker.execute()
            elif len(sline) == 2:
                # print("Verbose")
                if sline[1] == "-v":
                    if sline[0] == "dev":
                        # print("using dev / verbose")
                        invoker.set_on_start(NightcapPackageUpdaterCommand(self.config, False, True))
                    elif sline[0] == "main":
                        # print("Using main / verbose")
                        invoker.set_on_start(NightcapPackageUpdaterCommand(self.config, True, True))
                    else:
                        self.printer.print_error(Exception("Error processing verbose output"))
                else:
                    self.printer.print_error(Exception("Error with verbose option"))
                invoker.execute()
            else:
                self.printer.print_error(Exception("To many arguments"))

        except Exception as e:
            if e.args[0] == "Restarting":
                raise KeyboardInterrupt('Restarting')
            else:
                self.printer.print_error(e)
    # endregion

    # region Verbosity
    def complete_verbosity(self, text, line, begidx, endidx) -> List[str]:
        return [i for i in ("normal", "debug") if i.startswith(text)]

    def help_verbosity(self) -> None:
        self.printer.help("Configure verbosity level", endingBreaks=0)
        self.printer.help("Usage: verbosity <normal|debug>", leadingBreaks=0)

    def do_verbosity(self, line) -> None:
        try:
            if line != "":
                if "normal" == str(line).lower().strip():
                    self.config.verbosity = False
                    self.config.config.set('NIGHTCAPCORE', 'verbose', 'False')
                elif "debug" == str(line).lower().strip():
                    self.config.verbosity = True
                    self.config.config.set('NIGHTCAPCORE', 'verbose', 'True')
                self.config.Save()
            else:
                raise Exception(
                    "Error with level, for more information use: help verbosity"
                )
        except Exception as e:
            self.printer.print_error(e)

    # endregion

    # region Server config section
    def complete_server(self, text, line, begidx, endidx) -> List[str]:
        return [i for i in ("web", "database") if i.startswith(text)]

    def help_server(self) -> None:
        self.printer.help("Configure a server")
        self.printer.help("Usage: server <web|database>")

    def do_server(self, line) -> None:
        try:
            NightcapMongoServerSettingsCMD(line).cmdloop()
        except Exception as e:
            self.printer.print_error(e)

    # endregion

    #region Exit
    def do_exit(self, line) -> bool:
        return True
    #endregion