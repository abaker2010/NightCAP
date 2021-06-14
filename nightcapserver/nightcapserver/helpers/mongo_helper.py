# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Imports
from pathlib import Path
import subprocess
from nightcapserver.helpers.docker_image_helper import NightcapDockerImageHelper
from nightcapserver.helpers.docker_container_helper import NightcapDockerContainerHelper
import os
import time

from nightcapserver.helpers.docker_status import NightcapDockerStatus

DEVNULL = open(os.devnull, "wb")
# endregion

class NightcapMongoDockerHelper(NightcapDockerContainerHelper, NightcapDockerImageHelper):

    # region Init
    def __init__(self) -> None:
        NightcapDockerContainerHelper.__init__(self, "nightcapmongodb")
        NightcapDockerImageHelper.__init__(self, "mongo", "latest")
    # endregion

    def init_container(self) -> bool:
        try:
            self.printer.item_1(text="Init container", optionalText=self.name)
            _ = os.path.join(
                Path(__file__).resolve().parent.parent.parent, "docker-compose.yml"
            )
            p = subprocess.Popen(["docker-compose", "-f", _, "up", "--no-start", "mongodb"], stdout=DEVNULL, stderr=DEVNULL)
            while p.poll() is None:
                print("", end="", flush=True)
                time.sleep(1)
            self.printer.print_formatted_check(text="Created Containers", endingBreaks=1)
        except Exception as e:
            raise e
        return True

    def init_image(self) -> bool:
        
        # print("Pulling image: ", self.name, " : ", self.tag)
        if self.image_exists() == NightcapDockerStatus.EXISTS:
            self.printer.print_formatted_check("Mongo Image", "Exists")
            return True
        else:
            try:
                self.printer.print_formatted_additional("Pulling image please wait...", leadingBreaks=1)
                self.docker.images.pull(self.name+":"+self.tag)
                self.printer.print_formatted_check("Pulled Image", "Mongo")
                return True
            except Exception as e:
                return False

