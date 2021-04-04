# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
#region Imports
import os
import errno
#endregion

class NightcapCoreFiles:
    """
        
        This class is used to help validate user input to the console

        ...

        Attributes
        ----------
            ppath: -> str
                the package path

        Methods 
        -------
            Accessible 
            -------
                create_html_report(self, data): -> None
                    Create Html reports

            None Accessible
            -------
                _make_dirs(self): -> None
                    Makes the needed directories passed

    """
    #region Init
    def __init__(self, ppath: str):
        self.ppath = ppath
    #endregion

    #region Make Dirs
    def _make_dirs(self):
        _path = os.path.dirname(self.ppath)
        try:
            print("testing", _path)
            os.makedirs(_path)
        except OSError as exc:  # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(_path):
                pass
            else:
                raise
    #endregion

    #region Generate reports
    def create_html_report(self, data):
        print("Creating HTML Report at:", self.ppath)
        print("Data to be wrote", len(data))
        self._make_dirs()
        # self.mkdir_p(os.path.dirname(self.ppath))
        # # file = open('myfile.dat', 'w+')
        # file.close()
        with open(self.ppath, "w+") as file:
            file.write(data)
        print("File Wrote")
    #endregion

    # def mkdir_p(self, path):
    #     try:
    #         os.makedirs(path)
    #     except OSError as exc: # Python >2.5
    # if exc.errno == errno.EEXIST and os.path.isdir(path):
    #     pass
    # else: raise

    # def safe_open_w(path):
    #     ''' Open "path" for writing, creating any parent directories as needed.
    #     '''
    #     mkdir_p(os.path.dirname(path))
    #     return open(path, 'w')
