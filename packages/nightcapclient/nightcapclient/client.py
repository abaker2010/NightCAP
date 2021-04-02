# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
import argparse
import json
from nightcapcore import NightcapCLIConfiguration
import abc
from abc import abstractmethod

from nightcapcore.configuration.package_config import NightcapCLIPackageConfiguration

class NightcapScanner(NightcapCLIPackageConfiguration):
    def __init__(self, intro: str = None):
        parser = argparse.ArgumentParser(description="Process some pcaps.")
        parser.add_argument("--data", required=True, help="list of pcap filenames")
        args = parser.parse_args()
        # print("Args after passing", args)
        # print("Args after passing", args.data)
        # print("Args after passing", dict(json.loads(args.data)))

        try:
            NightcapCLIPackageConfiguration.__init__(self, dict(json.loads(args.data))['2'])
        except Exception as e:
            print("Error 1", e)
        print("Client generate PCAPS:", self.generatePcaps)

        self.captures = self._get_pcaps()
        # NightcapCLIConfiguration.__init__(
        #     self, generatePcaps=True, basedata=dict(json.loads(args.data))
        # )
        # print(self.generatePcaps)
        # print(self.nc_pacakge_config)
        # try:
        #     self.pkg_config = NightcapCLIPackageConfiguration(self.config, dict(json.loads(args.data))['2'])
        #     # nc_pacakge_config=dict(json.loads(args.data))['2']
        # except Exception as e:
        #     print("Error 2", e)
        # print(self.pkg_config.pcaps)

        return []
    def onClose(self):
        """Todo when the process is done"""
        raise NotImplementedError

    def onIntro(self):
        """Intro to the program"""
        self.printer.print_formatted_additional("Please wait while processing PCAP files...", endingBreaks=1)

    @abc.abstractmethod
    def onProcess(self):
        """Process to do"""
        raise NotImplementedError

    @abc.abstractmethod
    def onReport(self):
        """Generate Reports"""
        raise NotImplementedError

    
    def onRun(self):
        """Run the program"""
        try:
            self.onIntro()
        except Exception as e:
            self.printer.print_error(Exception("Error with Intro"))
            raise e

        try:
            self.onProcess()
        except Exception as e:
            self.printer.print_error(Exception("Error with Processing"))
            raise e

        try:
            self.onReport()
        except Exception as e:
            self.printer.print_error(Exception("Error with Reporting"))
            raise e


    def run(self):
        self.onRun()