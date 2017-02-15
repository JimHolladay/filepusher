#! usr/bin/env python

"""
Tests the './configuration/config_targets.py' module.

This test file is in FilePusher/tests
and config_targets.py is in project root ('.').

Your CMD prompt should be at rest in FilePusher,
and you call the test with something like this:

> cls & python ./tests/test_some_module_name.py

"""
import linecache
import os
import unittest

import yaml

from .. configuration import config_targets as cis


class TestYamlIngestConfig(unittest.TestCase):
    """ This class runs tests against the target configuration file. """
    def test_conf_exists(self):
        """ Check if YAML configuration file exists """
        self.assertTrue(os.path.exists(cis.FULL_PATH))

    def test_conf_file_vs_dir(self):
        """ Make sure it's a file not a dir. """
        self.assertTrue(os.path.isfile(cis.FULL_PATH))

    def test_conf_eol(self):
        """ Check for DOS EOL.  We want False. """
        with open(cis.FULL_PATH, 'r') as conf:
            self.assertNotIn('\r\n', conf)

    def test_what_is_line_seven(self):
        """ Is line 7 what I think it is? We want True. """
        text = 'PS-320'
        line = linecache.getline(cis.FULL_PATH, 7)
        self.assertIn(text, line)

    # Need to check for meaningful data.
    def test_conf_is_machine(self):
        """ Check DB Address. """
        with open(cis.FULL_PATH, 'r') as conf:
            target_file = yaml.load(conf)
            self.assertEqual(target_file['Targets'][0]['IsMachine'], False)


if __name__ == '__main__':
    unittest.main()
