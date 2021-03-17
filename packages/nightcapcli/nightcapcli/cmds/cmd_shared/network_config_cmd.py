# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
from nightcapcli.base.base_cmd import NightcapBaseCMD
from nightcapcore import *
from colorama import Fore

class NightcapMongoNetworkSettingsCMD(NightcapBaseCMD):
    def __init__(self, networkopt: str, configuration: NightcapCLIConfiguration):
        self.network = ''
        if networkopt == 'database':
            NightcapBaseCMD.__init__(self,["settings","server","database"],configuration)
            self.network = 'MONGOSERVER'
        elif networkopt == 'web':
            NightcapBaseCMD.__init__(self,["settings","server","web"],configuration)
            self.network = 'REPORTINGSERVER'

    def help_config(self):
        self.printer.help(text="Shows current configuration")

    def do_config(self, line):
        self.printer.print_underlined_header(text='CURRENT CONFIG')
        self.printer.print_formatted_other(text='IP', optionaltext=self.config.currentConfig[self.network]['ip'], leadingTab=2, optionalTextColor=Fore.MAGENTA)
        self.printer.print_formatted_other(text='Port', optionaltext=self.config.currentConfig[self.network]['port'], endingBreaks=1, leadingTab=2, optionalTextColor=Fore.MAGENTA)

    def _isvalidIPAddress(self, IP):
      """
      :type IP: str
      :rtype: str
      """
      def isIPv4(s):
         try: return str(int(s)) == s and 0 <= int(s) <= 255
         except: return False
      def isIPv6(s):
         if len(s) > 4:
            return False
         try : return int(s, 16) >= 0 and s[0] != '-'
         except:
            return False
      if IP.count(".") == 3 and all(isIPv4(i) for i in IP.split(".")):
         return True
      if IP.count(":") == 7 and all(isIPv6(i) for i in IP.split(":")):
         return True
      return False

    def help_ip(self):
        self.printer.help(text="Sets a new IP Address", optionalText='ip [IP Address]')

    def do_ip(self,line):
        print("Set IP")
        try:
            print("Change IP address for django server")
            if str(line).lower() == 'localhost':
                self.config.currentConfig.set(self.network,'ip','127.0.0.1')
                self.config.Save()
            elif(self._isvalidIPAddress(line)):
                self.config.currentConfig.set(self.network,'ip',line)
                self.config.Save()
            else:
                self.printer.print_error(exception=Exception("Error with setting IP Address { %s }, please try again" % line))    
        except Exception as e:
            self.printer.print_error(exception=e)

    def help_port(self):
        self.printer.help(text="Sets a new Port Number", optionalText='port [1-65535]')

    def do_port(self,line):
        print("Set port")
        try:
            port = int(line)
            if 1 <= port <= 65535:
                self.config.currentConfig.set(self.network,'port',line)
                self.config.Save()
            else:
                raise ValueError
        except ValueError:
            self.printer.print_error(exception=Exception("Error with setting Port { %s }. Expected range 1 - 65535, please try again" % line))
