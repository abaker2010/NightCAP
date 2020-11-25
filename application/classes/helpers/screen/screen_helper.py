# Copyright 2020 by Aarom Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
#region imports
import os
import platform
#endregion

class ScreenHelper():
    def __init__(self):
        return

    def clearScr(self):
        if platform.system() == "windows":
            os.system('cls')
        else:
            os.system('clear')