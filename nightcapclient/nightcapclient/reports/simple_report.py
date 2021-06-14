# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.

#region Imports
from nightcapserver.server.reports.base.report import NightcapReport

#endregion

class NightcapSimpleReport(NightcapReport):

    def __init__(self, project: str, packageID: str, base_params: dict, params_used: dict) -> None:
        super().__init__(project, packageID, base_params, params_used)

 