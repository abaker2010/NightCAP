# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Imports
from nightcapcore.singleton.singleton import Singleton
from nightcapcore.printers import Printer
from nightcappackages.classes.databases.mogo.connections.mongo_operation_connector import (
    MongoDatabaseOperationsConnection,
)

# endregion


class MongoReportsDatabase(MongoDatabaseOperationsConnection, metaclass=Singleton):
    """

    This class is used to connect to the reports database

    ...

    Attributes
    ----------
        _db: -> MongoClient
        printer: -> Printer

    Methods
    -------
        Accessible
        -------
            create(self, prj: str): -> None
                inserts a new project

            read(self): -> Any
                reads all of the entries in the db

            update(self): -> None
                Not working yet

            delete(self, puid: int): -> None
                tries to delete the project from the db

            projects(self): -> {}
                returns a dict of the projects

            find_project_by_generated_num(self, id: int): -> bool
                returns a boolean if the project is found

            find(self, prj_name: str): -> dict
                returns a dict of the project if found

            select(self, id: int): -> dict
                returns a dict of the project selected
    """

    # region Init
    def __init__(self, project: dict):
        MongoDatabaseOperationsConnection.__init__(self)
        self.printer = Printer()
        if project != None:
            self.project = project

            self.db = self.client[self.conf.config["MONGOSERVER"]["db_name"]]["reports"]
        else:
            self.project = None
            self.db = None

    # endregion

    def create(self, report: dict):
        # if self.db.find("$eq": prj_name}}).count() == 1:
        #     self.printer.print_formatted_delete(text="Project Already Exists")
        # else:
        self.db.insert_one(report)

    # region Read
    def read(self):
        return self.db.find()

    # endregion

    # region Update
    def update(self):
        pass

    # endregion

    def drop(self):
        self.db.drop()

    # region Date
    def delete(self, puid: int):
        pass

    # endregion

    # region Find
    def find(self, prj_name: str):
        return self.db.find({"project_name": {"$eq": prj_name}})

    # endregion
