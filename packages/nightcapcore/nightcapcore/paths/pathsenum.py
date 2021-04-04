# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
#region Imports
import enum
import os
#endregion

class NightcapPathsEnum(enum.Enum):
    """
        
        This class is used as an enum for where to generate the package paths

        ...

        Attributes
        ----------
            ProjectBase
            Reporting
            ReportingTemplates

    """
    ProjectBase = os.sep.join(["nightcore", "nightcore"])
    Reporting = "reporting"
    ReportingTemplates = os.sep.join(["server", "webbase"])
