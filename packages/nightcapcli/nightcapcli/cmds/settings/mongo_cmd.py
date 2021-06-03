# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Imports
from nightcapcli.cmds.cmd_shared.network_config_cmd import NightcapMongoNetworkSettingsCMD
# endregion

class NightcapMongoSettingsCMD(NightcapMongoNetworkSettingsCMD):
    """
    (User CLI Object)

    This class is used as a wrapper for the network settings object but to be specified for the MongoDB Settings

    """

    def __init__(self) -> None:
        NightcapMongoNetworkSettingsCMD.__init__(self, "database")
