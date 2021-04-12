# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
#region Imports
from colorama import Fore
from nightcapclient import NightcapScanner
from nightcapcore import *
import socket
from pyshark.packet.packet import Packet
#endregion

class TrafficOverviewScanner(NightcapScanner):
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
        self.fqdn = {}
    #endregion

    def _fqdn(self, ip):
        return socket.gethostbyaddr(ip)

    #region Process
    def onProcess(self, pkt: Packet, count: int):
        # print("Processing packet")
        try:
            if hasattr(pkt, 'ip') is True:
                try:
                    if pkt.ip.src_host not in self.collected.keys():
                        self.collected[pkt.ip.src_host] = {}
                    
                    if pkt.ip.dst_host not in self.collected[pkt.ip.src_host]:
                        self.collected[pkt.ip.src_host][pkt.ip.dst_host] = 1
                    else:
                        self.collected[pkt.ip.src_host][pkt.ip.dst_host] += 1

                    try:
                        if self.package_params['fqdn'] == "True":
                            try:
                                if pkt.ip.src_host not in self.fqdn.keys():
                                    self.fqdn[pkt.ip.src_host] = self._fqdn(pkt.ip.src_host)
                            except Exception as e:
                                self.fqdn[pkt.ip.src_host] = "Host Unknown"

                            try:
                                if pkt.ip.dst_host not in self.fqdn.keys():
                                    self.fqdn[pkt.ip.dst_host] = self._fqdn(pkt.ip.dst_host)
                            except Exception as e:
                                self.fqdn[pkt.ip.src_host] = "Host Unknown"
                    except:
                        pass
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)
            pass
      
    #endregion

    #region Close
    def onClose(self):
        self.collected = {}
        self.fqdn = {}
        self.found_count = 0
        return super().onClose()

    #endregion

    #region Console Print
    def onConsolePrint(self):
        self.printer.print_underlined_header_undecorated("Traffic Report")
        if self.collected != {}:
            for src, data in self.collected.items():
                self.printer.print_header_w_option(src, '(src addr)', leadingTab=2)
                for dst, count in dict(data).items():
                    self.printer.item_2(dst, count, leadingText="->")

        if self.package_params['fqdn'] == "True":
            self.printer.print_underlined_header_undecorated("FQDN Data")
            if self.fqdn != {}:
                for src, data in self.fqdn.items(): 
                    if data == "Host Unknown":
                        self.printer.item_2(src, data, leadingTab=2)
                    else:
                        self.printer.item_2(src, " ", leadingTab=2)
                        self.printer.item_2("Hostname", data[0], leadingTab=3)
                        self.printer.item_2("Alias List", data[1], leadingTab=3)
        print()
    #endregion

    #region Report
    def onReport(self):
        # print("Generating Reports")
        # print(self.package_params)
        pass
    #endregion

def main():
    ncore = TrafficOverviewScanner()
    try:
        
        # ncore.printer.print_underlined_header("Traffic Overview")
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
