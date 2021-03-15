# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.

from nightcappackages.classes.databases.base_interfaces.template_interface import Interface, abstractfunc


class MongoDatabaseOperationsInterface(metaclass=Interface):
    @abstractfunc
    def create(self):
        pass

    @abstractfunc
    def read(self):
        pass

    @abstractfunc
    def update(self):
        pass

    @abstractfunc
    def delete(self):
        pass