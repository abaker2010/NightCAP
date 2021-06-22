# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Imports
import json
import os
from nightcappackages.classes.helpers.package_ncp import NightcapPackageInstallerHelper
from nightcappackages.classes.helpers.package_imports import NightcapPackageImports
from nightcappackages.classes.databases.mogo.mongo_modules import MongoModuleDatabase
from nightcappackages.classes.databases.mogo.mongo_packages import MongoPackagesDatabase
from nightcappackages.classes.helpers.tmp_files import NightcapTmpFileHelper
from nightcappackages.classes.helpers.github_package_ncp import (
    NightcapGithubPackageInstallerHelper,
)
from nightcappackages.classes.databases.mogo.mongo_submodules import (
    MongoSubModuleDatabase,
)
from nightcappackages.classes.paths import (
    NightcapPackagesPaths,
)
from nightcapcore import *
import shutil
import time
from .get_updater import NightcapPackageUpdateDownloaderCommand

# endregion


class NightcapGithubPackageInstallerCommand(Command):

    # region Init
    def __init__(
        self,
        github_link: dict,
        package_path,
        package_paths: NightcapPackagesPaths,
        package,
        clear: bool = False,
        verbose: bool = False,
    ) -> None:

        self.printer = Printer()
        self.github_link = github_link
        self._clearScreen = clear
        self.verbose = verbose
        self.package = package
        self.package_paths = package_paths
        self.package_path = package_path

    # endregion

    # region Execute
    def execute(self) -> None:
        self.printer.print_formatted_additional("Getting Link", self.github_link["url"])
        _tmp = NightcapTmpFileHelper()
        _tmp.create()

        invoker = Invoker()
        invoker.set_on_start(
            NightcapPackageUpdateDownloaderCommand(
                self.github_link["url"], _tmp.tmp_location, "github-package.zip"
            )
        )
        _data = invoker.execute()

        NightcapGithubPackageInstallerHelper(
            _data, self.package_path, self.package
        ).install()
        _tmp.delete()
        return _data
