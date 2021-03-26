# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
from nightcapcli.cmds.cmd_shared.network_config_cmd import NightcapMongoNetworkSettingsCMD
from nightcapcore import *

class NightcapDjangoSettingsCMD(NightcapMongoNetworkSettingsCMD):
    def __init__(self, configuration: NightcapCLIConfiguration):
        NightcapMongoNetworkSettingsCMD.__init__(self, 'web', configuration)
