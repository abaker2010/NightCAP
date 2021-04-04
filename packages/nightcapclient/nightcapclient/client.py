# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
#region Imports
import argparse
import json
import abc
from abc import abstractmethod
from nightcapcore.configuration.package_config import NightcapCLIPackageConfiguration
#endregion

class NightcapScanner(NightcapCLIPackageConfiguration):
    """
        
        This class is used to allows the Nightcap program to interact with the installed scanners

        ...

        Attributes
        ----------
            ** Not including those inherited from NightcapCLIPackageConfiguration for now

            captures: -> List<FileCapture>
                returns a list of FileCaptures for the scanner to work with

        Methods 
        -------
            Accessible 
            -------
                onClose(self): -> NotImplementedError
                    After the package is ran

                onIntro(self): -> NotImplementedError
                    Intro before the client package is executed

                onProcess(self): -> NotImplementedError
                    - User Must Implement
                    This is the code that the user is running in the package

                onReport(self): -> NotImplementedError
                    - User Must Implement
                    This will be the way that the user generates reports

                onRun(self): -> None
                    This will try and run the package 

                run(self): -> None
                    Allows the user to have the clean Object.run() syntax

    """
    #region Init
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
    #endregion

    #region onClose
    def onClose(self):
        """Todo when the process is done"""
        raise NotImplementedError
    #endregion

    #region onIntro
    def onIntro(self):
        """Intro to the program"""
        self.printer.print_formatted_additional("Please wait while processing PCAP files...", endingBreaks=1)
    #endregion

    #region onProcess
    @abc.abstractmethod
    def onProcess(self):
        """Process to do"""
        raise NotImplementedError
    #endregion

    #region onReport
    @abc.abstractmethod
    def onReport(self):
        """Generate Reports"""
        raise NotImplementedError
    #endregion

    #region onRun
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
    #endregion

    #region run
    def run(self):
        self.onRun()
    #endregion