# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
from nightcapcore.printers import PrinterBase
from colorama import Fore, Back, Style


class ItemPrinter(PrinterBase):
    def __init__(self):
        super().__init__()

    def item_1(self, leadingTab=2, leadingText="[-]", text="", optionalText="", leadingBreaks=0, endingBreaks=0, vtabs=0,seperator=' -> ', 
               leadingColor=Fore.LIGHTGREEN_EX, textColor=Fore.LIGHTYELLOW_EX, optionalTextColor=Fore.LIGHTBLUE_EX,
               breakTextColor=Fore.LIGHTMAGENTA_EX, styleRest=Style.RESET_ALL):

            self.base_print(leadingText=leadingText, leadingTab=leadingTab, text=text, optionalText=optionalText, leadingBreaks=leadingBreaks,
            endingBreaks=endingBreaks, vtabs=vtabs,leadingColor=leadingColor, textColor=textColor, optionalTextColor=optionalTextColor,seperator=seperator,
            breakTextColor=breakTextColor, styleRest=styleRest)

    def item_2(self, leadingTab=3, leadingText="-", text="", optionalText="", leadingBreaks=0, endingBreaks=0, vtabs=0,seperator=' : ', 
               leadingColor=Fore.LIGHTGREEN_EX, textColor=Fore.LIGHTYELLOW_EX, optionalTextColor=Fore.LIGHTBLUE_EX,
               breakTextColor=Fore.LIGHTMAGENTA_EX, styleRest=Style.RESET_ALL):

            self.base_print(leadingText=leadingText, leadingTab=leadingTab, text=text, optionalText=optionalText, leadingBreaks=leadingBreaks,
            endingBreaks=endingBreaks, vtabs=vtabs,leadingColor=leadingColor, textColor=textColor, optionalTextColor=optionalTextColor,seperator=seperator,
            breakTextColor=breakTextColor, styleRest=styleRest)

    def item_3(self, leadingTab=4, leadingText="*", text="", optionalText="", leadingBreaks=0, endingBreaks=0, vtabs=0,seperator=' : ', 
               leadingColor=Fore.LIGHTGREEN_EX, textColor=Fore.LIGHTYELLOW_EX, optionalTextColor=Fore.LIGHTBLUE_EX,
               breakTextColor=Fore.LIGHTMAGENTA_EX, styleRest=Style.RESET_ALL):

            self.base_print(leadingText=leadingText, leadingTab=leadingTab, text=text, optionalText=optionalText, leadingBreaks=leadingBreaks,
            endingBreaks=endingBreaks, vtabs=vtabs,leadingColor=leadingColor, textColor=textColor, optionalTextColor=optionalTextColor,seperator=seperator,
            breakTextColor=breakTextColor, styleRest=styleRest)
