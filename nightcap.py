#!/usr/bin/env python3.8
# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Imports
from src.shutdown_checks import NightcapShutdownChecks
from nightcapcore.context.context import Context
import os
from src.boot_checks import NightcapBootChecks
import sys
import colorama
from nightcapcli.observer.publisher import NightcapCLIPublisher
from nightcapcore import ScreenHelper, Printer
from pymongo.errors import ServerSelectionTimeoutError
from src.nightcap import Nightcap

DEVNULL = open(os.devnull, "wb")
try:
    import readline

    if "libedit" in readline.__doc__:
        readline.parse_and_bind("bind ^I rl_complete")
    else:
        readline.parse_and_bind("tab: complete")
except ImportError:
    sys.stdout.write("No readline module found, no tab completion available.\n")
else:
    import rlcompleter
# endregion

# region Main
def main():
    """

    This class is used as the main entry to the program

    """
    _printer = Printer()
    try:
        colorama.init()
        try:
            context = Context(NightcapBootChecks())
            _ = context.execute()
            if _:
                ScreenHelper().clearScr()
                _who = Nightcap([], "basecli")
                NightcapCLIPublisher().register("basecli", _who)

                l = _who.precmd("banner")
                r = _who.onecmd(l)
                r = _who.postcmd(r, l)
                if not r:
                    _who.cmdloop()
            # else:
            #     _printer.print_error(Exception("Error with connecting to Docker"))
        except ServerSelectionTimeoutError as e:
            raise e
        except Exception as e:
            raise e

    except KeyboardInterrupt as ke:
        ScreenHelper().clearScr()
        _printer.print_formatted_delete(text="Forced Termination!! ")
        exit()
    except Exception as e:
        _printer.print_error(e)
    finally:

        _printer.print_underlined_header("Cleaning up...")
        try:
            context = Context(NightcapShutdownChecks())
            context.execute()
        except Exception as e:
            _printer.print_error(e)


# endregion

# region __NAME__
if __name__ == "__main__":
    main()
# endregion
