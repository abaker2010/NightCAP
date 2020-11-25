# Copyright 2020 by Aarom Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
from application.classes.configuration.configuration import Configuration
from nightcapcore import NightcapCoreBase, NightcapPaths, NightcapPathsEnum, NightcapCoreConsoleOutput, NightcapCoreProject
from application.classes.base_cmd.base_cmd import NightcapBaseCMD
from application.classes.helpers.screen.screen_helper import ScreenHelper
from colorama import Fore, Style
import shutil

class NightcapProjects(NightcapBaseCMD):
    def __init__(self, packagebase: NightcapCoreBase, conf: Configuration):
        NightcapBaseCMD.__init__(self,["projects"], packagebase)
        self.projects_db = NightcapCoreProject()
        self.base = packagebase
        self.config = conf
        self.output = NightcapCoreConsoleOutput()

    #region Exit
    def do_exit(self,line):
        ScreenHelper().clearScr()
        try:
            self.selectedList.remove(self.selectedList[-1])
        except Exception as e:
            pass
        return True
    #endregion

    #region Delete Project
    def do_delete(self, line):
        '''Delete a project'''
        _confirm = input((Fore.RED + ("Project with ID: %s will be DELETED used would you like to continue? [Y/n]: " % (line)) + Fore.GREEN))
        yes_options = self.config.Config()["NIGHTCAP"]["yes"].split(" ")
        
        try:
            try:
                if(_confirm in yes_options):
                    self.output.output("DELETING PROJECT", level=6)

                    pro_id = int(line)
                    proj = self.projects_db.select(pro_id)[0]
                    
                    print(pro_id)
                    print(proj)
                    print(proj['project_name'])

                    print("Will need to remove the entry from the db and remove the files from the system")
                    print(NightcapPaths().generate_path(NightcapPathsEnum.Reporting, [pro_id]))


                    # reporting_path = self.config.Config()["PROJECTS"]["path"].split('/')
                    # de_path = os.path.dirname(__file__).replace(os.sep.join(['nightcap','application','classes','project']), os.sep.join(reporting_path)) + os.sep + str(pro_id)

                    # print(de_path)
                    # delete entry 
                    self.projects_db.delete(pro_id)

                    try:
                        # remove files
                        shutil.rmtree(NightcapPaths().generate_path(NightcapPathsEnum.Reporting, [pro_id]))
                    except:
                        self.output.output("There was no reports to delete")

            except ValueError as ar:
                raise Exception("Please enter a project ID Numder")
                
        except Exception as e:
            print(Fore.YELLOW, e, Style.RESET_ALL)
    #endregion

    #region List Projects
    def do_projects(self, line):
        '''List all projects'''
        print(Fore.LIGHTGREEN_EX, "\n\n\tCurrent Projects", Style.RESET_ALL)
        print(Fore.LIGHTYELLOW_EX, "\t", "-"*len("Current Projects"), Style.RESET_ALL, sep="")
        # _num_name = "\t\t%s | %s" % (Fore.LIGHTBLUE_EX + "Num", "Name" + Style.RESET_ALL)
        print("\t", Fore.LIGHTCYAN_EX, "Num   |   Name")
        print("\t ","-"*(int(len("Num   |   Name")*1.3)),Style.RESET_ALL)

        for docs in self.projects_db.projects():
            print("\t  ",Fore.LIGHTGREEN_EX, docs["project_number"], Fore.LIGHTMAGENTA_EX, " | ", Fore.LIGHTCYAN_EX, docs["project_name"])

        print()
    #endregion

    #region Select Project
    def do_select(self, line):
        '''\n\tSelect a project\n\t\tUsage: select [project_number]\n'''
        try:
            found = self.projects_db.select(line)
            self.base.project = found[0]
            self.output.output(Fore.YELLOW + "Selecting project ~ " + Fore.GREEN + found[0]["project_name"])
            # print("\n\t", Fore.YELLOW, "Selecting project ~", Fore.GREEN, found[0]["project_name"], Style.RESET_ALL, end="\n\n")
        except Exception as e:
            print("\nPlease check the param and try again. Note: Must use project number for selection")
    #endregion

    #region Unselect Project
    def do_unselect(self, line):
        '''\n\tUnselect a project\n\t\tUsage: unselect\n'''
        try:
            self.base.project = None
            self.output.output("[+] Unselected project")
        except Exception as e:
            self.output.output(str(e), level=6)
    #endregion

    #region Create Project
    def do_create(self,line):
        '''\n\tCreate a project\n\t\tUsage: create [project_name]\n'''
        _id = []
        for p in self.projects_db.projects():
            _id.append(p['project_number'])
        try:
            if(len(_id) != 0):
                proj_num = max(_id) + 1
            else:
                proj_num = 1

            self.projects_db.create({"project_number" : proj_num, "project_name" : line})
        except Exception as e:
            self.console_output.output(e, level=6)
    #endregion