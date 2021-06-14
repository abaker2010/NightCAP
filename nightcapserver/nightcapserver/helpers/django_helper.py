# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Imports
from nightcapcore.helpers.screen.screen_helper import ScreenHelper
from pathlib import Path
import subprocess
from nightcapserver.helpers.docker_image_helper import NightcapDockerImageHelper
from nightcapserver.helpers.docker_container_helper import NightcapDockerContainerHelper
import os
import time
import getpass
import re
from colorama import Fore
from nightcapserver.helpers.docker_status import NightcapDockerStatus

DEVNULL = open(os.devnull, "wb")
# endregion

class NightcapDjangoDockerHelper(NightcapDockerContainerHelper, NightcapDockerImageHelper):
    # region Init
    def __init__(self) -> None:
        NightcapDockerContainerHelper.__init__(self, "nightcapsite")
        NightcapDockerImageHelper.__init__(self, "nightcapsite", "latest")
    # endregion

    def init_container(self) -> bool:
        try:
            self.printer.item_1(text="Init container", optionalText=self.name)
            _ = os.path.join(
                Path(__file__).resolve().parent.parent.parent, "docker-compose.yml"
            )
            p = subprocess.Popen(["docker-compose", "-f", _, "up", "--no-start", "website"], stdout=DEVNULL, stderr=DEVNULL)
            while p.poll() is None:
                print("", end="", flush=True)
                time.sleep(1)
            self.printer.print_formatted_check(text="Created Containers", endingBreaks=1)
        except Exception as e:
            raise e
        return True

    def init_image(self) -> bool:

        if self.image_exists() == NightcapDockerStatus.EXISTS:
            self.printer.print_formatted_check("Django Image", "Exists")
            return True
        else:
            self.printer.print_formatted_additional("Pulling image please wait...", leadingBreaks=1)
            # self.docker.images.pull(self.name+":"+self.tag)
            _ = Path(__file__).resolve().parent.parent
            p = subprocess.Popen(["make", "-C", Path(__file__).resolve().parent.parent.parent], stdout=DEVNULL, stderr=DEVNULL)

            while p.poll() is None:
                print("", end="", flush=True)
                time.sleep(1)


            if p.returncode != 0:
                self.printer.print_error(Exception("Error pulling docker image: %s" % (p.returncode)))
                return False
            self.printer.print_formatted_check("Pulled Image", "Mongo")
            return True

    def set_account(self):
        try:
            self.printer.print_underlined_header(text="Creating account")
            # self.start_all_containers()
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

    def _email_validation(self, email: str):
        regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
        if(re.search(regex, email)):
            return True
        else:
            return False
