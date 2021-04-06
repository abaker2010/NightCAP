# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Imports
import argparse
import json
import abc
import time
from abc import abstractmethod
from nightcapcore.configuration.package_config import NightcapCLIPackageConfiguration
from pyshark.packet.packet import Packet
# endregion


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

    # region Init
    def __init__(self, intro: str = None, *args, keep_packets=True, display_filter=None, only_summaries=False,
                 decryption_key=None, encryption_type="wpa-pwk", decode_as=None,
                 disable_protocol=None, tshark_path=None, override_prefs=None,
                 use_json=False, output_file=None, include_raw=False, eventloop=None, custom_parameters=None,
                 debug=False, **kwargs):
        parser = argparse.ArgumentParser(description="Process some pcaps.")
        parser.add_argument("--data", required=True, help="list of pcap filenames")
        args = parser.parse_args()
        # print("Args after passing", args)
        # print("\n\nArgs after passing", args.data, "\n\n")
        # print("Args after passing", dict(json.loads(args.data)))

        try:
            # print("Tring to pass json on to client", dict(json.loads(args.data)))
            NightcapCLIPackageConfiguration.__init__(
                self, dict(json.loads(args.data))["2"], dict(json.loads(args.data))["0"]
            )

            self._keep_packets = keep_packets
            self._display_filter = display_filter
            self._only_summaries = only_summaries
            self._decryption_key = decryption_key
            self._encryption_type = encryption_type
            self._decode_as = decode_as
            self._disable_protocol = disable_protocol
            self._tshark_path = tshark_path
            self._override_prefs = override_prefs
            self._use_json = use_json
            self._output_file = output_file
            self._include_raw = include_raw
            self._eventloop = eventloop
            self._custom_parameters = custom_parameters
            self._debug = debug

        except Exception as e:
            print("Error 1", e)
        # print("Client generate PCAPS:", self.generatePcaps)

        # self.captures = self.get_pcaps(display_filter='dhcp')
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

    # endregion

    # region onClose
    def onClose(self):
        """Todo when the process is done"""
        self.printer.print_formatted_check('Elapse time (seconds)', str(round(self._elapseTime, 3)), endingBreaks=1)
    # endregion

    # region onConsolePrint
    @abc.abstractmethod
    def onConsolePrint(self):
        """Generate Console Report"""
        raise NotImplementedError

    # endregion

    # region onIntro
    def onIntro(self):
        """Intro to the program"""
        self.show_params()
        self.printer.print_formatted_additional(
            "Please wait while processing PCAP files...", endingBreaks=1
        )

    # endregion

    # region onProcess
    @abc.abstractmethod
    def onProcess(self, pkt: Packet, count: int):
        """Process to do"""
        raise NotImplementedError

    # endregion

    # region onReport
    @abc.abstractmethod
    def onReport(self):
        """Generate Reports"""
        raise NotImplementedError

    # endregion

    # region onRun
    def onRun(self):
        """Run the program"""
        try:
            self.onIntro()
        except Exception as e:
            self.printer.print_error(Exception("Error with Intro"))
            raise e

        try:
            start = time.time()
            for cpt in self.get_pcaps(display_filter=self._display_filter):
                _count = 1
                for pkt in cpt:
                    # print(type(pkt))
                    self.onProcess(pkt, _count)
                    _count += 1
            self._elapseTime = time.time() - start
            print("")
        except Exception as e:
            self.printer.print_error(Exception("Error with Processing"))
            print(e)
            raise e

        try:
            self.onReport()
        except Exception as e:
            self.printer.print_error(Exception("Error with Reporting"))
            raise e

        try:
            self.onConsolePrint()
        except Exception as e:
            self.printer.print_error(Exception("Error with Console Printing"))
            raise e

        try:
            self.onClose()
        except Exception as e:
            self.printer.print_error(Exception("Error with Closing"))
            raise e

    # endregion

    # region run
    def run(self):
        self.onRun()

    # endregion
