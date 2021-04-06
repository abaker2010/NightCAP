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

class XMRigScanner(NightcapScanner):
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
        NightcapScanner.__init__(self, display_filter='http')
        self.found_count = 0
        self.regex_1 = re.compile(r'{"jsonrpc":"\d.\d","method":"(\w+)","params":{(.+)}}', re.IGNORECASE)
        self.regex_2 = re.compile(r'{"id":\d+,"jsonrpc":"\d.\d","method":"(\w+)","params":{(.+)}}', re.IGNORECASE)
        self.regex_3 = re.compile(r'{"id":\d+,"jsonrpc":"\d.\d","error":(.+)}}', re.IGNORECASE)
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
    def onProcess(self, pkt: Packet, count: int):
        # This is processing each packet passed for XMRig cryptojacking
        try:
            src = pkt.ip.src + " -> " + pkt.ip.dst
            for layer in pkt:
                try:
                    if self.Check_Layername(layer) == "http":
                        if hasattr(layer, 'unknown_header') is True:
                            if self.regex_1.match(str(layer.unknown_header)) != None:
                                #region Checking for job packets
                                m = self.regex_1.match(str(layer.unknown_header))
                                if src not in self.collected:
                                    self.collected[src] = {"login" : {}, "job" : {count : m.group()}, "keepalived" : {}, "submit" : {}, "error" : {}}
                                else:
                                    self.collected[src]["job"][count] = m.group()
                                self.found_count += 1
                                #endregion

                            if self.regex_2.match(str(layer.unknown_header)) != None:
                                #region Checking for login, keepalive, and submit packets
                                m = self.regex_2.match(str(layer.unknown_header))
                                if m:
                                    # so far have found 'login', 'keepalived', 'submit'
                                    if m.group(1) == "login":
                                        if src not in self.collected:
                                            self.collected[src] = {"login" : {count : m.group()}, "job" : {}, "keepalived" : {}, "submit" : {}, "error" : {}}
                                        else:
                                            self.collected[src]["login"][count] = m.group()
                                    elif m.group(1) == 'keepalived':
                                        if src not in self.collected:
                                            self.collected[src] = {"login" : {}, "job" : {}, "keepalived" : {count : m.group()}, "submit" : {}, "error" : {}}
                                        else:
                                            self.collected[src]["keepalived"][count] = m.group()
                                    elif m.group(1) == 'submit':
                                        if src not in self.collected:
                                            self.collected[src] = {"login" : {}, "job" : {}, "keepalived" : {}, "submit" : {count : m.group()}, "error" : {}}
                                        else:
                                            self.collected[src]["submit"][count] = m.group()
                                self.found_count += 1
                                #endregion

                            if self.regex_3.match(str(layer.unknown_header)):
                                #region Checking for error packets being sent
                                m = self.regex_2.match(str(layer.unknown_header))
                                if m:
                                    if src not in self.collected:
                                        self.collected[src] = {"login" : {}, "job" : {}, "keepalived" : {}, "submit" : {}, "error" : {count : m.group()}}
                                    else:
                                        self.collected[src]["error"][count] = m.group()
                                self.found_count += 1
                                #endregion
                except Exception as e:
                    pass
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
        try:
            self.printer.print_underlined_header_undecorated("XMRig Scan Report")
            self.printer.print_formatted_additional("Packets Counted", str(self.found_count), leadingTab=2, leadingColor=Fore.LIGHTGREEN_EX)
            if self.collected != {}:
                self.printer.print_formatted_delete("XMRig strain found", endingBreaks=1)
                self.printer.print_underlined_header("Details")

                for src, data in self.collected.items():
                    self.printer.print_underlined_header_undecorated(src, leadingTab=2)
                    
                    if data != {}:
                        for _type, pkts in data.items():
                            self.printer.print_underlined_header_undecorated(_type, leadingTab=3)
                            if len(pkts) != 0:
                                # self.printer.print_formatted_additional("PKTS", str(pkts))
                                self.printer.print_underlined_header("Sample Found: " + str(list(pkts)[0]), leadingTab=4)

                                json_acceptable_string = str(pkts[list(pkts)[0]]).replace("'", "\"")
                                d = json.loads(json_acceptable_string)
                                for k, v in d.items():
                                    if type(v) == dict:
                                        self.printer.item_3(str(k), ' ',leadingTab=5)
                                        for k1, v1 in v.items():
                                            self.printer.item_2(str(k1), str(v1), leadingTab=6)
                                    else:
                                        self.printer.item_3(str(k), str(v), leadingTab=5)

                                # for k, v in dict(str(pkts[list(pkts)[0]]).).items():
                                #     self.printer.print_formatted_additional(str(k), str(v), leadingTab=5)
                            else:
                                self.printer.print_formatted_check("No packets found", textColor=Fore.CYAN, leadingTab=4, endingBreaks=1)
                            
                        # print("SRC", src)
                        # print("Count", count)
            else:
                self.printer.print_formatted_check("XMRig strain not found")
        except Exception as e:
            print(e)
    #endregion

    #region Report
    def onReport(self):
        print("Generating Reports")
    #endregion

def main():
    ncore = XMRigScanner()
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
