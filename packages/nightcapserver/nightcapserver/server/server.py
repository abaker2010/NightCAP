# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
from nightcapcore import NighcapCoreCLIBaseConfiguration, Printer
from nightcapcore.singleton.singleton import Singleton # Our http server handler for http requests
from subprocess import Popen, PIPE, STDOUT
import os
import psutil
import subprocess
DEVNULL = open(os.devnull, 'wb')
 
class NighcapCoreSimpleServer(object, metaclass=Singleton):
    def __init__(self):
        self.config = NighcapCoreCLIBaseConfiguration().currentConfig
        self.ip = self.config["REPORTINGSERVER"]["ip"]
        self.port = int(self.config["REPORTINGSERVER"]["port"])
        self.proc = self.config["REPORTINGSERVER"]["proc"]
        self.status = self.config["REPORTINGSERVER"]["status"]
        self.pproc = None
        self.printer = Printer()

    def get_url(self):
        return "https://%s:%s/" % (self.ip, self.port)

    def get_status(self):
        if(self.status == "False"):
            return "DOWN"
        if(self.status == "True"):
            return "UP"

    def start(self):
        try:
            call = "python3.8 %s runserver %s" % (os.path.join(os.path.dirname(__file__), "../nightcapsite/manage.py"), self.config['REPORTINGSERVER']['port'])
            self.pproc = Popen(call, shell=True, stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
            self.printer.print_formatted_additional(text="Starting Up Django Server", leadingBreaks=1, endingBreaks=1)
            self.status = "True"
        except Exception as e:
            self.printer.print_error(exception=e)


    def shutdown(self):
        self.status = False
        try:
            if self.pproc.poll() is None:
                self.printer.print_formatted_additional(text="Shutting Down Django Server", leadingBreaks=1, endingBreaks=1)
                process = psutil.Process(self.pproc.pid)
                for proc in process.children(recursive=True):
                    proc.kill()
                self.status = "False"
        except Exception as e:
            print(e)