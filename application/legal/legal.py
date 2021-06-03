# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
#region Imports
from colorama import Fore, Style
#endregion

class Legal(object):
    """ Handles the legal header """
    def __init__(self) -> None:
        super().__init__()

    def termsAndConditions(self) -> None:
        print(Fore.LIGHTYELLOW_EX + "\n\tI shall not use nightcap to:")
        print("\t-----------------------------\n")
        print("\t\t(i) inspect or, display or distribute any content that")
        print(
            "\t\t\tinfringes any trademark, trade secret, copyright or other proprietary"
        )
        print(
            "\t\t\tor intellectual property rights of any person or company; \n\n"
            + Style.RESET_ALL
        )
