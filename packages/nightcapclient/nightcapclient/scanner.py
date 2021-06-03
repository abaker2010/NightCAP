# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Imports
import argparse
import json
import abc
import os
import sys
import time
from abc import abstractmethod
from colorama import Fore
from colorama.ansi import Style
from nightcapcli.base.base_cmd import NightcapBaseCMD
from nightcapcore.configuration.package_config import NightcapCLIPackageConfiguration
from nightcapcore.printers.print import Printer
from nightcappackages.classes.helpers.encoder import NightcapJSONEncoder
import pyshark
from pyshark.packet.packet import Packet
# endregion


class NightcapScanner(NightcapBaseCMD):
    """

    This class is used to allows the Nightcap program to interact with the installed scanners

    ...

    Attributes
    ----------
        ** Not including those inherited from NightcapBaseCMD for now

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
                 debug=False, **kwargs)  -> None:
        parser = argparse.ArgumentParser(description="Process some pcaps.")
        parser.add_argument("--data", required=True,
                            help="list of pcap filenames")
        args = parser.parse_args()

        self.printer = Printer()

        try:
            _data = NightcapJSONEncoder().default(args.data)

            # print("Tring to pass json on to client", dict(json.loads(args.data)))
            NightcapBaseCMD.__init__(
                self, _data["2"], passedJson=_data["0"]
            )
            # _data = dict(json.loads(args.data))
            # print("Data needs fixed in the client", _data)
            self.base_params = _data["0"]
            self.package_params = _data["1"]
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
            self._elapseTime = 0

            self.printer.debug("Args after passing", args,
                               currentMode=self.config.verbosity)

        except Exception as e:
            print("Error 1", e)


    # endregion

    # region onClose
    def onClose(self):
        """Todo when the process is done"""
        try:
            self.printer.print_formatted_check('Elapse time (seconds)', str(
                round(self._elapseTime, 3)), endingBreaks=1)
        except Exception as e:
            print(e)
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
        try:
            if self.config.project != None or self.package_params != {}:
                self.printer.print_underlined_header("Scan Details: (Params Used)")
                
            if self.config.project != None:
                self.printer.print_underlined_header("Project", leadingTab=2)
                self.printer.item_1("ID", optionalText=self.base_params['project']['_id']['$oid'], seperator=" : ", leadingTab=3)
                self.printer.item_1("Name", optionalText=self.base_params['project']['project_name'], seperator=" : ", leadingTab=3)

                self.printer.print_underlined_header("Scan Params", leadingTab=2)                
                self.printer.item_1("isDir", optionalText=self.base_params['isDir'], seperator=" : ", leadingTab=3)
                self.printer.item_1("dir", optionalText=self.base_params['dir'], seperator=" : ", leadingTab=3)
                self.printer.item_1("filename", optionalText=self.base_params['filename'], seperator=" : ", leadingTab=3)
                
            if self.package_params != {}:
                self.printer.print_underlined_header("Package Params", leadingTab=2)
                for k, v in dict(self.package_params).items():
                    self.printer.item_1(str(k), optionalText=str(v), seperator=" : ", leadingTab=3)
        except Exception as e:
            self.printer.print_error(e)
        pass
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
            self.printer.print_formatted_additional("Running package. Please wait...", leadingTab=1, leadingBreaks=1, endingBreaks=1)
            for cpt in self.get_pcaps(display_filter=self._display_filter):
                _count = 1
                for pkt in cpt:
                    # print(type(pkt))
                    sys.stdout.write(Fore.LIGHTCYAN_EX + "\r\t\t[?] " + Fore.LIGHTGREEN_EX +
                                     "Scanning Packet # : " + Fore.LIGHTYELLOW_EX + str(_count) + Style.RESET_ALL)
                    try:
                        self.onProcess(pkt, _count)
                    except Exception as e:
                        print("There has been an error")
                        print(e)
                        pass
                    _count += 1
            self._elapseTime = time.time() - start
            print("")
        except Exception as e:
            self.printer.print_error(Exception("Error with Processing"))
            print(e)
            # raise e

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

    # region Get pcaps
    def get_pcaps(self, *args, keep_packets=True, display_filter=None, only_summaries=False,
                  decryption_key=None, encryption_type="wpa-pwk", decode_as=None,
                  disable_protocol=None, tshark_path=None, override_prefs=None,
                  use_json=False, output_file=None, include_raw=False, eventloop=None, custom_parameters=None,
                  debug=False, **kwargs) -> list:
        try:
            _pcapFiles = []
            # print("Trying to generate pcaps")Generating Reports
            # print(self.base_params['isDir'])
            # print(type(self.base_params['isDir']))
            if self.base_params['isDir'] == True:
                # print("Trying to use full dir")
                exts = self.config.config["NIGHTCAPCORE"]["extentions"].split(
                    " ")
                for root, dirs, files in os.walk(self.base_params['dir'], topdown=False):
                    # print("Root ", root)
                    # print("Files", files)
                    for name in files:
                        # print("Parsing filename", name)
                        if str(name).split(".")[1] in exts:
                            _pcapFiles.append(
                                pyshark.FileCapture(
                                    os.path.join(root, name),
                                    display_filter=display_filter,
                                    keep_packets=keep_packets,
                                    only_summaries=only_summaries,
                                    decryption_key=decryption_key,
                                    encryption_type=encryption_type,
                                    decode_as=decode_as,
                                    disable_protocol=disable_protocol,
                                    tshark_path=tshark_path,
                                    override_prefs=override_prefs,
                                    use_json=use_json,
                                    output_file=output_file,
                                    include_raw=include_raw,
                                    eventloop=eventloop,
                                    custom_parameters=custom_parameters,
                                    debug=debug
                                )
                            )
            else:
                # print("Parsing filename", os.path.join(self.base_params['dir'], self.base_params['filename']))
                _pcapFiles.append(
                    pyshark.FileCapture(
                        os.path.join(
                            self.base_params['dir'], self.base_params['filename']),
                        display_filter=display_filter,
                        keep_packets=keep_packets,
                        only_summaries=only_summaries,
                        decryption_key=decryption_key,
                        encryption_type=encryption_type,
                        decode_as=decode_as,
                        disable_protocol=disable_protocol,
                        tshark_path=tshark_path,
                        override_prefs=override_prefs,
                        use_json=use_json,
                        output_file=output_file,
                        include_raw=include_raw,
                        eventloop=eventloop,
                        custom_parameters=custom_parameters,
                        debug=debug
                    )
                )
            return _pcapFiles
        except Exception as e:
            self.printer.print_error(e)
            return []
    # endregion

    # region run
    def run(self) -> None:
        self.onRun()
    # endregion
