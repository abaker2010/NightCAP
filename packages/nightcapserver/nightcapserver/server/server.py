# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
from pathlib import Path
import sys
import time
from nightcapcore import NightcapCLIConfiguration, Printer
from nightcapcore.singleton.singleton import (
    Singleton,
)  # Our http server handler for http requests
from subprocess import Popen, PIPE, STDOUT
import os
import psutil
import subprocess

DEVNULL = open(os.devnull, "wb")


class NighcapCoreSimpleServer(object):
    def __init__(self, config: NightcapCLIConfiguration):
        self.config = config
        # self.ip = self.config["REPORTINGSERVER"]["ip"]
        # self.port = int(self.config["REPORTINGSERVER"]["port"])
        self.proc = self.config.config["REPORTINGSERVER"]["proc"]
        # self.status = self.config["REPORTINGSERVER"]["status"]
        self.pproc = None
        self.printer = Printer()

    def get_url(self):
        return "http://%s:%s/" % (
            self.config.config["REPORTINGSERVER"]["ip"],
            self.config.config["REPORTINGSERVER"]["port"],
        )

    def get_status(self):

        if self.config.config["REPORTINGSERVER"]["status"] == "False":
            return "DOWN"
        if self.config.config["REPORTINGSERVER"]["status"] == "True":
            return "UP"

    def start(self):
        try:
            call = "python3.8 %s runserver %s" % (
                os.path.join(os.path.dirname(__file__), "..", "..", "manage.py"),
                self.config.config["REPORTINGSERVER"]["port"],
            )
            print(call)
            self.pproc = Popen(
                call, shell=True, stdin=PIPE, stdout=DEVNULL, stderr=STDOUT
            )
            self.printer.print_formatted_additional(
                text="Starting Up Django Server", leadingBreaks=1, endingBreaks=1
            )
            self.config.config.set("REPORTINGSERVER", "status", "True")
            self.config.config.set("REPORTINGSERVER", "proc", self.pproc.pid)
            self.config.Save()

        except Exception as e:
            self.printer.print_error(e)

    def shutdown(self):
        self.status = False
        try:
            if self.proc != "None":
                self.printer.print_formatted_additional(
                    text="Shutting Down Web Server Please Wait...", leadingBreaks=1
                )
                process = psutil.Process(self.proc)
                for proc in process.children(recursive=True):
                    proc.kill()
                    while proc.is_running() == True:
                        time.sleep(0.5)
                self.config.config.set("REPORTINGSERVER", "status", "False")
                self.config.config.set("REPORTINGSERVER", "proc", "None")
                self.config.Save()
                self.printer.print_formatted_check(
                    text="Shutdown complete", endingBreaks=1
                )
            else:
                self.printer.print_formatted_check(
                    text="Server was not running", endingBreaks=1
                )
        except Exception as e:
            print(e)
