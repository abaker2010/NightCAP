# Copyright 2020 by Aarom Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
from nightcapcore.paths.paths import NightcapPaths
from nightcapcore.paths.pathsenum import NightcapPathsEnum
import os
import base64
from colorama import Fore, Style
from .base import *
from ..files.files import NightcapCoreFiles
from nightcapcore import NightcapDynamicParams, NightcapCoreConsoleOutput 

class NightcapSimpleReport(NightcapCoreReportBase):

    def __new__(cls, scriptpath: str = None, params: NightcapDynamicParams = None):
        if(scriptpath is None):
            raise Exception("Path must be passed")
        instance = super(NightcapSimpleReport, cls).__new__(cls)
        return instance

    def __init__(self, scriptpath: str = None, params: NightcapDynamicParams = None):
        NightcapCoreReportBase.__init__(self)
        self.spath = (os.sep).join(os.path.normpath(scriptpath).split(os.sep)[-4:])
        self.console = NightcapCoreConsoleOutput()
        self.params = params

    #region Print Report to console
    def print_report(self):
        '''This is meant for console printing'''
        print("\n")
        print(Fore.CYAN + "\t" + "*"*75, Style.RESET_ALL)
        print(Fore.CYAN + "\t" + self.name.center(75, " "), Style.RESET_ALL)
        print(Fore.CYAN + "\t" + "*"*75, Style.RESET_ALL)

        # {0: 
        # {'name': 'header name one', 'format': 'header_default', 
        #       'data': [{'name': 'para name', 'format': 'paragraph_default'}]}, 
        # 1: {'name': 'header name two', 'format': 'header_default', 'data': []}
        # }
        for k in self.data.keys():
            self.console.output('\n')
            self.console.output("\t" + '-'*len(self.data[k].name), level=5)
            self.console.output("\t" + self.data[k].name, level=5)
            self.console.output("\t" + '-'*len(self.data[k].name), level=5)
            for d in self.data[k].data:
                self.console.output("\t" + "  ~ " + d.text)

        self.console.output("\n")
        self.console.output("\t  " + "** END OF REPORT **", color=Fore.RED)
        self.console.output("\n")
    #endregion


    #region Save Report to HTML File
    def save(self):
        '''This is meant for saving html files'''

        self.console.output("Trying to save report (HTML)", level=7)
        self.console.output("Params: " + str(self.params), level=2)
        self.console.output("Project Name: " + str(self.params['project']), level=2)
        self.console.output("Custom style sheet needs to be used: " + str(self.custom_style_sheets), level=2)
        # print("\n\n")
        # print("Params:", self.params)
        # print("Project Name:", self.params['project'])
        # print("Custom style sheet needs to be used:", self.custom_style_sheets)
        
        if(self.params['project'] == None):
            print("")
        else:
            _html = []
            print("From Paths")
            print("---------------")
            print(NightcapPaths().generate_path(NightcapPathsEnum.Reporting, [self.params['project']['project_number']] + self.spath.split(os.sep)[:-1] + ['index.html']))
            
            report_files = NightcapCoreFiles(NightcapPaths().generate_path(NightcapPathsEnum.Reporting, [self.params['project']['project_number']] + self.spath.split(os.sep)[:-1] + ['index.html']))

            if(len(self.custom_style_sheets) == 0 or self.replace_original_style_sheet == False):
                print("Second Style Sheet Is Not Added")
                _html.append('<link rel="stylesheet" href="http://localhost:8056/style.css">')
            
            if(len(self.custom_style_sheets) != 0):
                print("Second Style Sheet Needed To Be Used")
                try:
                    custom_style_format = '<link href="http://localhost:8056/custom_report_style/%s.css" rel="stylesheet">'
                    for sheet in self.custom_style_sheets:
                        _html.append(custom_style_format % (base64.b64encode((sheet).encode('ascii')).decode("utf-8")))
                except Exception as e:
                    raise e

            _html.append('<body class="w3-light-grey">')
            _html.append('<div class="report w3-container w3-center w3-round w3-light-grey">')
            _html.append("<h1>Scan Used: %s</h1>" % os.sep.join(self.spath.split(os.sep)[:-1]))
            _html.append('<center><hr class="style18"></center>')
            _html.append('<div class="w3-container w3-center w3-round rpcontainer">')
            for k in self.data.keys():
                _html.append("<div>")
                _html.append((self.header_formats[self.data[k].format] % self.data[k].name))
                for v in self.data[k].data:
                    _html.append((self.paragraph_formats[v.format] % v.text))

                _html.append("</div>")
            _html.append('</div>')
            _html.append("</div>")
            _html.append("</body>")
            report_files.create_html_report("\n".join(_html))
    #endregion
