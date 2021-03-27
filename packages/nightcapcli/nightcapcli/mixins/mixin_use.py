# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Import
from nightcapcli.cmds.cmd_shared.cmd_validator import NightcapCLIOptionsValidator
from nightcapcore import Printer, configuration, NightcapBanner, ScreenHelper
from nightcapcli.observer.publisher import NightcapCLIPublisher
from ..generator import NightcapOptionGenerator
from colorama import Fore, Style
# endregion

class NightcapCLI_MixIn_Use:
    def __init__(self, selectedList: list, configuration: configuration,
                 pageobjct: object = None, channelid: str =  None):
        self.config = configuration
        self.pageobjct = pageobjct
        self.selected = selectedList
        self.printer = Printer()
        self.channelID = channelid

    def help_use(self):
        print("\nSelect/Use a module/submobule/package: use [module/submobule/package name]\n")

    def do_use(self, line: str, override: object = None):
        # _validator = NightcapCLIOptionsValidator(line, self.selected)
        print("*"*10)
        print("Line", line)
        print(self.selected)
        _validator = NightcapCLIPublisher().isValid(line, self.selected)
        if _validator:
            print("valid option")
            _stagedlist = NightcapCLIPublisher().newSelectedList
            _compared = NightcapCLIPublisher().compare()
            
            
            print("CurrentList: ", '/'.join(self.selected))
            print("StagedList: ", "/".join(_stagedlist))
            print("Compared: ", _compared)
            print("*"*10)
            try:
                if 'remove' not in _compared.keys():

                    _tnewlist = []
                    _tadditional = []
        
                    if _compared['add'] == 1:
                        print("Trying to add 1")
                        _tnewlist = _stagedlist
                    elif _compared['add'] == 2:
                        print("Trying to add 2")
                        _tnewlist = [str(_stagedlist[0])]
                        _tadditional = _stagedlist[1::]
                    elif _compared['add'] == 3:
                        print("Trying to add 3")
                        _tnewlist = [str(_stagedlist[0])]
                        _tadditional = _stagedlist[1::]

                    print("new list:", _tnewlist)
                    print("additional list:", _tadditional)
                    NightcapCLIPublisher().set_list(_tnewlist)


                    _channel = NightcapCLIPublisher().new_channel()
                    _who = None
                    if len(_tnewlist) == 3:
                        _who = override(_tnewlist, self.config, NightcapCLIPublisher().get_package_config(_tnewlist), _channel)
                    else:
                        _who = self.pageobjct(_tnewlist, self.config, _channel, self.channelID, _tadditional)
                    NightcapCLIPublisher().register(_channel, _who)

                    # print(NightcapCLIPublisher().channels)
                    # NightcapCLIPublisher().set_list(NightcapCLIPublisher().newSelectedList)
                    # print(_newlist)
                    print("*"*15)
                    _who.cmdloop()
                else:
                    print("Items need to be removed first")
            except Exception as e:
                ScreenHelper().clearScr()
                NightcapBanner(self.config).Banner()
                print("\n", Fore.RED, e, Style.RESET_ALL, "\n")
                print(e)#Exception("Not a valid option. Use [options] for help"))
            # try:
            #     print("Valid command to use")
            #     print("Path", _validator.newSelectedList)
            #     print("Register new console page")
            #     _channel = NightcapCLIPublisher().new_channel()
            #     print("channel created:", _channel)
            #     ScreenHelper().clearScr()
            #     NightcapCLIPublisher().set_list(_validator.newSelectedList)
            #     _who = None
            #     if len(_validator.newSelectedList) == 3:
            #         _who = override(NightcapCLIPublisher().selectedList, self.config, _validator.get_package_config(_validator.newSelectedList), _channel)
            #     else:
            #         _who = self.pageobjct(NightcapCLIPublisher().selectedList, self.config, _channel, self.channelID)
            #     NightcapCLIPublisher().register(_channel, _who)
            #     print(NightcapCLIPublisher().channels)
            #     print(_validator.newSelectedList)
            #     _who.cmdloop()
                
            # except Exception as e:
            #     ScreenHelper().clearScr()
            #     NightcapBanner(self.config).Banner()
            #     print("\n", Fore.RED, e, Style.RESET_ALL, "\n")
        else:
            self.printer.print_error(exception=Exception("Not a valid option. Use [options] for help"))

    def do_options(self, line):
        '''\nSee what options are available to use. Use -d on packages to see detailed information\n'''
        if(len(line) == 0):
            NightcapOptionGenerator(self.selected).options()
        elif(line == "-d"):
            if(len(self.selected) != 2):
                self.printer.print_formatted_additional(text="Detailed information can not be provided at this level")
                NightcapOptionGenerator(self.selected).options(isDetailed=False)
            else:
                NightcapOptionGenerator(self.selected).options(isDetailed=True)
        else:
            print("Error with command")

    def do_exit(self, line):
        try:
            print("using overriden exit in use")
            print(NightcapCLIPublisher().channels)
            NightcapCLIPublisher().del_channel(self.channelID)
            try:
                NightcapCLIPublisher().selectedList.pop()
                print(NightcapCLIPublisher().selectedList)
            except IndexError as e:
                print("List is empty in the publisher")
            
            return True
        except Exception as e:
            self.printer.print_error(exception=e)
