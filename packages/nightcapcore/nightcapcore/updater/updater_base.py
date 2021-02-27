# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
from nightcapcore.printers import Printer
from nightcapcore.updater import NightcapCoreUpaterRules
from tinydb import TinyDB, Query
from tinydb.queries import where
from tinydb.table import Table

class NightcapCoreUpdaterBase:
    def __init__(self):
        self.printer = Printer()
        pass

    def _insert(self, localtable: Table, item: dict):
        try:
            localtable.insert(item)
            self.printer.print_formatted_check(text="added", leadingTab=4)
        except Exception as e:
            self.printer.print_error(e, optionalText="Error with inserting: ")

    def _find_module_item(self, localtable: Table, find: str, checkonrow: str):
        _v = localtable.search(Query()[checkonrow] == find)
        return _v

    def _find_submodule_item(self, localtable: Table, find: str, findtwo: str, checkonrow: str, checkonrowtwo: str):
        _v = localtable.search((where(checkonrow) == find) & (where(checkonrowtwo) == findtwo))
        return _v

    def update(self, updatetable: TinyDB, localtable: TinyDB, checkonrow: str, updaterrule: NightcapCoreUpaterRules, checkonrowtwo: str = None):
        for _upditem in updatetable.all():
            _found = None
            if updaterrule == NightcapCoreUpaterRules.Module:
                _found = self._find_module_item(localtable, _upditem[checkonrow], checkonrow)
            elif updaterrule == NightcapCoreUpaterRules.Submodule:
                _found = self._find_submodule_item(localtable=localtable, find=_upditem[checkonrow], findtwo=_upditem[checkonrowtwo], checkonrow=checkonrow, checkonrowtwo=checkonrowtwo)
            elif updaterrule == NightcapCoreUpaterRules.Package:
                _found = self._find_module_item(localtable, _upditem[checkonrow], checkonrow)

            try:
                if _found == []:
                    if updaterrule == NightcapCoreUpaterRules.Package:
                        self.printer.print_formatted_additional(text=str(_upditem[checkonrow][checkonrowtwo]), leadingTab=3)
                        self._insert(localtable, _upditem)
                    elif updaterrule == NightcapCoreUpaterRules.Module:
                        self.printer.print_formatted_additional(text=str(_upditem[checkonrow]), leadingTab=3)
                        self._insert(localtable, _upditem)
                    elif updaterrule == NightcapCoreUpaterRules.Submodule:
                        self.printer.print_formatted_additional(text=str(_upditem[checkonrow] + " / " + _upditem[checkonrowtwo]), leadingTab=3)
                        self._insert(localtable, _upditem)
                else:
                    if updaterrule == NightcapCoreUpaterRules.Package:
                        self.printer.print_formatted_check(text=str("UID: " + _upditem[checkonrow][checkonrowtwo]), leadingTab=3)
                    else:
                        self.printer.print_formatted_check(text=_upditem[checkonrow], leadingTab=3)
            except Exception as e:
                self.printer.print_error(e)
