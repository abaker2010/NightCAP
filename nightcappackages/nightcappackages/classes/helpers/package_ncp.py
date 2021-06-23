# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Imports
import os
import shutil
import errno
from nightcapcore.printers.print import Printer
from nightcappackages.classes.paths import (
    NightcapPackagesPathsEnum,
    NightcapPackagesPaths,
)

# endregion


class NightcapPackageInstallerHelper(object):
    def __init__(
        self,
        base_path: str,
        package_path,
        package_paths: NightcapPackagesPaths,
        package,
    ) -> None:
        super().__init__()

        self._package = package
        self._base_path = base_path
        self._package_paths = package_paths
        self._package_path = package_path
        self.printer = Printer()

    def copy_installer(self):
        self._copy(self._package, self._base_path)
        self._copy_installer(self._package_path)

    # region Copy
    def _copy_installer(self, installer: str):
        _path = self._package_paths.generate_path(NightcapPackagesPathsEnum.Installers)

        _name = os.path.basename(installer)

        try:
            if os.path.exists(os.path.join(_path, _name)):
                os.remove(os.path.join(_path, _name))

            shutil.copy(installer, _path)
        except OSError as e:
            # If the error was caused because the source wasn't a directory
            self.printer.print_formatted_delete(
                text="Package not copied (.ncp) Error: %s" % str(e)
            )

    # endregion

    # region Copy
    def _copy(self, pkt: dict, src: str):
        _path = self._package_paths.generate_path(
            NightcapPackagesPathsEnum.PackagesBase,
            [
                pkt["package_for"]["module"],
                pkt["package_for"]["submodule"],
                pkt["package_information"]["package_name"],
            ],
        )
        try:
            shutil.move(src, _path)
        except OSError as e:
            # If the error was caused because the source wasn't a directory
            if e.errno == errno.ENOTDIR:
                shutil.move(src, _path)
            else:
                self.printer.print_formatted_delete(
                    text="Package not copied. (Installer Files) Error: %s" % str(e)
                )

    # endregion
