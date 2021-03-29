# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.

# from application.classes.helpers.printers.print import Printer
import os
from typing import Mapping
from nightcapcore.printers import Printer
from tinydb import TinyDB
from tinydb.queries import Query


class NightcapCoreRemoteDocs(object):
    def __init__(self):
        self.protocol_db = TinyDB(
            os.path.join(
                os.path.dirname(__file__), "..", "database", "protocol_links.json"
            )
        )
        self.printer = Printer()

    def get_link(self, protocol):
        found = self.protocol_db.table("protocol_links").search(
            Query()["name"] == protocol
        )
        return found

    def __add_link(self, link: Mapping):
        try:
            self.protocol_db.table("protocol_links").insert(link)
        except Exception as e:
            print(e)

    def update(self, updatedb: TinyDB):
        try:
            _items_added = 0
            for protocol in updatedb.table("protocol_links").all():
                if self.get_link(protocol["name"]) == []:
                    self.__add_link(protocol)
                    _items_added += 1
            self.printer.print_formatted_check(
                "Successfully updated", optionaltext=str(_items_added), leadingTab=3
            )
        except Exception as e:
            self.printer.print_error("Error updating:", e.message)
