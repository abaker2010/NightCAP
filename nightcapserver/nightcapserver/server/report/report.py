# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.

#region Imports
from nightcappackages.classes.databases.mogo.mongo_projects import MongoProjectsDatabase

#endregion

class NightcapReport(object):

    def __init__(self, client: MongoProjectsDatabase, project: str) -> None:
        super().__init__()
        self._client = client
        self._project = project

        
    def put_data(self, data: dict) -> bool:
        try:
            _ = self._client.find(prj_name=self._project)

            print(_)

            return True
        except Exception as e:
            print(e)
            return False


        


    