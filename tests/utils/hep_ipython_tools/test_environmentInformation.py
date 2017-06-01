# Licensed under a 3-clause BSD style license, see LICENSE.
from unittest import TestCase
try:
    from unittest.mock import patch, MagicMock
except ImportError:
    from mock import patch, MagicMock

import datetime

from skhep.utils.hep_ipython_tools.information import EnvironmentInformation


class TestEnvironmentInformation(TestCase):

    def setUp(self):
        self.patch = patch("skhep.utils.hep_ipython_tools.information.datetime")
        datetime_patch = self.patch.start()

        datetime_patch.now = MagicMock(return_value=datetime.datetime(1999, 11, 12))

        self.information = EnvironmentInformation()

        self.information.externals_version = "Version"
        self.information.externals_option = "ExternalOption"
        self.information.option = "Option"
        self.information.architecture = "Architecture"
        self.information.release = "Release"
        self.information.release_folder = "ReleaseFolder"

    def tearDown(self):
        self.patch.stop()

    def test_str(self):
        self.information._cached_revision = "Revision"

        string_information = str(self.information)
        self.assertEqual(string_information.splitlines(), ["externals version: Version",
                                                           "externals option: ExternalOption",
                                                           "option: Option",
                                                           "architecture: Architecture",
                                                           "release: Release",
                                                           "release folder: ReleaseFolder",
                                                           "revision number: Revision",
                                                           "date: 1999-11-12"])

    def test_repr(self):
        self.information._cached_revision = "Revision"
        string_information = str(self.information)
        repr_information = self.information.__repr__()

        self.assertEqual(repr_information, string_information)

    def test_cached_revision(self):
        self.information._cached_revision = "Revision"

        self.assertEqual(self.information.revision_number, "Revision")

    def test_new_revision(self):

        self.information.get_current_revision_number = MagicMock(return_value="OtherRevision")

        self.assertEqual(self.information.revision_number, "OtherRevision")

        self.information.get_current_revision_number.assert_called_once_with()

    def test_get_current_revision(self):
        pass
