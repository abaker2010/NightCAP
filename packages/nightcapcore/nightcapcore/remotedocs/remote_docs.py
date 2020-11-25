# Copyright 2020 by Aarom Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
import os
from tinydb import TinyDB
from tinydb.queries import Query

class NightcapCoreRemoteDocs(object):
    def __init__(self):
        self.protocol_db = TinyDB(os.path.join(os.path.dirname(__file__), "..", "database", "protocol_links.json")).table("protocol_links")

    def get_link(self, protocol):
        found = self.protocol_db.search(Query()["name"] == protocol)
        return found
