# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Import
# from application.classes.base_cmd.base_cmd import NightcapBaseCMD
from nightcappackages.classes.databases.mogo.interfaces.mogo_operations import MongoDatabaseOperationsInterface
from nightcappackages.classes.databases.mogo.mongo_connection import MongoDatabaseConnection
from nightcapcore.decorators.singleton import Singleton
from nightcapcore.printers import Printer

@Singleton
class MongoProjectsDatabase(MongoDatabaseConnection, MongoDatabaseOperationsInterface):
    def __init__(self):
        MongoDatabaseConnection.__init__(self)
        MongoDatabaseOperationsInterface.__init__(self)
        self._db = self.client[self.conf.currentConfig['MONGOSERVER']['db_name']]['projects']
        self.printer = Printer()

    def create(self, prj: str):
        if(self.find(prj).count() == 1):
            self.printer.print_formatted_delete(text="Project Already Exists")
        else:
            self._db.insert_one({"project_name" : prj})


    def read(self):
        return self._db.find()

    def update(self):
        # super().update(updatetable=updatedb.table('packages'),localtable=self.db_packages.table('packages'),checkonrow='package_information',checkonrowtwo='uid', updaterrule=NightcapCoreUpaterRules.Package)
        pass

    def delete(self, puid: int):
        try:
            _prj = self.projects()
         
            if puid in _prj.keys():    
                self._db.remove(_prj[puid])
            
        except Exception as e:
            self.printer.print_error(exception=e)        

    def projects(self):
        '''List all projects'''
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

    def find_project_by_generated_num(self, id: int):
        try:
            if id in self.projects().keys():
                return True
            return False
        except: 
            return False

    def find(self, prj_name: str):
        return self._db.find({'project_name' : {"$eq" : prj_name}})

    def select(self, id: int):
        '''\n\tSelect a project\n\t\tUsage: select [project_number]\n'''
        try:
            _ = self.projects()
            if id in _.keys():
                return _[id]
            else:
                return None
        except Exception as e:
            raise ValueError("")

    #region Old Code needs updated
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
    #endregion