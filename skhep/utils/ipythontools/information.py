# Licensed under a 3-clause BSD style license, see LICENSE.
from datetime import datetime
from subprocess import check_output


class EnvironmentInformation:

    """
    Helper class for accessing the information about the environment.
    """

    def __init__(self):
        """
        Get the variables from the environment variables.
        """
        #: Externals version
        self.externals_version = ""
        #: Compile options of externals
        self.externals_option = ""
        #: Compile options
        self.option = ""
        #: OS
        self.architecture = ""
        #: Release version
        self.release = ""
        #: Release folder
        self.release_folder = ""
        #: Revision number (cached, the real getter is the property)
        self._cached_revision = ""

    @property
    def revision_number(self):
        """
        Get the cached revision number from SVN or get it from SVN directly.
        """
        if not self._cached_revision:
            self._cached_revision = self.get_current_revision_number()

        return self._cached_revision

    def __str__(self):
        """
        A nice representation.
        """
        result = ""
        result += "externals version: " + self.externals_version + "\n"
        result += "externals option: " + self.externals_option + "\n"
        result += "option: " + self.option + "\n"
        result += "architecture: " + self.architecture + "\n"
        result += "release: " + self.release + "\n"
        result += "release folder: " + self.release_folder + "\n"
        result += "revision number: " + self.revision_number + "\n"
        result += "date: " + datetime.now().strftime("%Y-%m-%d") + "\n"
        return result

    def __repr__(self):
        """
        Also for ipython.
        """
        return self.__str__()

    def get_current_revision_number(self):
        """
        Try to download the current revision number from SVN.
        """
        try:
            return check_output(["git", "log", "-1", "--format='%H'"], cwd=self.release_folder).decode()
        except:
            return ""
