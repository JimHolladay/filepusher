#! usr/bin/env python

'''
Tests the './config_ingest_service.py' module.

This test file is in FilePusher/tests
and config_ingest_service.py is in project root ('.').

Your CMD prompt should be at rest in FilePusher,
and you call the test with something like this:

> cls & python ./tests/test_some_module_name.py

'''

import linecache
import os
import unittest
import yaml
import config.config_ingest_service as cis


class TestYamlIngestService(unittest.TestCase):

    def test_conf_exists(self):
        ''' Check if YAML config file exists '''
        self.assertTrue(os.path.exists(cis.FULL_PATH))

    def test_conf_file_vs_dir(self):
        ''' Make sure it's a file not a dir. '''
        self.assertTrue(os.path.isfile(cis.FULL_PATH))

    def test_conf_eol(self):
        ''' Check for DOS EOL.  We want False. '''
        with open(cis.FULL_PATH, 'r') as conf:
            self.assertNotIn('\r\n', conf)

    def test_what_is_line_seven(self):
        ''' Is line 7 what I think it is? We want True. '''
        text = 'PS-320'
        line = linecache.getline(cis.FULL_PATH, 7)
        self.assertIn(text, line)

    # Need to check for meaningful data.
    def test_conf_db_address(self):
        ''' Check DB Address. '''
        with open(cis.FULL_PATH, 'r') as conf:
            y = yaml.load(conf)
            self.assertEqual(y['Database']['DBAddr'], '192.168.208.61:5432')

if __name__ == '__main__':
    unittest.main()
