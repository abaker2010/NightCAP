# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Imports
import enum

# endregion


class NightcapDockerStatus(enum.Enum):
    """

    This class is used as an enum for where to generate the docker status

    ...

    Attributes
    ----------
        ProjectBase
        Reporting
        ReportingTemplates

    """

    STOPPED = "stopped"
    RUNNING = "running"
    MISSING = "missing"
    EXISTS = "exists"
