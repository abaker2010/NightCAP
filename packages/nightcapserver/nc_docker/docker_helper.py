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
import sys
import re
import getpass
import docker as dDocker
from docker import APIClient
from colorama.ansi import Fore, Style
from nightcapcore.configuration import NightcapCLIConfiguration
from nightcapcore.docker.docker_checker import NightcapCoreDockerChecker
from nightcapcore.helpers.screen.screen_helper import ScreenHelper
from nightcapcore.printers.print import Printer
from nightcappackages.classes.databases.mogo.checker.mongo_database_checker import (
    MongoDatabaseChecker,
)
from requests.exceptions import RetryError

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
            self.init_mongo(dc)
            # self.init_nc_site(dc)
            self.build_containers()
            self.prepare_containers()
            # self.set_account()
            return True
        except Exception as e:
            raise e

    # endregion

    # region NC Site Init
    def init_nc_site(self, dc: NightcapCoreDockerChecker):
        if dc.ncs_exits == False:
            self.printer.print_underlined_header(
                "Initializing: (NC Site)", endingBreaks=1
            )
            self.make_docker()
    # endregion

    # region Stop all containers
    def stop_all_containers(self):
        self.printer.print_underlined_header_undecorated("Stopping Docker Containers")
        self.stop_mongodb()
        # self.stop_nightcapsite()
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
            # for _container in self.docker.containers.list(all=True):
            #     if _container.name == name:
            self.printer.print_formatted_additional("Stopping...", name)
            # client = APIClient(base_url='unix://var/run/docker.sock')
            # client.stop(_container.name)
            p = subprocess.Popen(["docker", "stop", name], stdout=DEVNULL)
            while p.poll() is None:
                print("", end="", flush=True)
                time.sleep(1)
            self.printer.print_formatted_check("Stopped", leadingTab=3)
            # return True

            # return False
            # while self.get_container_status_by_name(name) != 'running':
            #     time.sleep(1)
        except Exception as e:
            raise e

    # endregion

    # region start All Containers
    def start_all_containers(self):
        self.start_mongodb()
        print()
        # self.start_nighcap_site()

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
        # print("Containers")
        # print(self.docker.containers.list(all=True))
        # self.docker.containers.run("mongo:latest")
        try:
            for _container in self.docker.containers.list(all=True):
                if _container.name == name:
                    self.printer.print_formatted_additional(
                        "Starting...", _container.name
                    )
                    # client = APIClient(base_url='unix://var/run/docker.sock')
                    # client.create_container(image='mongo:lastest',host_config=_container.attrs['Config'])
                    p = subprocess.Popen(
                        [
                            "docker",
                            "start",
                            dict(_container.attrs["Config"])["Hostname"],
                        ],
                        stdout=DEVNULL,
                    )
                    while p.poll() is None:
                        print("", end="", flush=False)
                        time.sleep(1)
                    self.printer.print_formatted_check(text="Container Started")
                    return True

            return False
            # while self.get_container_status_by_name(name) != 'running':
            #     time.sleep(1)
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
            self.printer.print_underlined_header(text="Creating Docker Containers")
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
            print()
            self.printer.print_underlined_header(text="Account data")
            
            # _ = os.path.join(
            #     Path(__file__).resolve().parent.parent, "manage.py"
            # )
            # p = subprocess.Popen(["python3", _, "createsuperuser"], stdout=PIPE, stdin=PIPE)
            # while p.poll() is None:
            #     print("", end="", flush=True)
            #     time.sleep(1)


            try:
                self.printer.print_formatted_additional("Making Migrations")
                _p1 = self._wait_while_processing(subprocess.Popen(["docker", "exec", "-it", "nightcapsite", "python3", "manage.py", "makemigrations"], stdout=DEVNULL))
            except Exception as e:
                raise e

            try:
                self.printer.print_formatted_additional("Migrating")
                _p2 = self._wait_while_processing(subprocess.Popen(["docker", "exec", "-it", "nightcapsite", "python3", "manage.py", "migrate"], stdout=DEVNULL))
            except Exception as e:
                raise e
            
            try:
                self.printer.print_underlined_header("Django Admin Account")
                self.printer.item_3("Please enter some information to create your web admin account", leadingTab=2, endingBreaks=1)
                _username = input(Fore.LIGHTGREEN_EX + str("User Name: %s" % (Fore.LIGHTCYAN_EX)))
                _email = input(Fore.LIGHTGREEN_EX + str("Email Address: %s" % (Fore.LIGHTCYAN_EX))) 
                _password = getpass.getpass(Fore.LIGHTGREEN_EX + str("Password:")) 
                _p3 = self._wait_while_processing(subprocess.Popen(["docker", "exec", "-it", "nightcapsite", "python", "manage.py", "shell", "-c",\
                    ("from django.contrib.auth.models import User; User.objects.create_superuser('%s', '%s', '%s')" % (_username, _email, _password))], stdout=PIPE, stderr=PIPE))
            except Exception as e:
                raise e

            print()
            self.printer.print_underlined_header("Django Clean Up")
            self.printer.print_formatted_check(text="Account Created")
            self.stop_nightcapsite()
        except Exception as e:
            raise e
    #endregion

    def _wait_while_processing(self, process: Popen):
        while process.poll() is None:
            print("", end="", flush=True)
            time.sleep(1)

        if process.returncode == 0:
            self.printer.print_formatted_check("Done", leadingTab=3)
        else:
            self.printer.print_error(Exception("Error pulling docker image: %s" % (process.returncode)))
    
        return process




    def _email_validation(self, email: str):
        regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
        if(re.search(regex, email)):
            return True
        else:
            return False

    # region Make Docker
    def make_docker(self):
        # ScreenHelper().clearScr()
        self.printer.item_1(
            "Please wait while making NC Docker Image"
        )
        p = subprocess.Popen(["make", "-C", Path(__file__).resolve().parent.parent], stdout=DEVNULL, stderr=DEVNULL)

        while p.poll() is None:
            print("", end="", flush=True)
            time.sleep(1)

        # print("returncode", p.returncode)
        if p.returncode == 0:
            self.printer.print_formatted_check("Done", leadingTab=3)
        else:
            self.printer.print_error(Exception("Error pulling docker image: %s" % (p.returncode)))

    # endregion

    # region Init Mongo
    def init_mongo(self, dc: NightcapCoreDockerChecker):
        if dc.mongo_im_exists == False:
            # ScreenHelper().clearScr()
            try:
                self.printer.print_underlined_header(
                    "Initializing: (Mongo)", endingBreaks=1
                )
                print(Fore.LIGHTBLACK_EX)
                dc.pull_image("mongo")
                self.printer.print_formatted_check(
                    text="Initialized", optionaltext="Mongo"
                )
                #
                return True
            except Exception as e:
                self.printer.print_formatted_delete(
                    text="Error with installing docker mongo image"
                )
                raise e
    # endregion
