# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Import
from nightcappackages.classes.databases.mogo.connections.mongo_connection import (
    MongoDatabaseConnection,
)
from nightcapcore.interface.template_interface import abstractfunc

# endregion


class MongoDatabaseOperationsConnection(MongoDatabaseConnection):
    """

    This class is used to define some of the MongoDatabseInterface

    ...

     Methods
    -------
        Accessible
        -------

            create(self): -> pass
                Must be implemented when inherited

            read(self) -> pass
                Must be implemented when inherited

            update(self) -> pass
                Must be implemented when inherited

            delete(self) -> pass
                Must be implemented when inherited
    """

    # region Init
    def __init__(self):
        super().__init__()

    # endregion

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
