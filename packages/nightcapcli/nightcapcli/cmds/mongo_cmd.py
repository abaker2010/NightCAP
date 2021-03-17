# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
from nightcapcli.cmds.cmd_dev_options import NightcapDevOptions
from nightcapcli.cmds.cmd_shared.network_config_cmd import NightcapMongoNetworkSettingsCMD
from nightcapcli.generator.listpackages import NightcapListPackages
from nightcapcli.updater.updater import NightcapUpdater
# from nightcapcli.updater.updater import NightcapUpdater
from nightcappackages.classes.helpers.package_installer import NightcapPackageInstallerCommand
from nightcappackages.classes.helpers.package_uninstaller import NightcapPackageUninstallerCommand
from ..base import NightcapBaseCMD
from nightcapcore import *
from colorama import Fore, Style

class NightcapMongoSettingsCMD(NightcapMongoNetworkSettingsCMD):
    def __init__(self, configuration: NightcapCLIConfiguration):
        NightcapMongoNetworkSettingsCMD.__init__(self, 'database', configuration)