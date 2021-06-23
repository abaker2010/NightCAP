# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Imports
from nightcapserver.helpers.docker_rescue_config import NightcapDockRescueConfigHelper
from docker.errors import DockerException
from nightcapserver.helpers.docker_configure import NightcapDockerConfigurationHelper
from nightcapserver.helpers.docker_status import NightcapDockerStatus
from nightcapcore.strategy.strategy import Strategy
from nightcapcore import ScreenHelper, Printer, NightcapCLIConfiguration, NightcapBanner

# endregion


class NightcapBootChecks(Strategy):
    """

    This class is used to as a wrapper for the entry process to the program

    ...

    Attributes
    ----------

        conf: -> NightcapCLIConfiguration
            this allows us to use the main configuration of the program

        printer: -> Printer
            allows us to print to the command line


        mongo_server = None


    Methods
    -------
        Accessible
        -------
            agreements(self): -> bool
                asks the user to agree to the terms of usage and conduct

            banner(self): -> None
                easier to access banner

    """

    def __init__(self) -> None:
        super().__init__()

    def execute(self, *arg, **kwargs) -> bool:
        _printer = Printer()
        _conf = NightcapCLIConfiguration()

        try:
            _docker_configer = NightcapDockerConfigurationHelper(_conf)
            _banner = NightcapBanner()

            if _docker_configer.check_legal():
                _docker_configer = NightcapDockerConfigurationHelper(_conf)
                # print(_docker_configer.env_check())
                # if _docker_configer.env_check() != (
                #     (NightcapDockerStatus.EXISTS, NightcapDockerStatus.EXISTS),
                #     (NightcapDockerStatus.EXISTS, NightcapDockerStatus.EXISTS),
                # ):

                if _docker_configer.mongo_helper.container_status() == NightcapDockerStatus.RUNNING and _docker_configer.mongo_helper.image_exists() == NightcapDockerStatus.EXISTS:
                    return True
                else:    
                    ScreenHelper().clearScr()
                    _banner.Banner()
                    _ready = _docker_configer.change_configuration()
                    if _ready:
                        return True


        except DockerException as de:
            _printer.print_error(
                Exception("Error connecting to Docker Container(s) Please Reconfigure.")
            )
            _now = _printer.input(
                "Would you like to reconfigure now? (Y/n)", defaultReturn=True
            )
            if _now:
                NightcapDockRescueConfigHelper(_conf).change_connection_only()
                self.execute()
            else:
                return False
