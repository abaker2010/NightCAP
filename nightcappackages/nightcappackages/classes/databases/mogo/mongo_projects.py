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


class MongoProjectsDatabase(MongoDatabaseOperationsConnection, metaclass=Singleton):
    """

    This class is used to connect to the projects database

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
    def __init__(self):
        MongoDatabaseOperationsConnection.__init__(self)
        self._db = self.client[self.conf.config["MONGOSERVER"]["db_name"]]["projects"]
        self.printer = Printer()

    # endregion

    # region Create
    def create(self, prj: str):
        if self.find(prj).count() == 1:
            self.printer.print_formatted_delete(text="Project Already Exists")
        else:
            self._db.insert_one({"project_name": prj})

    # endregion

    # region Read
    def read(self):
        return self._db.find()

    # endregion

    # region Update
    def update(self):
        pass

    # endregion


    def drop(self):
        self._db.drop()
        

    # region Date
    def delete(self, puid: int):
        try:
            _prj = self.projects()

            if puid in _prj.keys():
                self._db.remove(_prj[puid])

        except Exception as e:
            self.printer.print_error(e)

    # endregion

    # region Projects
    def projects(self):
        """List all projects"""
        _ = self.read()
        if _.count() == 0:
            return None
        else:
            _n = {}
            count = 0
            for i in _:
                count += 1
                _n[count] = i
            return _n

    # endregion

    # region Find Project by generated num
    def find_project_by_generated_num(self, id: int):
        try:
            if id in self.projects().keys():
                return True
            return False
        except:
            return False

    # endregion

    # region Find
    def find(self, prj_name: str):
        return self._db.find({"project_name": {"$eq": prj_name}})

    # endregion

    # region Select
    def select(self, id: int):
        """\n\tSelect a project\n\t\tUsage: select [project_number]\n"""
        try:
            _ = self.projects()
            if id in _.keys():
                return _[id]
            else:
                return None
        except Exception as e:
            raise ValueError("")

    # endregion

    # region Old Code needs updated
    # def __has_project(self, project_name):
    #     found = self.projects_db.search(Query()["project_name"] == project_name)
    #     return found

    # def update(self,updatedb: TinyDB):
    #     self.printer.item_2(text="updating db", optionalText='projects_db.json')
    #     self.printer.item_2(text="Checking entries: from update", leadingText='~')

    #     for _proj in updatedb.table("projects").all():
    #         _there = self.__has_project(_proj['project_name'])
    #         if(_there == []):
    #             self.printer.print_formatted_additional(text="Adding: " + _proj['project_name'], leadingTab=4)
    #             self.create(_proj['project_name'])
    #         else:
    #             self.printer.print_formatted_check(text=_proj['project_name'], leadingTab=4)
    # endregion
