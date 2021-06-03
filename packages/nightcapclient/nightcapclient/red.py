# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Imports
import argparse
import abc
from nightcappackages.classes.helpers.encoder import NightcapJSONEncoder
import time
from nightcapcli.base.base_cmd import NightcapBaseCMD
from nightcapcore.printers.print import Printer
# endregion

class NightcapRedTeam(NightcapBaseCMD):
    """

    This class is used to allows the Nightcap program to interact with the installed custom programs

    ...

    Attributes
    ----------
        ** Not including those inherited from NightcapBaseCMD for now

    Methods
    -------
        Accessible
        -------
            onClose(self): -> NotImplementedError
                After the package is ran

            onIntro(self): -> NotImplementedError
                Intro before the client package is executed

            onConsolePrint(self): -> NotImplementedError
                Console Printing will happen after the Processing has been done

            onProcess(self): -> NotImplementedError
                This is the code that the user is running in the package

            onReport(self): -> NotImplementedError
                This will be the way that the user generates reports

            onRun(self): -> None
                This will try and run the package

            run(self): -> None
                Allows the user to have the clean Object.run() syntax

    """
    #region Init
    def __init__(self, intro: str = None, *args, debug=False, **kwargs) -> None:

        parser = argparse.ArgumentParser(description="Process some pcaps.")
        parser.add_argument("--data", required=True,
                            help="list of pcap filenames")
        args = parser.parse_args()
        self.printer = Printer()
  
        try:

            _data = NightcapJSONEncoder().default(args.data)

            self.base_params = _data["0"]
            self.package_params = _data["1"]
            NightcapBaseCMD.__init__(
                    self, _data["2"], passedJson=_data["0"]
                )
            self.printer.debug("Args after passing", args,
                           currentMode=self.config.verbosity)

        except Exception as e:
            self.printer.print_error(e)
    #endregion 

    # region onClose
    def onClose(self) -> None:
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
            if self.config.project != None or self.package_params != [] or self.package_params != None:
                self.printer.print_underlined_header("Scan Details: (Params Used)")

            if self.config.project != None:
                self.printer.print_underlined_header("Project", leadingTab=2)
                self.printer.item_1("ID", optionalText=self.base_params['project']['_id']['$oid'], seperator=" : ", leadingTab=3)
                self.printer.item_1("Name", optionalText=self.base_params['project']['project_name'], seperator=" : ", leadingTab=3)
                
            if self.package_params != [] or self.package_params != None:
                self.printer.print_underlined_header("Package Params", leadingTab=2)
                for k, v in dict(self.package_params).items():
                    self.printer.item_1(str(k), optionalText=str(v), seperator=" : ", leadingTab=3)
        except Exception as e:
            self.printer.print_error(e)
        pass
    # endregion

    # region onProcess
    @abc.abstractmethod
    def onProcess(self):
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
            self.onProcess()
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

    # region run
    def run(self):
        self.onRun()
    # endregion
