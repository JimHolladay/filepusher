# ==============================================================================
# _tester.py
#
# This module runs all of the tests in the ./tests folder.
#
# Written with/for Python 3.4.3.
# ==============================================================================
""" This module runs all of the tests for cs2vs filepusher."""
import unittest
from .tests.test_config_ingest_service import TestYamlIngestService
from .tests.test_config_ingest_targets import TestYamlIngestConfig
from .tests.test_smil_file_parser import TestSmilFileParser


class AllTests(unittest.TestSuite):
    """ Run all of the tests in the test suite."""

    def suite(self):
        """ Run all of the tests in the test suite."""
        suite = unittest.TestSuite()
        suite.addTest(TestYamlIngestConfig)
        suite.addTest(TestYamlIngestService)
        suite.addTest(TestSmilFileParser)
        self.run(suite)

if __name__ == "__main__":
    unittest.main()
