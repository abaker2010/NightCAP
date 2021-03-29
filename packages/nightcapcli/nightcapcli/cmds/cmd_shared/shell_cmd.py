# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.

import os
import cmd
from colorama.ansi import Fore, Style


class ShellCMDMixin(cmd.Cmd, object):
    def do_shell(self, s):
        "\n\tRun a shell command, becareful with this. This feature is still in beta\n"
        print(Fore.LIGHTGREEN_EX)
        os.system(s)
        print(Style.RESET_ALL)
