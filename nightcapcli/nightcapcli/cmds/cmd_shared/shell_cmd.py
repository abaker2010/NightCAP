# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Imports
import os
import cmd
from typing import IO, Optional
from colorama.ansi import Fore, Style

# endregion


class ShellCMDMixin(cmd.Cmd, object):
    """
    This class is used to allow the user to enter shell commands

    ...
    Methods
    -------
        do_shell(self, line): -> None
            This allows the user to enter shell commands if they need to
        -------

    """

    def __init__(
        self, completekey: str, stdin: Optional[IO[str]], stdout: Optional[IO[str]]
    ) -> None:
        super().__init__(completekey=completekey, stdin=stdin, stdout=stdout)

    def do_shell(self, s) -> None:
        "\n\tRun a shell command, becareful with this. This feature is still in beta\n"
        print(Fore.LIGHTGREEN_EX)
        os.system(s)
        print(Style.RESET_ALL)
