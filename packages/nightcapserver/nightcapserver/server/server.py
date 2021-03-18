# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
import sys
import time
from nightcapcore import NighcapCoreCLIBaseConfiguration, Printer
from nightcapcore.configuration.base import NightcapCLIConfiguration
from nightcapcore.singleton.singleton import Singleton # Our http server handler for http requests
from subprocess import Popen, PIPE, STDOUT
import os
import psutil
import subprocess
DEVNULL = open(os.devnull, 'wb')
 
class NighcapCoreSimpleServer(object):
    def __init__(self, config: NightcapCLIConfiguration):
        self.config = config
        # self.ip = self.config["REPORTINGSERVER"]["ip"]
        # self.port = int(self.config["REPORTINGSERVER"]["port"])
        self.proc = self.config.currentConfig["REPORTINGSERVER"]["proc"]
        # self.status = self.config["REPORTINGSERVER"]["status"]
        self.pproc = None
        self.printer = Printer()

    def get_url(self):
        return "https://%s:%s/" % (self.config.currentConfig["REPORTINGSERVER"]["ip"], self.config.currentConfig["REPORTINGSERVER"]["port"])

    def get_status(self):
        
        if(self.config.currentConfig["REPORTINGSERVER"]["status"] == "False"):
            return "DOWN"
        if(self.config.currentConfig["REPORTINGSERVER"]["status"] == "True"):
            return "UP"

    def start(self):
        try:
            call = "python3.8 %s runserver %s" % (os.path.join(os.path.dirname(__file__), "../nightcapsite/manage.py"), self.config.currentConfig['REPORTINGSERVER']['port'])
            self.pproc = Popen(call, shell=True, stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
            self.printer.print_formatted_additional(text="Starting Up Django Server", leadingBreaks=1, endingBreaks=1)
            self.config.currentConfig.set("REPORTINGSERVER","status", 'True')
            self.config.currentConfig.set("REPORTINGSERVER","proc", self.pproc.pid)
            self.config.Save()

        except Exception as e:
            self.printer.print_error(exception=e)


    def shutdown(self):
        self.status = False
        try:
            if self.proc != "None":
                self.printer.print_formatted_additional(text="Shutting Down Web Server Please Wait...", leadingBreaks=1)
                process = psutil.Process(self.proc)
                for proc in process.children(recursive=True):
                    proc.kill()
                    while proc.is_running() == True:
                        time.sleep(.5)
                self.config.currentConfig.set("REPORTINGSERVER","status", 'False')
                self.config.currentConfig.set("REPORTINGSERVER","proc", "None")
                self.config.Save()
                self.printer.print_formatted_check(text="Shutdown complete", endingBreaks=1)
            else:
                self.printer.print_formatted_check(text="Server was not running", endingBreaks=1)
        except Exception as e:
            print(e)