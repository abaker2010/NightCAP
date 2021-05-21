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
        self.make_archive(source, destination, name, 'zip')
        os.rename(os.path.join(destination, name + ".zip"), os.path.join(destination, name+ ".ncb"))
        self.printer.print_formatted_check("Done", endingBreaks=1)

    def _backup_installers(self, output: str):
        _installer_path = self._package_paths.generate_path(
                NightcapPackagesPathsEnum.Installers
            )

        self.printer.print_underlined_header("Backing Up Installers")  
        self.printer.print_formatted_additional("Installer(s) Location: ", optionaltext=_installer_path)
        self.printer.print_formatted_additional("Backup Location:", optionaltext=output)

        self.make_archive(_installer_path, output, "installers", "zip")
        self.printer.print_formatted_check("Done")


    def _backup_databases(self, output: str):

        self.printer.print_underlined_header("Backing Up Collections")        

        _packages = self.backup_packages()
        self._write_file(output, "packages.json", _packages)
        self.printer.print_formatted_additional("Packages", optionaltext="Backed Up")

        _projects = self.backup_projects()
        self._write_file(output, "projects.json", _projects)
        self.printer.print_formatted_additional("Projects", optionaltext="Backed Up")
        
        _submodules = self.backup_submodules()
        self._write_file(output, "submodules.json", _submodules)
        self.printer.print_formatted_additional("Submodules", optionaltext="Backed Up")

        _modules = self.backup_modules()
        self._write_file(output, "modules.json", _modules)
        self.printer.print_formatted_additional("Modules", optionaltext="Backed Up")

        self.printer.print_formatted_check("Done")

        
        

    def _write_file(self, dest, name, data):
        with open(os.path.join(dest, name), "w") as outfile:
                json.dump(JSONEncoder().encode(data), outfile)


    # region make archive(s)
    def make_archive(self, source, destination, name, format):
        shutil.make_archive(name, format, source)
        shutil.move('%s.%s'%(name,format), destination)
        

    def backup_modules(self):
        _modules = MongoModuleDatabase().read()
        return list(_modules)

    def backup_submodules(self):
        _submodules = MongoSubModuleDatabase().read()
        return list(_submodules)

    def backup_packages(self):
        _packages = MongoPackagesDatabase().read()
        return list(_packages)

    def backup_projects(self):
        _projects = MongoProjectsDatabase().read()
        return list(_projects)

    # endregion

    #endregion


    #region Restore
    def help_restore(self):
        self.printer.help("Restore your instance of the NightCAP program from a backup")
        self.printer.help("useage: restore <output location>.ncb")

    def do_restore(self, line):
        print(str(line).split(os.sep)[-1])
        if ".ncb" in str(line).split(os.sep)[-1]:
            self.printer.print_underlined_header("Starting Restore")
            self.printer.print_formatted_additional("Restore File Path", optionaltext=line, endingBreaks=1)

            self.tmpdir = tempfile.mkdtemp()
            shutil.copy(str(line), self.tmpdir)
            # print(self.tmpdir)

            name = os.path.basename(str(line))
            new_name = name.replace(".ncb", ".zip")
            dir = os.path.dirname(str(line))
            # print("Name : " + name)
            # print("Dir : " + dir)

            os.rename(os.path.join(self.tmpdir, name), os.path.join(self.tmpdir, new_name))

            shutil.unpack_archive(os.path.join(self.tmpdir, new_name), os.path.join(self.tmpdir, "restoring_backup"), "zip") 
            shutil.unpack_archive(os.path.join(self.tmpdir, "restoring_backup", "installers.zip"), os.path.join(self.tmpdir, "restoring_backup", "installers"), "zip") 

            _installers_path = os.path.join(self.tmpdir, "restoring_backup", "installers")
            _r_paths = self.restore_installers_paths(_installers_path)
            for _r in _r_paths:
                self.restore_installers(_r)
            # _dbs_path = os.path.join(self.tmpdir, "restoring_backup")

            shutil.rmtree(self.tmpdir)
            self.printer.print_formatted_check("Restore Complete", leadingTab=1, endingBreaks=1, leadingBreaks=1)
        else:
            self.printer.print_error(Exception("Please check the backup file. Inforrect file type used"))
        

    def restore_installers_paths(self, location: str):
        _installers = []

        for root, dirs, files in os.walk(location):
            for file in files:
                if file.endswith('.ncp'):
                    print(file)
                    _installers.append({"name" : file.replace(".ncp", ''), "path" : os.path.join(root, file)})
        return _installers

    def restore_installers(self, installers: str):
        # for _ in installers:
        # print("Installing: " + installers['name'])
        # print("Installing: " + installers['path'])
        _pack = NightcapPackageInstallerCommand(installers['path'], clear=False)
        _pack.execute()
        # for installer in _installers:
        #     self.printer.print_formatted_additional("Installing", installer['name'])
        # try:
        #     invoker = Invoker()
        #     invoker.set_on_start(NightcapPackageInstallerCommand(installers['path'], clear=False))
        #     invoker.execute()
        # except Exception as e:
        #     self.printer.print_error(e)

        

    def resotre_dbs(self, location: str):
        _module_backup = os.path.join(location, "modules.json")
        _submodule_backup = os.path.join(location, "submodules.json")
        _packages_backup = os.path.join(location, "packages.json")
        _projects_backup = os.path.join(location, "projects.json")


    #endregion