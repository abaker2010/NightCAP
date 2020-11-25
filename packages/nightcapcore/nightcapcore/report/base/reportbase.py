# Copyright 2020 by Aarom Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
import os
from nightcapcore.report.widgets import header
from ..widgets import NightcapSimpleReportHeader, NightcapSimpleReportParagraph

class NightcapCoreReportBase(object):
    def __new__(cls):
        instance = super(NightcapCoreReportBase, cls).__new__(cls)
        return instance
 
    def __init__(self):
        self._name = ""
        self.header_formats = { 
            "header_default" : '<div><h1>%s</h1><hr class="dotted"></div>'
            }
        self.paragraph_formats = {
            "paragraph_default" : "<p>%s</p>"
        }

        self.custom_style_sheets = []
        self.replace_original_style_sheet = False

        # print(os.path(__file__))
        #region Data Structure For Data
        # Data should be structured like so
        # {
        #   header_num : {
        #   header_name : "",
        #   header_data : [para]
        # }
        #endregion
        self.data = {}

    #region Name Property 
    # function to get value of _name
    def get_name(self):
        return self._name

    # function to set value of _name 
    def set_name(self, a: str): 
        self._name = a 
  
     # function to delete _name attribute 
    def del_name(self): 
        del self._name 

    def add_custom_style_sheet(self, sheetpath: str):
        self.custom_style_sheets.append(sheetpath)
    
    name = property(get_name, set_name, del_name)  
    #endregion

    # #region Header Formatting
    # def add_header_formmat(self, key: str, frmt: str):
    #     self.header_formats[key] = frmt
    # #endregion

    def add_header(self, header: NightcapSimpleReportHeader):
        # if(type(header) is NightcapSimpleReportHeader):
        if(isinstance(header, NightcapSimpleReportHeader)):
            key = len(self.data.keys())
            self.data[key] = header
            return key
        else:
            raise Exception("Error with adding header: Wrong data type")

    def add_header_data(self, headerkey: int, para: NightcapSimpleReportParagraph = None):
        try:
            self.data[headerkey].data.append(para)
        except Exception as e:
            raise e
    #endregion

    #regin Saving Report
    def save(self):
        pass
    #endregion

    #region Print Report
    def print_report(self):
        pass
    #endregion