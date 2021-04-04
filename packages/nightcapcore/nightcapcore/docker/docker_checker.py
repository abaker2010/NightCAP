# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Imports
import time
from subprocess import Popen, PIPE, STDOUT
import os

DEVNULL = open(os.devnull, "wb")
# endregion


class NightcapCoreDockerChecker(object):
    """

    This class is used to help validate user input to the console

    ...

    Attributes
    ----------
        mongo_im_exists: -> bool
            Checks to see if the mongo image exists

        ncs_exits: -> bool
            Checks to see if the nightcapsite image exists

    Methods
    -------
        Accessible
        -------
            pull_image(self, image: str): -> None
                pulls the docker image passed

        None Accessible
        -------
            __check_image(self, image: str, tag: str, grep: str): -> bool
                returns a boolean depending on if the image exists or not

            _check_setup(self): -> bool
                returns a boolean depending on if the image has been pulled from the Docker images
    """

    # region Init
    def __init__(self) -> None:
        super().__init__()
        self.mongo_im_exists = self.__check_image("mongo", "latest", "mongo")
        self.ncs_exits = self.__check_image("nightcapsite", "latest", "nightcapsite")

    # endregion

    # region Check Image
    def __check_image(self, image: str, tag: str, grep: str):
        _p1 = Popen(["docker", "images", ("%s:%s" % (image, tag))], stdout=PIPE)
        _p2 = Popen(["grep", grep], stdin=_p1.stdout, stdout=PIPE)
        _p1.stdout.close()
        _d = _p2.communicate()[0].decode("utf-8")
        _image_exists = True if _d != "" else False
        return _image_exists

    # endregion

    # region Check Set-up
    def _check_setup(self):
        if self.mongo_im_exists == False:
            print("install mongo")

    # endregion

    # region Pull Image
    def pull_image(self, image: str):
        print("Tring to pull", image)
        p = Popen(["docker", "pull", image])

        while p.poll() is None:
            print(".", end="", flush=True)
            time.sleep(1)

        print("returncode", p.returncode)
        # _p1 = subprocess.Popen(['docker', 'pull', image], stdout=subprocess.PIPE)
        # _p1.wait()
        # return

    # endregion
