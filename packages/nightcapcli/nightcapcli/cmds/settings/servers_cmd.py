# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
from nightcapcli.base.base_cmd import NightcapBaseCMD
from nightcapcli.cmds.settings import NightcapMongoSettingsCMD
from nightcapcli.cmds.settings.django_cmd import NightcapDjangoSettingsCMD
from nightcapcore.configuration import NightcapCLIConfiguration


class NightcapMongoServerSettingsCMD(NightcapBaseCMD):
    def __init__(self, configuration: NightcapCLIConfiguration):
        NightcapBaseCMD.__init__(self, ["settings", "server"])

    def help_database(self):
        self.printer.help("(Mongo) Database Configurations")

    def do_database(self, line):
        NightcapMongoSettingsCMD().cmdloop()

    def help_web(self):
        self.printer.help("Web Server Configurations")

    def do_web(self, line):
        NightcapDjangoSettingsCMD().cmdloop()
