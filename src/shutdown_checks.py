# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Imports
from nightcapserver.helpers.docker_configure import NightcapDockerConfigurationHelper
from nightcapcore.strategy.strategy import Strategy
from nightcapcore import Printer, NightcapCLIConfiguration
#endregion


class NightcapShutdownChecks(Strategy):

    def __init__(self) -> None:
        super().__init__()
        self.printer = Printer()
        self.conf = NightcapCLIConfiguration()
        

    def execute(self, *arg, **kwargs):
        try:
            _docker_configer = NightcapDockerConfigurationHelper(self.conf)
            if self.conf.config.getboolean("REPORTINGSERVER", "shutdown_on_exit") == True:
                _docker_configer.django_helper.continer_stop()
                self.printer.print_formatted_check("Shutdown Django Server")

            if self.conf.config.getboolean("MONGOSERVER", "shutdown_on_exit") == True:
                _docker_configer.mongo_helper.continer_stop()
                self.printer.print_formatted_check("Shutdown Mongo Server")

        except Exception as e:
            self.printer.print_error(e)
