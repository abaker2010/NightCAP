# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
#region Imports
from typing import Collection
from colorama import Fore
from nightcapclient import NightcapRedTeam
from nightcapcore import *
import re
import json
import nmap3
import pprint
from pyshark.packet.packet import Packet
#endregion

class NmapStandardRecon(NightcapRedTeam):
    """ 
        This is used for standard network recon
    """
    #region Overview
    # Used to do a standard nmap recon on a target more to be added soon
    #endregion

    #region Init
    def __init__(self):
        NightcapRedTeam.__init__(self)
        self.found_count = 0
        self.nmap = nmap3.Nmap()
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

    #region Process
    def onProcess(self):
        # This is processing each packet passed for XMRig cryptojacking
        try:
            self.printer.print_formatted_additional(self.package_params['host'])
            self.printer.print_formatted_check("Scanning...")
            self.collected = self.nmap.scan_top_ports(self.package_params['host'])
            # print(self.collected)
        except Exception as e:
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
        self.printer.print_underlined_header("Results")
        for host, _vals in self.collected.items():
            # print("Host", host)
            if host != "stats" and host != "runtime":
                self.printer.print_formatted_additional(text="Host", optionaltext=host)
                for _t, data in _vals.items():
                    if type(data) == str:
                        self.printer.item_2(text=_t, optionalText=data)

                    
                    # Dict
                    elif type(data) == dict:
                        if data != {}:
                            self.printer.item_2(text=_t)
                            for k, v in data.items():
                                self.printer.item_3(text=k, optionalText=v)
                        else:
                            self.printer.item_2(text=_t, optionalText="NONE")

                    
                    # List
                    elif type(data) == list:
                        if data != []:
                            self.printer.item_2(text=_t)
                            for i in data:
                                if 'state' in i.keys():
                                    if i['state'] == 'open':
                                        if 'portid' in i.keys():
                                            # self.printer.item_1(text=i)
                                            self.printer.item_3(text=i['portid'], optionalText=i['service']['name'])

                                if 'portid' not in i.keys():
                                    # print("Do something with data", i)
                                
                                    for k, v in i.items():
                                        self.printer.item_3(text=k, optionalText=v)
                        else:
                            self.printer.item_2(text=_t, optionalText="NONE")
                    elif data is None:
                        self.printer.item_2(text=_t, optionalText="NONE")
                    else:
                        self.printer.item_2(text=_t, optionalText="Changes need made with data " + str(type(data)))
        print()
    #endregion

    #region Report
    def onReport(self):
        pass
    #endregion

def main():
    ncore = NmapStandardRecon()
    try:
        
        ncore.printer.print_underlined_header("Scanning")
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
