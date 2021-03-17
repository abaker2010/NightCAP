# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
from nightcapcli.cmds.cmd_dev_options import NightcapDevOptions
from nightcapcli.cmds.mongo_cmd import NightcapMongoSettingsCMD
from nightcapcli.cmds.django_cmd import NightcapDjangoSettingsCMD
from nightcapcli.generator.listpackages import NightcapListPackages
from nightcapcli.updater.updater import NightcapUpdater
# from nightcapcli.updater.updater import NightcapUpdater
from nightcappackages.classes.helpers.package_installer import NightcapPackageInstallerCommand
from nightcappackages.classes.helpers.package_uninstaller import NightcapPackageUninstallerCommand
from ..base import NightcapBaseCMD
from nightcapcore import *
from colorama import Fore, Style

class NightcapMongoServerSettingsCMD(NightcapBaseCMD):
    def __init__(self, configuration: NightcapCLIConfiguration):
        NightcapBaseCMD.__init__(self,["settings","server"],configuration)

    def help_database(self):
        self.printer.help(text="(Mongo) Database Configurations")

    def do_database(self, line):
        NightcapMongoSettingsCMD(self.config).cmdloop()

    def help_web(self):
        self.printer.help(text="Web Server Configurations")

    def do_web(self, line):
        NightcapDjangoSettingsCMD(self.config).cmdloop()