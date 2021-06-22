# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Imports
import os
import shutil
import subprocess
import errno
import sys
from nightcapcore.printers.print import Printer
from nightcappackages.classes.paths import (
    NightcapPackagesPathsEnum,
    NightcapPackagesPaths,
)

# endregion


class NightcapGithubPackageInstallerHelper(object):
    def __init__(self, data: tuple, package_path, package: dict) -> None:
        super().__init__()
        self.data = data
        self.package_path = package_path
        self.paths = NightcapPackagesPaths()
        self.package = package
        self.printer = Printer()

        self.installers_backup_loation = self.paths.generate_path(
            NightcapPackagesPathsEnum.Installers
        )
        self.package_install_location = self.paths.generate_path(
            NightcapPackagesPathsEnum.PackagesBase,
            [
                self.package["package_for"]["module"],
                self.package["package_for"]["submodule"],
                self.package["package_information"]["package_name"],
            ],
        )

    def install(self):
        # print("installing github package")
        # print(self.data)
        # print("NCP Location: ", self.package_path)
        # print("Installer(s) Backup Location: ", self.installers_backup_loation)
        # print("Install To: ", self.package_install_location)

        self._unpack()
        self._backup_installer()
        self._move_repo()
        self._requirements_install()

    def _unpack(self):
        try:
            shutil.unpack_archive(
                os.path.join(self.data[1], self.data[2]), self.data[1], "zip"
            )
        except Exception as e:
            self.printer.print_error(e)

    # region Backup Installer
    def _backup_installer(self):
        # self.printer.print_underlined_header("Backing up installer")
        try:
            if os.path.exists(
                os.path.join(self.installers_backup_loation, self.data[2])
            ):
                os.remove(os.path.join(self.installers_backup_loation, self.data[2]))

            shutil.copy(self.package_path, self.installers_backup_loation)
        except OSError as e:
            # If the error was caused because the source wasn't a directory
            self.printer.print_formatted_delete(
                text="Package not copied (.ncp) Error: %s" % str(e)
            )

    # endregion

    # region Install Repo
    def _move_repo(self):
        # self.printer.print_underlined_header("Installing Repo")

        try:

            _repo_fullpath = str(
                [
                    i
                    for i in map(
                        lambda name: os.path.join(self.data[1], name),
                        os.listdir(self.data[1]),
                    )
                    if ".zip" not in i and os.path.isdir(i)
                ][0]
            )

            # print(_repo_fullpath)

            shutil.move(_repo_fullpath, self.package_install_location)
        except OSError as e:
            # If the error was caused because the source wasn't a directory
            if e.errno == errno.ENOTDIR:
                shutil.move(_repo_fullpath, self.package_install_location)
            else:
                self.printer.print_formatted_delete(
                    text="Package not copied. (Installer Files) Error: %s" % str(e)
                )

    # endregion
    def _requirements_install(self):
        # self.printer.print_underlined_header("Installing Requirements")

        print()

        if (
            "python-requirements"
            in self.package["package_information"]["github"].keys()
        ):
            _requirements = []
            for k, _path in self.package["package_information"]["github"][
                "python-requirements"
            ].items():
                print(k)
                print(_path)
                _requirements.append(
                    os.path.join(self.package_install_location, os.sep.join(_path))
                )

        else:
            _requirements = [
                str(i)
                for i in map(
                    lambda name: os.path.join(self.package_install_location, name),
                    os.listdir(self.package_install_location),
                )
                if "requirements.txt" == str(i).split(os.sep)[-1]
            ]

        for _r in _requirements:
            with open(_r, "r") as rfile:
                _reqs = rfile.readlines()

                _reqs = [i for i in _reqs if str(i).strip() != ""]

                if _reqs != []:
                    for _req in _reqs:
                        # print("Try to get requirement: ", _req)
                        subprocess.check_call(
                            [
                                sys.executable,
                                "-m",
                                "pip",
                                "install",
                                _req,
                                "--force-reinstall",
                            ],
                            stdout=subprocess.DEVNULL,
                        )

    # region Install Git Repo Requirements

    # endregion
