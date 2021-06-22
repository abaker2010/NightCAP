# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Imports
from nightcapcli.base.base_cmd import NightcapBaseCMD
from nightcapcli.cmds.settings import (
    NightcapMongoSettingsCMD,
    NightcapDjangoSettingsCMD,
)
from nightcapcore.configuration import NightcapCLIConfiguration

# endregion


class NightcapMongoServerSettingsCMD(NightcapBaseCMD):
    """

    This class is used control the Django Docker container

    ...

    Methods
    -------
        Accessible
        -------
            help_database(self): -> None
                Overrides the Database commands help option

            do_database(self, line): -> None
                Allows the user to enter in to the databse cmd

            help_web(self): -> None
                Overrides the Web commands help option

            do_web(self, line): -> None
                Allows the user to enter in to the web cmd
    """

    def __init__(self, configuration: NightcapCLIConfiguration) -> None:
        NightcapBaseCMD.__init__(self, ["settings", "server"])

    def help_database(self) -> None:
        self.printer.help("(Mongo) Database Configurations")

    def do_database(self, line) -> None:
        NightcapMongoSettingsCMD().cmdloop()

    def help_web(self) -> None:
        self.printer.help("Web Server Configurations")

    def do_web(self, line) -> None:
        NightcapDjangoSettingsCMD().cmdloop()
