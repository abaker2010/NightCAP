# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
#region Imports
from nightcapcore.configuration.configuration import NighcapCoreConfiguration
from application.classes.options.cli_options_package import NightcapCLIOptionsPackage
from application.classes.options.mixin.mixin_use import NightcapCLIOption_MixIn_Use
from application.classes.options.mixin.mixin_usecmd import NightcapCLIUseCMDMixIn
from application.classes.options.cli_options_validator import NightcapCLIOptionsValidator
from nightcapcore import NightcapCoreBase
#endregion

class NightcapCLIOptionsSelector(NightcapCLIUseCMDMixIn):
    def __init__(self, selectedList: list, configuration: NighcapCoreConfiguration, packagebase: NightcapCoreBase = NightcapCoreBase()):
        # print("Working with List", selectedList, " : ", len(selectedList))
        # the reason that it's not working 100% right is do to this line, with the selectedList
        NightcapCLIUseCMDMixIn.__init__(self, selectedList, configuration,packagebase,NightcapCLIOptionsSelector)

    def do_use(self, line):
        NightcapCLIOption_MixIn_Use.do_use(self, line, override=NightcapCLIOptionsPackage)
        

    
            
    