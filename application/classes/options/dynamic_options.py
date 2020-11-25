# Copyright 2020 by Aarom Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
from nightcapcore.base import NightcapCoreBase
from application.classes.configuration.configuration import Configuration
import os
import copy
import json
from colorama import Fore, Style
from application.classes.helpers.screen.screen_helper import ScreenHelper
from application.classes.options.option_generator import NightcapOptionGenerator
from application.classes.use.dynamic_use import NightcapDynamicUse
from application.classes.banners.nightcap_banner import NightcapBanner
from application.classes.base_cmd.base_cmd import NightcapBaseCMD
from application.classes.banners.nightcap_banner import NightcapBanner
from application.classes.project.project import NightcapProjects
from nightcapcore import NighcapCoreSimpleServer

from subprocess import Popen, PIPE, STDOUT
try:
    from subprocess import DEVNULL # py3k
except ImportError:
    import os
    DEVNULL = open(os.devnull, 'wb')

class NightcapDynamicOptions(NightcapBaseCMD):
    def __init__(self, selectedList: list, configuration: Configuration, packagebase: NightcapCoreBase = NightcapCoreBase()):
        NightcapBaseCMD.__init__(self, selectedList, packagebase)
        self.config = configuration
        try:
            self.package_params = copy.deepcopy(self.packages_db.package_params(self.selectedList))
        except Exception as e:
            self.package_params = None

    def do_options(self, line):
        if(len(line) == 0):
            NightcapOptionGenerator(self.selectedList).options()
        elif(line == "detailed"):
            NightcapOptionGenerator(self.selectedList).options(isDetailed=True)
        else:
            print("Error with command")

    def help_options(self):
        NightcapOptionGenerator(self.selectedList).option_help()

    def do_params(self,line):  
        if(len(line) == 0):
            title1 = "Base Params"
            self.console_output.output("\n")
            self.console_output.output(title1, color=Fore.CYAN)
            self.console_output.output("-"*(len(title1)*2), color=Fore.LIGHTYELLOW_EX)
            self.package_base.show_params()
        else:
            sline = line.split(" ")
            slineCap = sline[0].upper()
            if(slineCap == "ISDIR"):
                self.package_base.isDir = True if sline[-1].upper() == "TRUE" else False 
            elif(slineCap == "PATH"):
                self.package_base.dir = str(sline[-1])
            elif(slineCap == "FILENAME"):
                self.package_base.filename = str(sline[-1])

        if(len(self.selectedList) == 3):
            if(len(line) == 0):
                if(self.package_params.keys()):
                    title2 = "Available Package Params"
                    self.console_output.output("\n")
                    self.console_output.output(title2, color=Fore.CYAN)
                    self.console_output.output("-"*(len(title2)), color=Fore.LIGHTYELLOW_EX)

                    g1 = "%s%s%s" % (Fore.LIGHTBLUE_EX, "Data Type", Fore.LIGHTGREEN_EX)
                    g2 = "%s" % ("Name")
                    g3 = "%s%s%s" % (Fore.CYAN, "Value", Style.RESET_ALL)
                    g4 = "%s%s%s%s%s" % (g1.center(20, " "), "|", g2.center(28, ' '), "|", g3.center(20, ' '))
                    print('\n\t',g4)
                    print('\t',Fore.YELLOW, "*"*len(g4), Style.RESET_ALL)
                    for k in self.package_params.keys():
                        g1 = "%s(%s)%s" % (Fore.LIGHTBLUE_EX, self.package_params[k]["type"], Fore.LIGHTGREEN_EX)
                        g2 = "%s" % (self.package_params[k]["name"])
                        g3 = "%s%s%s" % (Fore.CYAN, self.package_params[k]["value"], Style.RESET_ALL)
                        
                        print('\t',g1.rjust(20, " "), "|", g2.ljust(25, ' '), "|", g3)
                    print("\n")
            else:
                sline = line.split(' ')

                for k in self.package_params.keys():
                    if(self.package_params[k]["name"] == sline[0]):
                        self.package_params[k]["value"] = str(sline[-1])

    def help_params(self):
        h1 = "See all available parameters:"
        h2 = "params"
        h3 = "set param:\tparams [PARAM] [PARAMVALUE]"
        p = '''
         %s 
         %s
         %s
        ''' % (
            (Fore.GREEN + h1),
            (Fore.YELLOW + h2 + Style.RESET_ALL),
            (Fore.YELLOW + h3 + Style.RESET_ALL),
            )
        print(p)

    def do_exit(self,line):
        ScreenHelper().clearScr()
        try:
            self.selectedList.remove(self.selectedList[-1])
        except Exception as e:
            pass
        return True

    def do_banner(self, line):
        ScreenHelper().clearScr()
        NightcapBanner(self.config).Banner()

    def do_run(self,line):
    
        force = False
        if(self.package_base.project == None):
            force = input((Fore.YELLOW + "Project not selected to be used would you like to continue? [Y/n]: " + Fore.GREEN))
            print(Style.RESET_ALL, Fore.LIGHTCYAN_EX)
            yes_options = self.config.Config()["NIGHTCAP"]["yes"].split(" ")
            if(force == None):
                force = False
            else:
                if(force in yes_options):
                    force = True
        else:
            force = True

        if(force == True):
            if(len(self.selectedList) == 3):
                exe_path = self.packages_db.get_package_run_path(self.selectedList)
                dat = {}
                dat[0] = self.package_base.toJson()
                dat[1] = self.package_params
                print("data before passing: ", dat)
                
                call = "python3.8 %s --data '%s'" % (exe_path, json.dumps(dat))
                
                os.system(call)
            else:
                print("Package not selected to be used")
        else:
            self.console_output.output("Scan canceled by user\n", level=6)

    def do_use(self, line):
        try:
            optionNumber = 0 if self.selectedList == None else len(list(self.selectedList))
            if("/" in line):
                try:
                    print("Splitting line")
                    sline = line.split("/")
                    isvalid = NightcapDynamicUse().validate(sline)
                    if(isvalid):
                        NightcapDynamicOptions(sline, self.config, self.package_base).cmdloop()
                    else:
                        raise Exception("Path to module not correct")
                except Exception as e:
                    raise e
            else:
                try:
                    useList = NightcapDynamicUse().use(optionNumber, self.selectedList, line)
                    self.selectedList.append(useList)
                    NightcapDynamicOptions(self.selectedList, self.config, self.package_base).cmdloop() #.cmdloop(intro="Testing intro string")
                except Exception as e:
                    self.selectedList.pop()


        except Exception as e:
            ScreenHelper().clearScr()
            NightcapBanner(self.config).Banner()
            print("\n", Fore.RED, e, Style.RESET_ALL, "\n")


    #region Update Server
    def do_reportserver(self,line):
        '''\n\tControll the update server\n\n\t\tOptions: status, start, stop'''
        try:
            if(line == "start"):
                NighcapCoreSimpleServer.instance().start()
            elif(line == "stop"):
                NighcapCoreSimpleServer.instance().shutdown()
            elif (line == "status"):
                print(NighcapCoreSimpleServer.instance().get_status())
        except Exception as e:
            print(e)
    #endregion

    #region
    def do_project(self,line):
        '''\n\nChange current project'''
        try:
            NightcapProjects(self.package_base, self.config).cmdloop()
        except Exception as e:
            print(e)

    #endregion
            
    #region Shell
    def do_shell(self, line):
        "\n\tRun a shell command, becareful with this. This feature is still in beta\n"
        output = os.popen(line).read()
        print("\n{0}{1}{2}".format(Fore.LIGHTGREEN_EX,output, Style.RESET_ALL))
        self.last_output = output
    #endregion


    