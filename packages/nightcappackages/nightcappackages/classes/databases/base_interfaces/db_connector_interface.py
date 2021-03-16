# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
from nightcapcore.interface.template_interface import Interface, abstractfunc

class DatabaseConnectorInterface(metaclass=Interface):
    @abstractfunc
    def connect(self):
        pass

    @abstractfunc
    def transfer(self):
        pass

    @abstractfunc
    def close(self):
        pass
    