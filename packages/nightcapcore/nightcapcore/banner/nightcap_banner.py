# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region imports
from random import randint
from art import *
from colorama import Style, Fore
from nightcapcore import NightcapCLIConfiguration

# from application.classes.colors.nightcap_colors import NightcapColors
from nightcapserver import NighcapCoreSimpleServer
from nightcapcore.colors import NightcapColors

# endregion


class NightcapBanner(NightcapCLIConfiguration):
    def __init__(self):
        NightcapCLIConfiguration.__init__(self)
        self.build_version = self.config["BUILD_DATA"]["version"]
        self.build_number = self.config["BUILD_DATA"]["build"]

    def _randomColor(self):
        random = randint(0, 11)
        return NightcapColors().randomColor(random)

    def Banner(self, rand: bool = True):
        rcolor = None
        rcolor2 = self._randomColor()
        rcolor3 = self._randomColor()
        if rand == True:
            rcolor = self._randomColor()
        else:
            rcolor = NightcapColors().randomColor(0)

        print(rcolor)
        Art = text2art("Nightcap", font="rnd-medium")
        sart = Art.splitlines()
        for l in sart:
            print(l.center(125, " "))
        print("\n\t", "=" * 100)
        print("\t=", rcolor3, "Created By: Aaron Baker".center(96, " "), rcolor, "=")
        print("\t=", " " * 98, "=")
        try:
            version_string = rcolor + "Version ~ " + rcolor2 + self.build_version
            build_number_string = rcolor + "Build ~ " + rcolor2 + self.build_number
            print(
                "\t=",
                rcolor2,
                ("%s\t%s" % (version_string, build_number_string)).center(109, " "),
                rcolor,
                "=",
            )
        except:
            pass
        print("\t", "=" * 100, Style.RESET_ALL)
        return
