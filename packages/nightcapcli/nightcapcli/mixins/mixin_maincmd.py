# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Import
from nightcapcore import NightcapCLIConfiguration
from nightcapcli.generator.option_generator import NightcapOptionGenerator
from nightcapcli.observer.publisher import NightcapCLIPublisher
from ..cmds import NightcapMainCMD

# endregion


class NightcapCLICMDMixIn(NightcapMainCMD):
    def __init__(
        self,
        selectedList: list,
        configuration: NightcapCLIConfiguration,
        nextobj: type = object,
        channelid: str = None,
    ):
        NightcapMainCMD.__init__(self, selectedList, configuration, channelid)
        self.pageobjct = nextobj

    def do_options(self, line):
        """\nSee what options are available to use. Use -d on packages to see detailed information\n"""
        if len(line) == 0:
            NightcapOptionGenerator(self.selectedList).options()
        elif line == "-d":
            if len(self.selectedList) != 2:
                self.printer.print_formatted_additional(
                    text="Detailed information can not be provided at this level"
                )
                NightcapOptionGenerator(self.selectedList).options(isDetailed=False)
            else:
                NightcapOptionGenerator(self.selectedList).options(isDetailed=True)
        else:
            print("Error with command")

    def help_use(self):
        print(
            "\nSelect/Use a module/submobule/package: use [module/submobule/package name]\n"
        )

    def complete_use(self, text, line, begidx, endidx):
        return [
            i
            for i in NightcapOptionGenerator(self.selectedList).completed_options()
            if i.startswith(text)
        ]

    def do_use(self, line: str, override: object = None):
        # print("Using ", line)
        try:
            _validator = NightcapCLIPublisher().isValid(line, self.selectedList)
            if _validator:
                # print('Should notify about change', self.channelID)
                # print(NightcapCLIPublisher().channels)

                NightcapCLIPublisher().directions["override"] = override
                NightcapCLIPublisher().dispatch(
                    self.channelID, NightcapCLIPublisher().directions
                )
            else:
                # print("Invalid using line: ", line)
                self.printer.print_error(
                    exception=Exception("Not a valid option. Use [options] for help")
                )

        except Exception as e:
            self.printer.print_error(exception=e)
