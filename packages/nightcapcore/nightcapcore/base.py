# Copyright 2020 by Aarom Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
import os
import pyshark
from nightcapcore.configuration import NighcapCoreConfiguration
from nightcapcore.params import NightcapDynamicParams

class NightcapCoreBase(NightcapDynamicParams):
    def __init__(self,generatePcaps: bool = False,basedata: dict = None,verboselevel: int = 0):
        NightcapDynamicParams.__init__(self,params=basedata,verboselevel=verboselevel)
        config = NighcapCoreConfiguration()
        self.basedata = basedata
        if basedata != None:
            self.package_params = dict(basedata)['1']
        self.pcapFiles = []
        if(generatePcaps):
            if(self.isDir):
                self.pcapFiles = []

                exts = config.Config()["NIGHTCAPCORE"]["extentions"].split(' ')

                for root, dirs, files in os.walk(self.dir, topdown=False):
                    for name in files:
                        if(name.split('.')[1] in exts):
                            self.pcapFiles.append(pyshark.FileCapture(os.path.join(root, name)))
            else:
                self.pcapFiles = [pyshark.FileCapture(os.path.join(self.dir,self.filename))] # open PCAP
                