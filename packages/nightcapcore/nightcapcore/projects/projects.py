# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
from nightcapcore.remotedocs.remote_docs import NightcapCoreRemoteDocs
from nightcapcore.printers import Printer
import os
from tinydb import TinyDB
from tinydb.queries import Query

class NightcapCoreProject(object):
    def __init__(self):
        self.projects_db = TinyDB(os.path.join(os.path.dirname(__file__), "..", "database", "projects_db.json")).table("projects")
        self.printer = Printer()

    def projects(self):
        '''List all projects'''
        # print(NightcapCoreRemoteDocs().get_link("eth"))
        return self.projects_db.all()
 
    def project_name(self,line):
        '''Get the projects name'''
        selecting = int(line)
        found = self.projects_db.search(Query()["project_number"] == selecting)
        return found

    def select(self, line):
        '''\n\tSelect a project\n\t\tUsage: select [project_number]\n'''
        selecting = int(line)
        found = self.projects_db.search(Query()["project_number"] == selecting)
        return found

    def delete(self, line):
        '''\n\tDelete a project\n\t\tUsage: delete [project_id]\n'''
        selecting = int(line)
        self.projects_db.remove(Query()["project_number"] == selecting)
        found = self.projects_db.search(Query()["project_number"] == selecting)
        return found

    def create(self,line):
        '''\n\tCreate a project\n\t\tUsage: create [project_name]\n'''
        # proj_num = len(self.projects_db.all()) + 1
        _id = []
        for p in self.projects():
            _id.append(p['project_number'])

        if(len(_id) != 0):
            proj_num = max(_id) + 1
        else:
            proj_num = 1
        self.projects_db.insert({"project_number" : proj_num, "project_name" : line})

    def __has_project(self, project_name):
        found = self.projects_db.search(Query()["project_name"] == project_name)
        return found

    def update(self,updatedb: TinyDB):
        self.printer.item_2(text="updating db", optionalText='projects_db.json')
        self.printer.item_2(text="Checking entries: from update", leadingText='~')

        for _proj in updatedb.table("projects").all():
            _there = self.__has_project(_proj['project_name'])
            if(_there == []):
                self.printer.print_formatted_additional(text="Adding: " + _proj['project_name'], leadingTab=4)
                self.create(_proj['project_name'])
            else:
                self.printer.print_formatted_check(text=_proj['project_name'], leadingTab=4)