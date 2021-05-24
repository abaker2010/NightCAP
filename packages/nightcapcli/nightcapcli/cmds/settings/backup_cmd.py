# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Imports
import json
from nightcappackages.classes.helpers.backup import NightcapBackupHelper
from nightcappackages.classes.helpers.restore import NightcapRestoreHelper
from nightcappackages.classes.helpers.clean import NightcapCleanHelper
# from nightcapcli.helpers.restore import NightcapRestoreHelper
# from nightcapcli.helpers.backup import NightcapBackupHelper
# from nightcapcli.helpers.clean import NightcapCleanHelper
from bson.objectid import ObjectId
from nightcapcli.base.base_cmd import NightcapBaseCMD
# endregion

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


class NightcapBackups(NightcapBaseCMD):
    def __init__(self, selectedList: list, channelid):
        super().__init__(selectedList, channelid=channelid)
        
    # region Backup
    def help_backup(self):
        self.printer.help("Backup your instance of the NightCAP program")
        self.printer.help("useage: backup <output location>")

    def do_backup(self, line):
        NightcapBackupHelper(line).backup()

    #region Restore
    def help_restore(self):
        self.printer.help("Restore your instance of the NightCAP program from a backup")
        self.printer.help("useage: restore <output location>.ncb")

    def do_restore(self, line):
        NightcapRestoreHelper(str(line)).restore()

    def do_clean(self, line):
        NightcapCleanHelper().clean()
        