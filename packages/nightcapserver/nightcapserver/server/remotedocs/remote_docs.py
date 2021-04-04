# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Imports
import os
from typing import Mapping
from nightcapcore.printers import Printer
from tinydb import TinyDB
from tinydb.queries import Query

# endregion


class NightcapCoreRemoteDocs(object):
    """

    This class is used as a remote document helper

    ...

    Attributes
    ----------
        protocol_db: -> TinyDB
            used to store the references to the different protocols

        printer: -> Printer
            used to allow us to print to the console

    Methods
    -------
        Accessible
        -------
            get_link(self, protocol): -> str
                returns a reference url for the user to use

            update(self, updatedb: TinyDB): -> None
                allows the db to be updated by the updater

        None Accessible
        -------
            __add_link(self, link: Mapping): -> none
                adds a link to the protocol database

    """

    # region Init
    def __init__(self):
        self.protocol_db = TinyDB(
            os.path.join(
                os.path.dirname(__file__), "..", "database", "protocol_links.json"
            )
        )
        self.printer = Printer()

    # endregion

    # region Get Link
    def get_link(self, protocol):
        found = self.protocol_db.table("protocol_links").search(
            Query()["name"] == protocol
        )
        return found

    # endregion

    # region Add Link
    def __add_link(self, link: Mapping):
        try:
            self.protocol_db.table("protocol_links").insert(link)
        except Exception as e:
            print(e)

    # endregion

    # region Update
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

    # endregion
