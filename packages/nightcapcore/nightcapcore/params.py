# Copyright 2020 by Aarom Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
import os
from colorama import Fore, Style
from nightcapcore.output import NightcapCoreConsoleOutput

class NightcapDynamicParams(object):
    def __init__(self,params: dict = None,verboselevel: int = 0):
        if(params != None):
            params_dict = dict(params)['0']
            self.isDir = params_dict['isDir']
            self.dir = params_dict['dir']
            self.filename = params_dict['filename']
            self.project = params_dict['project']
        else:
            self.isDir = False
            self.dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_pcaps", "pcaps")
            self.filename = "xmrig2.pcapng"
            self.project = None
        self.verboselevel = verboselevel

        self.output = NightcapCoreConsoleOutput()

    def show_params(self):

        if(self.project == None):
            proj = (Fore.LIGHTYELLOW_EX+'None')
        else:
            proj = (Fore.LIGHTRED_EX+'('+str(self.project['project_number'])+') '+Fore.LIGHTYELLOW_EX+str(self.project['project_name']))
        self.output.output("PROJECT = " + proj)
        self.output.output(Fore.LIGHTGREEN_EX+"\tFILENAME = "+Fore.LIGHTYELLOW_EX+str(self.filename))
        self.output.output(Fore.LIGHTGREEN_EX+"ISDIR = "+Fore.LIGHTYELLOW_EX+str(self.isDir))
        self.output.output("\t\t\tPATH = "+Fore.LIGHTYELLOW_EX+str(self.dir))        

    def toJson(self):
        js = {
            'project' : self.project,
            'isDir' : self.isDir,
            'dir' : self.dir, 
            'filename' : self.filename
        } 
        return js   
    