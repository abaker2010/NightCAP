#!/usr/bin/env python3.8
# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
#region imports
import sys
import colorama 
from colorama import Fore, Style
from application.classes.configuration.configuration import Configuration
from application.classes.nightcap import Nightcap
from application.classes.legal.legal import Legal
from application.classes.banners.nightcap_banner import NightcapBanner
from application.classes.helpers.screen.screen_helper import ScreenHelper
from nightcapcore import NighcapCoreSimpleServer
from application.classes.updater.updater import NightcapUpdater
        
try:
    import readline
    if 'libedit' in readline.__doc__:
        readline.parse_and_bind("bind ^I rl_complete")
    else:
        readline.parse_and_bind("tab: complete")
except ImportError:
    sys.stdout.write("No readline module found, no tab completion available.\n")
else:
    import rlcompleter
#endregion

#region Agreement
def Agreement(config: Configuration):
    """Legal agreement the at the user must accept to use the program"""
    _yes = config.Config().get('NIGHTCAP', 'yes').split()
    while not config.Config().getboolean("NIGHTCAP", "agreement"):
        ScreenHelper().clearScr()
        NightcapBanner(config).Banner()
        Legal().termsAndConditions()
        agree = input(Fore.LIGHTGREEN_EX + "\t\tYou must agree to our terms and conditions first (Y/n) " + Style.RESET_ALL).lower()

        if agree in _yes:
            config.Config().set('NIGHTCAP', 'agreement', 'true')
            conf.Save()
            ScreenHelper().clearScr()
            NightcapBanner(config).Banner()

    Nightcap(conf).cmdloop()
#endregion

#region Main named if for keyboard interrupt
if __name__ == '__main__':
    try:
        colorama.init()
        conf = Configuration()
        NightcapBanner(conf).Banner()
        Agreement(conf)

    except KeyboardInterrupt:
        print(Fore.RED + "\n\t[!] Forced Termination!! " + Style.RESET_ALL)
        exit()
    except Exception as e:
        print(e)
    finally:  
        NighcapCoreSimpleServer.instance().shutdown()   
        if(NightcapUpdater.instance().updateCalled):
            print("Changes need to be made:", "Updater called")
            print("Files that need modified")
            NightcapUpdater.instance().onCloseModifications()
        exit()
#endregion