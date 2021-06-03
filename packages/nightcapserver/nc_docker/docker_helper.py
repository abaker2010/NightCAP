# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Imports
from pathlib import Path
import subprocess
from subprocess import Popen, PIPE, STDOUT
import time
import os
import re
import getpass
import docker as dDocker
from colorama.ansi import Fore
from nightcapcore.configuration import NightcapCLIConfiguration
from nightcapcore.docker.docker_checker import NightcapCoreDockerChecker
from nightcapcore.helpers.screen.screen_helper import ScreenHelper
from nightcapcore.printers.print import Printer
from nightcappackages.classes.paths import NightcapPackagesPathsEnum, NightcapPackagesPaths
from nightcappackages.classes.helpers import NightcapRestoreHelper

DEVNULL = open(os.devnull, "wb")
# endregion


class NightcapDockerHelper(object):
    """

    This class is used as the main Docker helper

    ...

    Attributes
    ----------
        printer: -> Printer
            allows us to print from the command line

        conf: -> NightcapCLIConfiguration
            allows us to have access to the main configuration

        yes: -> list
            list of yes 'words'

        docker_helper: -> NightcapDockerHelper
            allows us to talk to the Docker containers

        mongo_server: -> MongoDatabaseChecker
            allows us to check the status of the Docker Container

    Methods
    -------
        Accessible
        -------
            prepare_containers(self): -> bool
                prepares the Docker containers

            restart_containers(self): -> None
                restart the containers

            init_containers(self, agreement: str, dc: NightcapCoreDockerChecker): -> bool
                initilize the containers

            init_nc_site(self, dc: NightcapCoreDockerChecker): -> None
                init for Nightcap Site

            stop_all_containers(self): -> bool
                stops all containers

            stop_nightcapsite(self): -> None
                stop the nc site container

            stop_mongodb(self): -> None
                stop the mongodb container

            stop_container_by_name(self, name: str): -> None
                stops a container by its name

            start_all_containers(self): -> None
                start all containers

            start_mongodb(self): -> None
                start monogdb container

            start_nighcap_site(self): -> None
                start nightcap site conatiner

            start_container_by_name(self, name: str): -> bool
                start container by name

            get_mongo_container_status(self): -> str
                gets status of mongodb container

            get_site_container_status(self): -> str
                gets the status of the nightcap site conatiner

            mongo_continer_exists(self): -> bool
                checks to see if the mongo container exists

            site_container_exists(self): -> bool
                checks to see if the nightcap site container exists

            container_exists(self, name: str): -> bool
                checks to see if any container exists

            get_container_status_by_name(self, name: str): -> str
                gets the container status by the name of the container

            build_containers(self): -> None
                builds the needed containers

            make_docker(self): -> None
                makes the nightcap site docker

            init_mongo(self, dc: NightcapCoreDockerChecker): -> bool
                init for the mongo database
    """

    # region Init
    def __init__(self, config: NightcapCLIConfiguration) -> None:
        super().__init__()
        self.conf = config
        self.yes = self.conf.config.get("NIGHTCAPCORE", "yes").split()
        self.printer = Printer()
        self.docker = dDocker.from_env()

    # endregion

    # region Prepare Containers
    def prepare_containers(self):
        try:
            self.start_container_by_name("nightcapmongodb")
            time.sleep(3)
            # MongoDatabaseChecker().initialize_database()
            return True
        except Exception as e:
            raise e

    # endregion

    # region Restart Containers
    def restart_containers(self):
        self.stop_all_containers()
        self.start_all_containers()

    # endregion

    # region Init Containers
    def init_containers(self, dc: NightcapCoreDockerChecker):
        try:
            self.printer.print_underlined_header("Initializing")
            self.init_mongo(dc)
            self.init_nc_site(dc)


            self.printer.print_underlined_header("Building Containers")
            self.build_containers()
            
            self.printer.print_underlined_header("Preparing Containers")
            self.prepare_containers()

            self.printer.print_underlined_header("Installing Packages...")
            self.restore_packages()
            self.set_account()
            return True
        except Exception as e:
            raise e

    # endregion

    def restore_packages(self):
        
        _path = NightcapPackagesPaths().generate_path(
            NightcapPackagesPathsEnum.NCInitRestore
        )
        _bc_path = os.path.join(_path, "restore_point.ncb")
        NightcapRestoreHelper(str(_bc_path)).restore()


    # region NC Site Init
    def init_nc_site(self, dc: NightcapCoreDockerChecker):
        if dc.ncs_exits == False:
            self.printer.item_1("Please wait while pulling Image", "nightcapsite:latest")

            p = subprocess.Popen(["make", "-C", Path(__file__).resolve().parent.parent], stdout=DEVNULL, stderr=DEVNULL)

            while p.poll() is None:
                print("", end="", flush=True)
                time.sleep(1)


            if p.returncode != 0:
                self.printer.print_error(Exception("Error pulling docker image: %s" % (p.returncode)))
    # endregion

    # region Stop all containers
    def stop_all_containers(self):
        self.printer.print_underlined_header_undecorated("Stopping Docker Containers")
        self.stop_mongodb()
        self.stop_nightcapsite()
        print("")
        return True
    # endregion

    # region Stop Nightcap Site
    def stop_nightcapsite(self):
        self.stop_container_by_name("nightcapsite")
    # endregion

    # region Stop MongoDB Container
    def stop_mongodb(self):
        self.stop_container_by_name("nightcapmongodb")
    # endregion

    # region Stop Container By Name
    def stop_container_by_name(self, name: str):
        try:
            self.printer.print_formatted_additional("Stopping...", name)        
            _container = self.docker.containers.get(name)
            _container.stop()
            self.printer.print_formatted_check("Stopped", leadingTab=3)
        except Exception as e:
            raise e

    # endregion

    # region start All Containers
    def start_all_containers(self):
        self.start_mongodb()
        print()
        self.start_nighcap_site()

    # endregion

    # region Start MongoDB
    def start_mongodb(self):
        self.start_container_by_name("nightcapmongodb")

    # endregion

    # region Start NC Container
    def start_nighcap_site(self):
        self.start_container_by_name("nightcapsite")

    # endregion

    # region Start Container By Name
    def start_container_by_name(self, name: str):
        try:
            for _container in self.docker.containers.list(all=True):
                if _container.name == name:
                    self.printer.print_formatted_additional(
                        "Starting...", _container.name
                    )
                    _container.start()
                    self.printer.print_formatted_check("Container Started", name)
                    return True

            return False
        except Exception as e:
            raise e

    # endregion

    # region Get Mongo Container Status
    def get_mongo_container_status(self):
        return self.get_container_status_by_name("nightcapmongodb")
    # endregion

    # region Get Nightcap Site Container Status
    def get_site_container_status(self):
        return self.get_container_status_by_name("nightcapsite")
    # endregion

    # region Mongo Container Exists
    def mongo_continer_exists(self):
        return self.container_exists("nightcapmongodb")
    # endregion

    # region Nightcap Site Contatiner Exists
    def site_container_exists(self):
        return self.container_exists("nightcapsite")
    # endregion

    # region Container Exists
    def container_exists(self, name: str):
        try:

            for _container in self.docker.containers.list(all=True):
                if _container.name == name:
                    return True
            return False
        except Exception as e:
            raise e

    # endregion

    # region Get Container Status By Name
    def get_container_status_by_name(self, name: str):
        try:
            for _container in self.docker.containers.list(all=True):
                if _container.name == name:
                    return _container.attrs["State"]["Status"]
            return _container.attrs["State"]["Status"]
        except Exception as e:
            return "Missing"

    # endregion

    # region Build Containers
    def build_containers(self):
        try:
            self.printer.item_1(text="Creating Docker Containers")
            _ = os.path.join(
                Path(__file__).resolve().parent.parent, "docker-compose.yml"
            )
            p = subprocess.Popen(["docker-compose", "-f", _, "up", "--no-start"], stdout=DEVNULL, stderr=DEVNULL)
            while p.poll() is None:
                print("", end="", flush=True)
                time.sleep(1)
            self.printer.print_formatted_check(text="Created Containers")
        except Exception as e:
            raise e

    # endregion

    #region set admin
    def set_account(self):
        try:
            self.printer.print_underlined_header(text="Creating account")
            self.start_all_containers()
            self.printer.print_underlined_header(text="Account data", leadingBreaks=1)

            try:              
                _container = self.docker.containers.get("nightcapsite")
                
                _container.exec_run("python3 manage.py makemigrations")
                self.printer.print_formatted_check("Making Migrations")

                _container.exec_run("python3 manage.py migrate")
                self.printer.print_underlined_header("Django Admin Account")
                self.printer.item_3("Please enter some information to create your web admin account", leadingTab=2, endingBreaks=1)
                self._set_user(_container)
                
            except Exception as e:
                self.printer.print_error(e)
                raise e

        except Exception as e:
            self.printer.print_error(e)
            raise e
    #endregion

    def _set_user(self, _container):
        _username = input(Fore.LIGHTGREEN_EX + str("\tUser Name: %s" % (Fore.LIGHTCYAN_EX)))
        _email = input(Fore.LIGHTGREEN_EX + str("\tEmail Address: %s" % (Fore.LIGHTCYAN_EX))) 
        
        if self._email_validation(_email):

            _password = getpass.getpass(Fore.LIGHTGREEN_EX + str("\tPassword:")) 
            _retype_password = getpass.getpass(Fore.LIGHTGREEN_EX + str("\tRetype Password:")) 
            if _password == _retype_password:
                _cmd = "".join(["python3 manage.py shell -c \"", ("from django.contrib.auth.models import User; User.objects.create_superuser('%s', '%s', '%s')" % (_username, _email, _password)),"\""])
                _container.exec_run(_cmd)
                self.printer.print_formatted_check(text="Account Created", leadingBreaks=1)
                return True
            else:
                self.printer.print_error(Exception('Passwords didn\'t match'))
                self._set_user(_container)
        else:
            ScreenHelper().clearScr()
            self.printer.print_error(Exception('Please enter a valid email address'))
            self._set_user(_container)

    def _wait_while_processing(self, process: Popen):
        while process.poll() is None:
            print("", end="", flush=True)
            time.sleep(1)

        if process.returncode != 0:
            self.printer.print_error(Exception("Error pulling docker image: %s" % (process.returncode)))
        return process

    def _email_validation(self, email: str):
        regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
        if(re.search(regex, email)):
            return True
        else:
            return False

    # region Init Mongo
    def init_mongo(self, dc: NightcapCoreDockerChecker):
        if dc.mongo_im_exists == False:
            try:
                self.printer.item_1("Please wait while pulling Image", "mongo:latest")
                self.docker.images.pull("mongo:latest")
                return True
            except Exception as e:
                self.printer.print_formatted_delete(
                    text="Error with installing docker mongo image"
                )
                raise e
    # endregion
