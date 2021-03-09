# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
import os
from nightcapcore.configuration.configuration import NighcapCoreCLIBaseConfiguration
import pyshark
from nightcapcore.params import NightcapDynamicParams

class NightcapCLIConfiguration(NightcapDynamicParams, NighcapCoreCLIBaseConfiguration):
    def __init__(self,generatePcaps: bool = False,basedata: dict = None,verboselevel: int = 0):
        NighcapCoreCLIBaseConfiguration.__init__(self)
        NightcapDynamicParams.__init__(self,params=basedata,verboselevel=verboselevel)
        self.basedata = basedata
        if basedata != None:
            self.package_params = dict(basedata)['1']
        self.pcapFiles = []
        if(generatePcaps):
            if(self.isDir):
                self.pcapFiles = []

                exts = self.currentConfig["NIGHTCAPCORE"]["extentions"].split(' ')

                for root, dirs, files in os.walk(self.dir, topdown=False):
                    for name in files:
                        if(name.split('.')[1] in exts):
                            self.pcapFiles.append(pyshark.FileCapture(os.path.join(root, name)))
            else:
                self.pcapFiles = [pyshark.FileCapture(os.path.join(self.dir,self.filename))] # open PCAP

    def get_currentConfig(self):
        return super.currentConfig
                