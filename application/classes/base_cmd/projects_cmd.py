# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
from nightcappackages.classes.databases.mogo.mongo_projects import MongoProjectsDatabase
from tinydb.database import TinyDB
from nightcapcore import NightcapCLIConfiguration
from application.classes.base_cmd.base_cmd import NightcapBaseCMD
from application.classes.helpers.screen.screen_helper import ScreenHelper
from colorama import Fore, Style
import shutil

class NightcapProjectsCMD(NightcapBaseCMD):
    def __init__(self, conf: NightcapCLIConfiguration):
        NightcapBaseCMD.__init__(self,["projects"], conf)
        self._db = MongoProjectsDatabase.instance()
        self.config = conf
        self._count = 0

    #region Delete Project
    def do_delete(self, line):
        '''Delete a project'''
        
        try:
            _puid = int(line)
            try:
                if self._db.find_project_by_generated_num(_puid):
                    _confirm = input((Fore.RED + ("Project with ID: %s will be DELETED used would you like to continue? [Y/n]: " % (line)) + Fore.GREEN))
                    yes_options = self.config.currentConfig["NIGHTCAPCORE"]["yes"].split(" ")
                    if(_confirm in yes_options):
                        self._db.delete(_puid)
                        
                        # self.printer.print_formatted_check(text="DELETING PROJECT")

                        # pro_id = int(line)
                        # proj = self.projects_db.select(pro_id)[0]
                        
                        # print(pro_id)
                        # print(proj)
                        # print(proj['project_name'])

                        # print("Will need to remove the entry from the db and remove the files from the system")
                        # print(NightcapPaths().generate_path(NightcapPathsEnum.Reporting, [pro_id]))


                        # # reporting_path = self.config.Config()["PROJECTS"]["path"].split('/')
                        # # de_path = os.path.dirname(__file__).replace(os.sep.join(['nightcap','application','classes','project']), os.sep.join(reporting_path)) + os.sep + str(pro_id)

                        # # print(de_path)
                        # # delete entry 
                        # self.projects_db.delete(pro_id)

                        # try:
                        #     # remove files
                        #     shutil.rmtree(NightcapPaths().generate_path(NightcapPathsEnum.Reporting, [pro_id]))
                        # except:
                        #     self.printer.print_formatted_check(text="There was no reports to delete")
                        #     # self.output.output("There was no reports to delete")
                else:
                    raise Exception("Project does not exist")
            except Exception as e:
                self.printer.print_error(exception=e)
        except ValueError as ar:
                self.printer.print_error(exception=Exception("Please enter a project ID Numder"))
    #endregion

    def _prepare_list(self, item):
        self._count += 1
        return {self._count : item}

    #region List Projects
    def do_list(self, line):
        '''List all projects'''
        _prj = self._db.projects()
        if(_prj == None):
            print(Fore.LIGHTGREEN_EX, "\n\tNo Projects Available\n", Style.RESET_ALL)
        else:
            print(Fore.LIGHTGREEN_EX, "\n\n\tCurrent Projects", Style.RESET_ALL)
            print(Fore.LIGHTYELLOW_EX, "\t", "-"*len("Current Projects"), Style.RESET_ALL, sep="")
            print("\t", Fore.LIGHTCYAN_EX, "Num   |   Name")
            print("\t ","-"*(int(len("Num   |   Name")*1.3)),Style.RESET_ALL)

            for k, v in _prj.items():
                print("\t  ",Fore.LIGHTGREEN_EX, k, Fore.LIGHTMAGENTA_EX, " | ", Fore.LIGHTCYAN_EX, v["project_name"])
            print()
    #endregion

    #region Select Project
    def do_select(self, line):
        '''\n\tSelect a project\n\t\tUsage: select [project_number]\n'''
        try:
            try:
                _puid = int(line)
                _selected = self._db.select(_puid)
                if _selected != None:
                    self.base.project = _selected
                    self.printer.print_formatted_check(text="Selected", optionaltext= _selected["project_name"])
                else:
                    raise Exception()
            except ValueError as ar:
                    self.printer.print_error(exception=Exception("Please enter an existing project ID Numder"))
        except Exception as e:
            self.printer.print_error(exception=Exception("Please check the param and try again. Note: Must use project number for selection"))
    #endregion

    #region Unselect Project
    def do_unselect(self, line):
        '''\n\tUnselect a project\n\t\tUsage: unselect\n'''
        try:
            self.base.project = None
            # self.output.output("[+] Unselected project")
            self.printer.print_formatted_check("Unselected project")
        except Exception as e:
            # self.output.output(str(e), level=6)
            self.printer.print_error(exception=e)
    #endregion

    #region Create Project
    def do_create(self,line):
        '''\n\tCreate a project\n\t\tUsage: create [project_name]\n'''
        try:
            self._db.create(line)
        except Exception as e:
            self.printer.print_error(exception=e)
    #endregion

    def update(self,updatedb: TinyDB):
        print("\t","updating db: projects_db.json")
        print("\t","updater tables:", updatedb.tables())
        # print("\t","user tables:", self.projects_db.table())
        # self.projects_db.update(updatedb)