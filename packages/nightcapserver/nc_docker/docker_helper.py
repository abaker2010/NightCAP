# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.

from pathlib import Path
import subprocess
from subprocess import Popen, PIPE, STDOUT
import time
import os
import docker as dDocker
from docker import APIClient
from colorama.ansi import Fore, Style
from nightcapcore.configuration.base import NightcapCLIConfiguration
from nightcapcore.docker.docker_checker import NightcapCoreDockerChecker
from nightcapcore.helpers.screen.screen_helper import ScreenHelper
from nightcapcore.printers.print import Printer
from nightcappackages.classes.databases.mogo.checker.mongo_database_checker import MongoDatabaseChecker
DEVNULL = open(os.devnull, 'wb')


class NightcapDockerHelper(object):
    def __init__(self, config: NightcapCLIConfiguration) -> None:
        super().__init__()
        self.conf = config
        self.yes = self.conf.currentConfig.get('NIGHTCAPCORE', 'yes').split()
        self.printer = Printer()
        self.docker = dDocker.from_env()

    def prepare_containers(self):
        try:
            self.start_container_by_name('nightcapmongodb')
            time.sleep(3)
            MongoDatabaseChecker().initialize_database()
            # _django_started = self.start_container_by_name('nightcapsite')
            return True
        except Exception as e:
            raise e


    def restart_containers(self):
        self.stop_all_containers()
        self.start_all_containers()
    

    def init_containers(self, agreement: str, dc: NightcapCoreDockerChecker):
        try:
            if agreement in self.yes:
                self.init_mongo(dc)
                self.init_nc_site(dc)
                self.build_containers()
            print(Style.RESET_ALL)
            return True
        except Exception as e:
            raise e

    def init_nc_site(self, dc: NightcapCoreDockerChecker):
        if dc.ncs_exits == False:
            self.printer.print_underlined_header(text="Initializing: (NC Site)",endingBreaks=1)
            self.make_docker()

    def stop_all_containers(self):
        self.printer.print_underlined_header_undecorated(text="Stopping Docker Containers")
        self.stop_mongodb()
        self.stop_nightcapsite()
        return True

    def stop_nightcapsite(self):
        self.stop_container_by_name('nightcapsite')

    def stop_mongodb(self):
        self.stop_container_by_name('nightcapmongodb')
        
    def stop_container_by_name(self, name: str):
        try:
            # for _container in self.docker.containers.list(all=True):
            #     if _container.name == name:
            self.printer.print_formatted_additional("Stopping...", name)
            # client = APIClient(base_url='unix://var/run/docker.sock')
            # client.stop(_container.name)
            p = subprocess.Popen(['docker', 'stop', name])
            while p.poll() is None:
                print('.', end='', flush=True)
                time.sleep(1)
            self.printer.print_formatted_check(text="Stopped", leadingTab=3)
            # return True
                
            # return False
            # while self.get_container_status_by_name(name) != 'running':
            #     time.sleep(1)
        except Exception as e:
            raise e

    def start_all_containers(self):
        self.start_mongodb()
        self.start_nighcap_site()

    def start_mongodb(self):
        self.start_container_by_name('nightcapmongodb')

    def start_nighcap_site(self):
        self.start_container_by_name('nightcapsite')

    def start_container_by_name(self, name: str):
        # print("Containers")
        # print(self.docker.containers.list(all=True))
        # self.docker.containers.run("mongo:latest")
        try:
            for _container in self.docker.containers.list(all=True):
                if _container.name == name:
                    self.printer.print_formatted_additional("Starting...", _container.name)
                    # client = APIClient(base_url='unix://var/run/docker.sock')
                    # client.create_container(image='mongo:lastest',host_config=_container.attrs['Config'])
                    p = subprocess.Popen(['docker', 'start', dict(_container.attrs['Config'])['Hostname']])
                    while p.poll() is None:
                        print('.', end='', flush=False)
                        time.sleep(1)
                    self.printer.print_formatted_check(text="Created Containers")
                    return True
                
            return False
            # while self.get_container_status_by_name(name) != 'running':
            #     time.sleep(1)
        except Exception as e:
            raise e

    def get_mongo_container_status(self):
        return self.get_container_status_by_name('nightcapmongodb')
    
    def get_site_container_status(self):
        return self.get_container_status_by_name('nightcapsite')

    def mongo_continer_exists(self):
        return self.container_exists('nightcapmongodb')

    def site_container_exists(self):
        return self.container_exists('nightcapsite')

    def container_exists(self, name: str):
        try:
            for _container in self.docker.containers.list(all=True):
                if _container.name == name:
                    return True
            return False
        except Exception as e:
            raise e

    def get_container_status_by_name(self, name: str):
        try:
            for _container in self.docker.containers.list(all=True):
                if _container.name == name:
                    return _container.attrs['State']['Status']
            return _container.attrs['State']['Status']
        except Exception as e:
            return 'Missing'


    def build_containers(self):
        try:
            self.printer.print_formatted_additional(text='Creating Docker Containers')
            _ = os.path.join(Path(__file__).resolve().parent.parent, 'docker-compose.yml')
            p = subprocess.Popen(['docker-compose', '-f', _, 'up', '--no-start'])
            while p.poll() is None:
                print('.', end='', flush=True)
                time.sleep(1)
            self.printer.print_formatted_check(text="Created Containers")
        except Exception as e:
            raise e

    def make_docker(self):
        ScreenHelper().clearScr()
        self.printer.print_underlined_header_undecorated(text='Making docker image', endingBreaks=1)
        p = subprocess.Popen(['make', '-C', Path(__file__).resolve().parent.parent])

        while p.poll() is None:
            print('.', end='', flush=True)
            time.sleep(1)

        print('returncode', p.returncode)

    def init_mongo(self, dc: NightcapCoreDockerChecker):
        if dc.mongo_im_exists == False:
            ScreenHelper().clearScr()
            try:
                self.printer.print_underlined_header(text="Initializing: (Mongo)",endingBreaks=1)
                print(Fore.LIGHTBLACK_EX)
                dc.pull_image('mongo')
                ScreenHelper().clearScr()
                self.printer.print_formatted_check(text="Initialized", optionaltext='Mongo')
                # 
                return True
            except Exception as e:
                self.printer.print_formatted_delete(text="Error with installing docker mongo image")
                raise e