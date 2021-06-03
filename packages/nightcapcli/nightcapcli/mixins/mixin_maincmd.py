# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Import
from nightcapcli.generator.option_generator import NightcapOptionGenerator
from nightcapcli.observer.publisher import NightcapCLIPublisher
from ..cmds import NightcapMainCMD

# endregion


class NightcapCLICMDMixIn(NightcapMainCMD):
    """
    (MixIn, User CLI Object)

    This class is used for the options, use commands for the application/nightcap.py

    ...

    Attributes
    ----------
        pageobjct: -> Object
            Used for casting when dynamically creating the next page

    Methods
    -------
        Accessible
        -------
            do_options(self, line): -> None
                Allows the user to see what options are available to be used

            help_use(self): -> None
                Overrides the use help command

            complete_use(self, text, line, begidx, endidx): -> list
                Tab auto complete for the use command

            do_use(self, line: str, override: object = None): -> None
                Allows the user to select an option to use and enter a new cmd
    """

    # region Init
    def __init__(
        self,
        selectedList: list,
        nextobj: type = object,
        channelid: str = None,
    ) -> None:
        NightcapMainCMD.__init__(self, selectedList, channelid)
        self.pageobjct = nextobj

    # endregion

    # region Do Options
    def do_options(self, line) -> None:
        """\nSee what options are available to use. Use -d on packages to see detailed information\n"""
        if len(line) == 0:
            NightcapOptionGenerator(self.selectedList).options()
        elif line == "-d":
            if len(self.selectedList) != 2:
                # self.printer.print_formatted_additional(
                #     text="Detailed information can not be provided at this level"
                # )
                if len(self.selectedList) == 0:
                    self.printer.print_header_w_option("Module Name", "(Submodule Count)")
                elif len(self.selectedList) == 1:    
                    self.printer.print_header_w_option("Submodule Name", "(Submodule Count)")
                NightcapOptionGenerator(self.selectedList).options(isDetailed=False)
            else:
                NightcapOptionGenerator(self.selectedList).options(isDetailed=True)
        else:
            print("Error with command")

    # endregion

    # region Help Use
    def help_use(self) -> None:
        print(
            "\nSelect/Use a module/submobule/package: use [module/submobule/package name]\n"
        )

    # endregion

    # region Complete Use
    def complete_use(self, text, line, begidx, endidx) -> list:
        return [
            i
            for i in NightcapOptionGenerator(self.selectedList).completed_options()
            if i.startswith(text)
        ]

    # endregion

    # region Do Use
    def do_use(self, line: str, override: object = None) -> None:
        try:
            _validator = NightcapCLIPublisher().isValid(line, self.selectedList)
            if _validator:
                NightcapCLIPublisher().directions["override"] = override
                NightcapCLIPublisher().dispatch(
                    self.channelID, NightcapCLIPublisher().directions
                )
            else:
                self.printer.print_error(
                    Exception("Not a valid option. Use [options] for help")
                )

        except Exception as e:
            self.printer.print_error(e)
    # endregion
