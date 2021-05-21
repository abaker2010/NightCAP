# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Imports
import os
import json
from pathlib import Path
import shutil
import tempfile
from datetime import datetime
from bson.objectid import ObjectId
from nightcapcli.base.base_cmd import NightcapBaseCMD
from colorama import Fore, Style
from nightcapcore.invoker.invoker import Invoker
from nightcappackages.classes.databases.mogo.mongo_modules import MongoModuleDatabase
from nightcappackages.classes.databases.mogo.mongo_packages import MongoPackagesDatabase
from nightcappackages.classes.databases.mogo.mongo_projects import MongoProjectsDatabase
from nightcappackages.classes.databases.mogo.mongo_submodules import MongoSubModuleDatabase
from nightcappackages.classes.helpers.package_installer import NightcapPackageInstallerCommand
from nightcappackages.classes.paths.paths import NightcapPackagesPaths
from nightcappackages.classes.paths.pathsenum import NightcapPackagesPathsEnum

# endregion

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


class NightcapBackups(NightcapBaseCMD):
    def __init__(self, selectedList: list, channelid):
        super().__init__(selectedList, channelid=channelid)
        self._package_paths = NightcapPackagesPaths()
        
    # region Backup
    def help_backup(self):
        self.printer.help("Backup your instance of the NightCAP program")
        self.printer.help("useage: backup <output location>")

    def do_backup(self, line):
        if len(line) == 0:
            self.printer.print_error(Exception("Please enter an output location"))
        else:
            self.printer.print_underlined_header("Starting Backup")
            # self.printer.print_formatted_additional("Backup Location:", optionaltext=str(line))

            self.tmpdir = tempfile.mkdtemp()
            self.printer.print_formatted_additional("Tmp Location", optionaltext=self.tmpdir)

            self._backup_installers(self.tmpdir)
            self._backup_databases(self.tmpdir)

            self.printer.print_underlined_header("Moving Backup")
            now = datetime.now()
            #date and time format: dd/mm/YYYY H:M:S
            format = "%d-%m-%Y-%H-%M-%S"
            #format datetime using strftime() 
            time1 = now.strftime(format)
            self._move_backup(self.tmpdir, str(line), "backup_" + str(time1))
            

            self.printer.print_formatted_additional("Backup Complete", endingBreaks=1, leadingTab=1, leadingBreaks=1)
            shutil.rmtree(self.tmpdir)
            
    def _move_backup(self, source, destination, name):
        self._make_archive(source, destination, name, 'zip')
        os.rename(os.path.join(destination, name + ".zip"), os.path.join(destination, name+ ".ncb"))
        self.printer.print_formatted_check("Done", endingBreaks=1)

    def _backup_installers(self, output: str):
        _installer_path = self._package_paths.generate_path(
                NightcapPackagesPathsEnum.Installers
            )

        self.printer.print_underlined_header("Backing Up Installers")  
        self.printer.print_formatted_additional("Installer(s) Location: ", optionaltext=_installer_path)
        self.printer.print_formatted_additional("Backup Location:", optionaltext=output)

        self._make_archive(_installer_path, output, "installers", "zip")
        self.printer.print_formatted_check("Done")


    def _backup_databases(self, output: str):

        self.printer.print_underlined_header("Backing Up Collections")        

        _packages = self._backup_packages()
        self._write_file(output, "packages.json", _packages)
        self.printer.print_formatted_additional("Packages", optionaltext="Backed Up")

        _projects = self._backup_projects()
        self._write_file(output, "projects.json", _projects)
        self.printer.print_formatted_additional("Projects", optionaltext="Backed Up")
        
        _submodules = self._backup_submodules()
        self._write_file(output, "submodules.json", _submodules)
        self.printer.print_formatted_additional("Submodules", optionaltext="Backed Up")

        _modules = self._backup_modules()
        self._write_file(output, "modules.json", _modules)
        self.printer.print_formatted_additional("Modules", optionaltext="Backed Up")

        self.printer.print_formatted_check("Done")

    def _write_file(self, dest, name, data):
        with open(os.path.join(dest, name), "w") as outfile:
                json.dump(JSONEncoder().encode(data), outfile)


    # region make archive(s)
    def _make_archive(self, source, destination, name, format):
        shutil.make_archive(name, format, source)
        shutil.move('%s.%s'%(name,format), destination)
        

    def _backup_modules(self):
        _modules = MongoModuleDatabase().read()
        return list(_modules)

    def _backup_submodules(self):
        _submodules = MongoSubModuleDatabase().read()
        return list(_submodules)

    def _backup_packages(self):
        _packages = MongoPackagesDatabase().read()
        return list(_packages)

    def _backup_projects(self):
        _projects = MongoProjectsDatabase().read()
        return list(_projects)

    # endregion

    #endregion


    #region Restore
    def help_restore(self):
        self.printer.help("Restore your instance of the NightCAP program from a backup")
        self.printer.help("useage: restore <output location>.ncb")

    def do_restore(self, line):
        # print(str(line).split(os.sep)[-1])
        if ".ncb" in str(line).split(os.sep)[-1]:
            
            self.printer.print_underlined_header("Starting Restore", leadingBreaks=1)
            self.printer.print_formatted_additional("Restore File Path", optionaltext=line, endingBreaks=1)

            # _installer_path = self._package_paths.generate_path(
            #     NightcapPackagesPathsEnum.Installers
            # )

            # _packages_path = self._package_paths.generate_path(
            # NightcapPackagesPathsEnum.PackagesBase)

            # self.printer.print_underlined_header("Cleaning")
            # try:
            #     shutil.rmtree(_installer_path)
            #     self.printer.print_formatted_check("Cleaned", optionaltext=("Installers"))
            # except Exception as e:
            #     self.printer.print_formatted_additional("Installers Not Cleaned", optionaltext=str(e))

            # try:
            #     os.makedirs(_installer_path)
            #     self.printer.print_formatted_check("Created", optionaltext=("Installers Location"))
            # except Exception as e:
            #     self.printer.print_formatted_additional("Installers Not Created", optionaltext=str(e))

            # try:
            #     shutil.rmtree(_packages_path)
            #     self.printer.print_formatted_check("Cleaned", optionaltext=("Packages"), leadingBreaks=1)
            # except Exception as e:
            #     self.printer.print_formatted_additional("Installers Not Cleaned", optionaltext=str(e))

            # try:
            #     os.makedirs(_packages_path)
            #     self.printer.print_formatted_check("Created", optionaltext=("Packages Location"))
            # except Exception as e:
            #     self.printer.print_formatted_additional("Installers Not Created", optionaltext=str(e))

            # try:
            #     self._drop_dbs()
            #     self.printer.print_formatted_check("Database", optionaltext=("Successful"))
            # except Exception as e:
            #     self.printer.print_formatted_additional("Dropping DB's", optionaltext=str(e))

            _cleaned = self._clean_all()

            if _cleaned:
                self.printer.print_underlined_header("Unpacking Backup")
                self.tmpdir = tempfile.mkdtemp()

                shutil.copy(str(line), self.tmpdir)
                name = os.path.basename(str(line))
                new_name = name.replace(".ncb", ".zip")
                dir = os.path.dirname(str(line))


                os.rename(os.path.join(self.tmpdir, name), os.path.join(self.tmpdir, new_name))

                shutil.unpack_archive(os.path.join(self.tmpdir, new_name), os.path.join(self.tmpdir, "restoring_backup"), "zip") 
                shutil.unpack_archive(os.path.join(self.tmpdir, "restoring_backup", "installers.zip"), os.path.join(self.tmpdir, "restoring_backup", "installers"), "zip") 
                self.printer.print_formatted_check("Successfully unpacked backup")
                    

                _installers_path = os.path.join(self.tmpdir, "restoring_backup", "installers")
                _r_paths = self._restore_installers_paths(_installers_path)
                for _r in _r_paths:
                    self._restore_installers(_r)
                    print("\t\t" + Fore.LIGHTMAGENTA_EX + "*"*25 + Style.RESET_ALL + "\n")           
            
                self.printer.item_1("Cleaning Up", leadingBreaks=1, endingBreaks=1)
                shutil.rmtree(self.tmpdir)
                self.printer.print_formatted_check("Restore Completed", leadingBreaks=1, endingBreaks=1)
            else:
                self.printer.print_error(Exception("There was an error when cleaning, please view above for more details."))
        else:
            self.printer.print_error(Exception("Please check the backup file. Inforrect file type used"))
        

    def _drop_dbs(self):
        try:
            MongoModuleDatabase().drop() 
        except Exception as e:
            self.printer.print_error(e)

        try:
            MongoSubModuleDatabase().drop()
        except Exception as e:
            self.printer.print_error(e)
            
        try:
            MongoPackagesDatabase().drop()
        except Exception as e:
            self.printer.print_error(e)
        
        try:
            MongoProjectsDatabase().drop()
        except Exception as e:
            self.printer.print_error(e)

    def _restore_installers_paths(self, location: str):
        _installers = []

        for root, dirs, files in os.walk(location):
            for file in files:
                if file.endswith('.ncp'):
                    # print(file)
                    _installers.append({"name" : file.replace(".ncp", ''), "path" : os.path.join(root, file)})
        return _installers

    def _restore_installers(self, installers: str):
        _pack = NightcapPackageInstallerCommand(installers['path'], clear=False)
        _pack.execute()
    #endregion


    def do_clean(self, line):
        _cleaned = self._clean_all()

        if _cleaned:
            self.printer.print_formatted_check("Cleaning was successful", leadingBreaks=1, endingBreaks=1, leadingTab=1)
        else:
            self.printer.print_error(Exception("There was an error when cleaning, please view above for more details."))


    def _clean_all(self):
        self.printer.print_underlined_header("Cleaning")

        _installer_path = self._package_paths.generate_path(
            NightcapPackagesPathsEnum.Installers
        )

        _packages_path = self._package_paths.generate_path(
        NightcapPackagesPathsEnum.PackagesBase)

        _passed = True

        try:
            shutil.rmtree(_installer_path)
            self.printer.print_formatted_check("Cleaned", optionaltext=("Installers"))
        except Exception as e:
            self.printer.print_formatted_additional("Installers Not Cleaned", optionaltext=str(e))
            _passed = False

        try:
            os.makedirs(_installer_path)
            self.printer.print_formatted_check("Created", optionaltext=("Installers Location"))
        except Exception as e:
            self.printer.print_formatted_additional("Installers Not Created", optionaltext=str(e))
            _passed = False

        try:
            shutil.rmtree(_packages_path)
            self.printer.print_formatted_check("Cleaned", optionaltext=("Packages"), leadingBreaks=1)
        except Exception as e:
            self.printer.print_formatted_additional("Installers Not Cleaned", optionaltext=str(e))
            _passed = False

        try:
            os.makedirs(_packages_path)
            self.printer.print_formatted_check("Created", optionaltext=("Packages Location"))
        except Exception as e:
            self.printer.print_formatted_additional("Installers Not Created", optionaltext=str(e))
            _passed = False

        try:
            self._drop_dbs()
            self.printer.print_formatted_check("Database", optionaltext=("Successful"))
        except Exception as e:
            self.printer.print_formatted_additional("Dropping DB's", optionaltext=str(e))
            _passed = False

        return _passed
