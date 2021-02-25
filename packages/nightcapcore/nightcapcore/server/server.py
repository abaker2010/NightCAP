# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
from nightcapcore.configuration import NighcapCoreConfiguration
from nightcapcore.decorators.singleton import Singleton # Our http server handler for http requests
from subprocess import Popen, PIPE, STDOUT
import os
DEVNULL = open(os.devnull, 'wb')
 
@Singleton
class NighcapCoreSimpleServer(object):
    def __init__(self):
        self.config = NighcapCoreConfiguration().Config()
        self.ip = self.config["REPORTINGSERVER"]["ip"]
        self.port = int(self.config["REPORTINGSERVER"]["port"])
        self.proc = self.config["REPORTINGSERVER"]["proc"]
        self.status = self.config["REPORTINGSERVER"]["status"]
        self.pproc = None

    def get_url(self):
        return "http://%s:%s/" % (self.ip, self.port)

    def get_status(self):
        if(self.status == "False"):
            return "DOWN"
        if(self.status == "True"):
            return "UP"

    def start(self):
        call = "python3.8 %s --ip %s --port %s" % (os.path.join(os.path.dirname(__file__), "_server.py"), str(self.ip), str(self.port))
        print(call)
        self.pproc = Popen(call, shell=True, stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
        print("Process ID Created", self.pproc.pid)
        self.status = "True"

    def shutdown(self):
        self.status = False
        try:
            if self.pproc.poll() is None:
                print("Killing process with pid %s " % (self.pproc.pid))
                self.pproc.kill()
                self.status = "False"
        except Exception as e:
            print(e)