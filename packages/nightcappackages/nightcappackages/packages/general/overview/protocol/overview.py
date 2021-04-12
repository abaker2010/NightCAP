# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
#region Imports
from colorama import Fore
from nightcapclient import NightcapScanner
from nightcapcore import *
import re
import json
from pyshark.packet.packet import Packet
#endregion

class ProtocolOverviewScanner(NightcapScanner):
    """ 
        This class is used to detect XMRig malware strains 
    """
    #region Overview
    # wire shark is getting this mixed up with a bad header so that is why it is showing funny in the 
    # program not their fault but is it because the coin miner is able to by pass firewalls and such this way
    # In here needs to be regex parser try catchs for each one found then 
    # have a dict like {Loging : {}, Job : {}, Error : {}}
    # use the json to c# to build the needed objects that the logic will need

    # in each instance this needs to add information to the httpinfo dict in the malform header section
    # then when printing the malformed header needs to be checked and printed if there is any information to be displayed
    #endregion

    #region Init
    def __init__(self):
        NightcapScanner.__init__(self)
        self.found_count = 0
        self.collected = {}
    #endregion

    #region Check LayerName
    def Check_Layername(self, layer):
        layerName = None
        if layer._layer_name.lower() == "fake-field-wrapper":
            layerName = layer.layer_name
        else:
            layerName = layer._layer_name
        return layerName
    #endregion

    #region Protcol Checking
    def Check_Protocol(self, layerName):
        if layerName in self.collected:
            self.collected[layerName] += 1
        else:
            self.collected[layerName] = 1
        return
    #endregion

    #region Process
    def onProcess(self, pkt: Packet, count: int):
        # print("Processing packet")
        try:
            for layer in pkt:
                try:
                    layerName = self.Check_Layername(layer)
                    self.Check_Protocol(layerName)
                    self.found_count += 1
                except Exception as e:
                    self.printer.print_error(e)
        except Exception as e:
            print(e)
            pass
      
    #endregion

    #region Close
    def onClose(self):
        self.collected = {}
        self.found_count = 0
        return super().onClose()

    #endregion

    #region Console Print
    def onConsolePrint(self):
        self.printer.print_underlined_header_undecorated("Protocol Report")
        self.printer.print_underlined_header("Packet Layers Counted: " + str(self.found_count), leadingTab=2, leadingColor=Fore.LIGHTGREEN_EX)
        if self.collected != {}:
            for k, v in self.collected.items():
                self.printer.item_3(str(k).upper(), str(v), leadingTab=3)

        print()
    #endregion

    #region Report
    def onReport(self):
        # print("Generating Reports")
        pass
    #endregion

def main():
    ncore = ProtocolOverviewScanner()
    try:
        
        ncore.printer.print_underlined_header("Protocol Overview")
        ncore.run()

    except Exception as e:
        ncore.printer.print_error(e)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit()
    except Exception as e:
        print(e)
    finally:
        exit()
