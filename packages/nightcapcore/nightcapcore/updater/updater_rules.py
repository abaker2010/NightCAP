# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
import enum

class NightcapCoreUpaterRules(enum.Enum):
    Basic = 0,
    Module = 1,
    Submodule = 2,
    Package = 3
    
    