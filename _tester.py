from tests.test_config_ingest_service import TestYamlIngestService
from tests.test_config_ingest_targets import TestYamlIngestConfig
from tests.test_main_thread import TestQueues
from tests.test_smil_file_parser import TestSmilFileParser
import unittest


class AllTests(unittest.TestSuite):

    def suite(self):
        suite = unittest.TestSuite()
        suite.addTest(TestYamlIngestConfig)
        suite.addTest(TestYamlIngestService)
        suite.addTest(TestQueues)
        suite.addTest(TestSmilFileParser)
        self.run(suite)


if __name__ == "__main__":
    unittest.main()
