# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
from colorama import Fore, Style

class NightcapCoreConsoleOutput(object):
    def __init__(self) -> None:
        return

    def input(self, text: str,width: int = 75,sep: str = ' ',color: Fore = Fore.RED,inputcolor: Fore = Fore.YELLOW):
        return input(color + str(text).center(width,sep) + inputcolor)

    def output(self, text, level=0, width=100, sep=' ', color=None):
        if(level == 0):
            if(color == None):
                self._verbose(text,width=width, sep=sep)
            else:
                self._verbose(text,width=width, sep=sep,color=color)
        elif(level == 1):
            if(color == None):
                self._verbose_one(text,width=width, sep=sep)
            else:
                self._verbose_one(text,width=width, sep=sep,color=color)
        elif(level == 2):
            if(color == None):
                self._verbose_two(text,width=width, sep=sep)
            else:
                self._verbose_two(text,width=width, sep=sep,color=color)
        elif(level == 3):
            if(color == None):
                self._verbose_three(text,width=width, sep=sep)
            else:
                self._verbose_three(text,width=width, sep=sep,color=color)
        elif(level == 4):
            if(color == None):
                self._verbose_four(text,width=width, sep=sep)
        elif(level == 5):
            if(color == None):
                self._verbose_five(text,width=width, sep=sep)
            else:
                self._verbose_five(text,width=width, sep=sep,color=color)
        elif(level == 6):
            if(color == None):
                self._warning(text,width=width, sep=sep)
            else:
                self._warning(text,width=width, sep=sep,color=color)
        elif(level == 7):
            if(color == None):
                self._header(text,width=width, sep=sep)
            else:
                self._header(text,width=width, sep=sep,color=color)

    def _verbose(self, text, width=100, sep=' ', color=Fore.LIGHTGREEN_EX):
        print(str(color + "\t" + str(text) + Style.RESET_ALL).center(width, sep))

    def _verbose_one(self, text, width=100, sep=' ', color=Fore.LIGHTBLUE_EX):
        print(str(color + "\t" + str(text) + Style.RESET_ALL).center(width, sep))

    def _verbose_two(self, text, width=100, sep=' ', color=Fore.LIGHTYELLOW_EX):
        print(str(color + "\t" + str(text) + Style.RESET_ALL).center(width, sep))

    def _verbose_three(self, text, width=100, sep=' ', color=Fore.LIGHTCYAN_EX):
        print(str(color + "\t" + str(text) + Style.RESET_ALL).center(width, sep))

    def _verbose_four(self, text, width=100, sep=' ', color=Fore.GREEN):
        print(str(color + "\t" + str(text) + Style.RESET_ALL).center(width, sep))

    def _verbose_five(self, text, width=100, sep=' ', color=Fore.MAGENTA):
        print(str(color + "\t" + str(text) + Style.RESET_ALL).center(width, sep))

    def _warning(self, text, width=100, sep=' ', color=Fore.RED):
        print(str(color + "\tWARNING: " + str(text) + Style.RESET_ALL).center(width, sep))

    def _header(self, text, width=100, sep=' ', color=Fore.CYAN):
        print(str(color + "\t" + str("*"*int(width/1.2)) + Style.RESET_ALL).center(width, sep))
        print(str(color + "\t" + str(text) + Style.RESET_ALL).center(width, sep))
        print(str(color + "\t" + str("*"*int(width/1.2)) + Style.RESET_ALL).center(width, sep))