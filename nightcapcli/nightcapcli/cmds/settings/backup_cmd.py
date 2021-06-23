# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Imports
from nightcappackages.classes.helpers import (
    NightcapBackupHelper,
    NightcapRestoreHelper,
    NightcapCleanHelper,
)
from nightcapcli.base import NightcapBaseCMD

# endregion


class NightcapBackups(NightcapBaseCMD):
    def __init__(self, selectedList: list, channelid):
        super().__init__(selectedList, channelid=channelid)

    # region Backup
    def help_backup(self) -> None:
        self.printer.help("Backup your instance of the NightCAP program")
        self.printer.help("useage: backup <output location>")

    def do_backup(self, line) -> None:
        NightcapBackupHelper(line).backup()

    # region Restore
    def help_restore(self) -> None:
        self.printer.help("Restore your instance of the NightCAP program from a backup")
        self.printer.help("useage: restore <output location>.ncb")

    def do_restore(self, line) -> None:
        NightcapRestoreHelper(str(line)).restore()

    def do_clean(self, line) -> None:
        NightcapCleanHelper().clean()
