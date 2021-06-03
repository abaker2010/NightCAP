# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Imports
import os
import platform

# endregion


class ScreenHelper(object):
    """

    This class is used to help with screen actions

    ...

    Methods
    -------
        Accessible
        -------
            clearScr(self): -> None
                Will clear the screen visible to the user

    """

    # region Init
    def __init__(self) -> None:
        super().__init__()

    # endregion

    # region Clear Screen
    def clearScr(self) -> None:
        if platform.system() == "windows":
            os.system("cls")
        else:
            os.system("clear")

    # endregion
