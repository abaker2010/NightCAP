# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
import os
import base64 
from nightcapcore.remotedocs.remote_docs import NightcapCoreRemoteDocs
from nightcapcore.configuration.configuration import NighcapCoreConfiguration
from nightcapcore.projects.projects import NightcapCoreProject
from nightcapcore.remotedocs.remote_docs import NightcapCoreRemoteDocs
from nightcapcore.paths.paths import NightcapPaths
from nightcapcore.paths.pathsenum import NightcapPathsEnum

class NightcapCoreServerReportingBase(NighcapCoreConfiguration):
    def __init__(self, basepath: str = ""):
        NighcapCoreConfiguration.__init__(self)
        self.basepath = basepath
        self.routes = {
            "/" : "index.html",
            "/style.css" : "style.css",
        }
        
    def get_route(self, route):
        if(route == "/"):
            _path = os.path.join(self.basepath, self.routes[route])
            return self._generate_standard_template_page(self.basepath, self._generate_home_page(_path))
        
        if(route == "/style.css"):
            syl = open(os.path.join(self.basepath, "style.css")).read()
            return syl

        if("/project/" in route):
            _path = os.path.join(self.basepath, route)
            subd =  str(_path).split("/")[2:]
            if(len(subd) <= 3):
                return self._generate_standard_template_page(self.basepath, self._generate_page(route, subd))
            elif(len(subd) == 4):
                return self._generate_report_template_page(self.basepath, self._generate_reports_page(self.basepath, subd))
            else:
                pass
        if("/custom_report_style/" in route):
            try:
                _file = open(base64.b64decode(str(route).replace("/custom_report_style/", '').replace('.css','')).decode("ascii")).read()

                return _file
            except Exception as e:
                return str(e)

        
        error = ""
        with open(os.path.join(self.basepath, "error.html"), 'r') as file:
            error = file.read()
        return error
    

    def _generate_report_template_page(self, basepath: str, data: str):
        base_page = open(os.path.join(basepath, "simple_report.html")).readlines()
        replacement = NighcapCoreConfiguration().Config().get("REPORTINGREPLACEMENTS", "report_data_replacement")
        
        n_lines = []
        for line in base_page:
            n_line = ""
            if(replacement in line):
                n_line = data
            else:
                n_line = line
            n_lines.append(n_line)
        
        return "\n".join(n_lines)
        
    #region Generate Reports Page
    def _generate_reports_page(self, basedir: list, subd: list):
        template_file = NightcapPaths().generate_path(NightcapPathsEnum.Reporting, subd + ['index.html'])
        file = open(template_file, 'r').read()
        return file
    #endregion       

    #region Standard Tempplate 
    def _generate_standard_template_page(self, basepath: str, data: str):
        base_page = open(os.path.join(basepath, "base.html")).readlines()
        replacement = NighcapCoreConfiguration().Config().get("REPORTINGREPLACEMENTS", "base_data_replacement")
        n_lines = []
        for line in base_page:
            n_line = ""
            if(replacement in line):
                n_line = data
            else:
                n_line = line
            n_lines.append(n_line)
        
        return "".join(n_lines)
    #endregion

    #region Generate Home Page
    def _generate_home_page(self, path):
        data = open(path).readlines()
        print("Data for home page: ", data)
        proj_replace = NighcapCoreConfiguration().Config().get("REPORTINGREPLACEMENTS", "project_list_replacement")
        ndata = []
        for l in data:
            if proj_replace in l:
                projs = NightcapCoreProject().projects()
                print(type(projs))
                print(projs)
                for proj in projs:
                    htm = "<a href='/project/%s'><li>%s</li></a>" % (proj["project_number"], proj["project_name"])
                    ndata.append(htm)
            else:
                ndata.append(l)

        return " ".join(ndata)
    #endregion

    #region Generate Projects Page
    def _generate_page(self, route: str, subd: list):
        # subd =  str(path).split("/")[2:]
        reports_path = NightcapPaths().generate_path(NightcapPathsEnum.Reporting, subd)
        
        if(len(subd) == 1):
            opts = self._generate_list_options(reports_path)
            t_data = self._format_list_page("Category", reports_path, route, opts)
            return "\n".join(t_data)
        elif(len(subd) == 2):
            opts = self._generate_list_options(reports_path)
            t_data = self._format_list_page("Sub-Category", reports_path, route, opts)
            return "\n".join(t_data)
        elif(len(subd) == 3):
            opts = self._generate_list_options(reports_path)
            t_data = self._format_list_page("Scanner", reports_path, route, opts)
            return "\n".join(t_data)
        else:
            return "No Scans have been done"
    #endregion

    #region Generate List Options
    def _generate_list_options(self, basedir: str, reportlink: bool = False):
        opts = []
        for root, dirs, files in os.walk(basedir, topdown=False):
            if(reportlink == False):
                for name in dirs:
                    _p = os.path.join(root, name).replace(basedir, "")                  
                    try:
                        opt = _p.split(os.sep)[1]
                        if opt not in opts:
                            opts.append(opt)
                    except:
                        pass
            elif(reportlink == True):
                for file in files:
                    if file not in opts:
                        opts.append(file)
        return opts
    #endregion

    #region Format List Page
    def _format_list_page(self, header: str, path: str, route: str, opts: list):
        t_data = []
        
        list_replacement = '[' + self.Config().get('REPORTINGREPLACEMENTS', 'list_item_replacement') + ']'
        header_replacement = '[' + self.Config().get('REPORTINGREPLACEMENTS', 'header_replacement') + ']'

        template_file = NightcapPaths().generate_path(NightcapPathsEnum.ReportingTemplates, ['list_template.html'])
        # template_folder = (self.Config().get('REPORTINGPATHS', 'reporting_templates') + '/list_template.html').replace('/', os.sep)
        # template_path = os.getcwd().replace('nightcap', template_folder)

        # print(NightcapCoreRemoteDocs.get_link("mdns"))
        with open(template_file, "r") as file:
            lines = file.readlines()
            for line in lines:
                if list_replacement in line:
                    for opt in opts: 
                        op = ("<a href='%s'><li>%s</li></a>" % ((route + '/' + opt), str(opt).replace(".html", '')))
                        t_data.append(op)
                elif header_replacement in line:
                    t_data.append(header)
                else:
                    t_data.append(line)
        return t_data
        # return template_file
    #endregion