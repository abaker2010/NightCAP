# Copyright 2020 by Aarom Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
import enum
import os

class NightcapPackagesPathsEnum(enum.Enum):
    ProjectBase = "classes"
    PackagesBase = "packages"
    Databases = ProjectBase + os.sep + "databases"
