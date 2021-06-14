# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
#region Imports
from nightcappackages.classes.helpers.encoder import NightcapJSONEncoder
from bson.objectid import ObjectId
from nightcappackages.classes.databases.mogo.mongo_reporter import MongoReportsDatabase
from uuid import uuid4
import datetime

from pymongo.results import UpdateResult
#endregion

class NightcapReport(MongoReportsDatabase):

    def __init__(self, project: str, packageID: str, base_params: dict, params_used: dict) -> None:
        super().__init__(project)

        self.id = uuid4().hex
        self.pkgID = packageID
        self.base_params = base_params
        self.params_used = params_used
        self.date = datetime.datetime.now()
        self.data = {}

    def add_category(self, cat: str):
        self.data[cat] = {}

    def add_category_data(self, cat: str, key: str, value: str):
        self.data[cat][key] = value

    def get_category(self, cat: str):
        return self.data[cat]

    def save(self):
        '''Save report to database'''
        try:
            _reports = self.db.find_one({"_id" : ObjectId(self.project['_id']['$oid'])})
            _project_there = None if _reports == None else _reports

            if _project_there != None:
                _reported = _project_there['data'][self.pkgID]
                if self.printer.input("Would you like to keep or replace the report? (k/R)", defaultReturn=True, default=['r', 'R']):
                    if not self.db.update_one({"_id" : ObjectId(self.project['_id']['$oid'])}, { "$set" : {
                                'data' : {
                                    self.pkgID : self.toJson()
                                    }
                                }
                                }).raw_result['updatedExisting']:
                        print("Error Replacing Report")
                else:
                    _reported[self.id] = {
                            "date" : datetime.datetime.now(),
                            "data" : self.data,
                            "params" :  {
                                "package_params" : self.params_used
                            }

                        }
                    if not self.db.update_one({"_id" : ObjectId(self.project['_id']['$oid'])}, { "$set" : {
                                'data' : {
                                    self.pkgID : _reported
                                    }
                                }
                                }).raw_result['updatedExisting']:
                        print("Error Inserting Report")
            else:
                if not self.db.insert_one({
                    '_id' : ObjectId(self.project['_id']['$oid']),
                    'data' : {
                        self.pkgID : self.toJson()
                        }
                }).acknowledged:
                    self.printer.print_error(Exception("Errir inserting Report"))
                
                # self.printer.print_formatted_additional("Skipping: No project selected to generate report for", endingBreaks=2)
            self.printer.print_formatted_check("Report Saved", endingBreaks=2)
        except AttributeError as ae:
            # print(ae)
            self.printer.print_formatted_check("Report Skipped", "No project selected", endingBreaks=2)
        except Exception as e:
            self.printer.print_error(e)
        
    # region To JSON
    def toJson(self) -> dict:
        js = {
            self.id  : {
                "date" : datetime.datetime.now(),
                "data" : self.data,
                "params" :  {
                    "package_params" : self.params_used,
                    # "base_params" : self.base_params
                }

            }
        }
        return js

    # endregion
    