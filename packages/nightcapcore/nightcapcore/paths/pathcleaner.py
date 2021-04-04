# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Imports
import os

# endregion


class NightcapPathCleaner(object):
    """

    This class is used to clean the system paths

    ...

    Attributes
    ----------
        cwd: -> str
            The currect dir

    Methods
    -------
        Accessible
        -------
            combine_with_base(self, path: str, paths: list = []): -> str
                this will combime the programs current path with the needed path for running packages

    """

    # region Init
    def __init__(self, cwd: str):
        self.cwd = cwd

    # endregion

    # region Combine with base
    def combine_with_base(self, path: str, paths: list = []):
        _cleaned_list = list(map(lambda v: str(v), paths))
        return os.sep.join([self.cwd, path, os.sep.join(_cleaned_list)])

    # endregion
