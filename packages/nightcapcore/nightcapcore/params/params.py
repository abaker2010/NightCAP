# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
import os
from colorama import Fore, Style
from nightcapcore.printers import Printer

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
            self.dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_pcaps")
            self.filename = "xmrig2.pcapng"
            self.project = None
        self.verboselevel = verboselevel
        self.printer = Printer()

    def show_params(self):

        if(self.project == None):
            proj = ('None')
        else:
            proj = Fore.LIGHTYELLOW_EX+str(self.project['project_name'])
        self.printer.item_2(text="~ PROJECT", optionalText=proj, leadingTab=1, leadingText='', textColor=Fore.LIGHTGREEN_EX)
        self.printer.item_2(text="~ FILENAME", optionalText=str(self.filename), leadingTab=1, leadingText='', textColor=Fore.LIGHTGREEN_EX)
        self.printer.item_2(text="~ ISDIR", optionalText=str(self.isDir), leadingTab=1, leadingText='', textColor=Fore.LIGHTGREEN_EX)
        self.printer.item_2(text="~ PATH", optionalText=str(self.dir), leadingTab=1, leadingText='', textColor=Fore.LIGHTGREEN_EX, endingBreaks=1)   

    def toJson(self):
        js = {
            'project' : self.project,
            'isDir' : self.isDir,
            'dir' : self.dir, 
            'filename' : self.filename
        } 
        return js   
    