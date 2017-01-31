#! usr/bin/env python

'''
Tests the 'xml_parse.smile_file_parser.py' module.

'''

import os
import unittest
import xml
import xml_parse.smil_file_parser as sfp


class TestSmilFileParser(unittest.TestCase):

    def test_class_init(self):
        ''' Create a SmilParse() class and test __init__. '''
        self.SMIL_FILE = r'\\capstage01\data\davep\joey_sa16-2048.smil'
        TestSmilParse = sfp.SmilParse(self.SMIL_FILE)

        self.assertEqual(self.SMIL_FILE, TestSmilParse.FULL_PATH)

        self.assertEqual(
            os.path.dirname(self.SMIL_FILE), TestSmilParse.DIR_NAME
        )

        self.assertEqual(
            os.path.basename(self.SMIL_FILE), TestSmilParse.BASE_NAME
        )

    def test_smil_probe(self):
        ''' Test file existence, file name & content validity. '''

        # Good file path, is file not dir, and can open it:
        self.SMIL_FILE = r'\\capstage01\data\davep\joey_sa16-2048.smil'
        TestSmilParse = sfp.SmilParse(self.SMIL_FILE)
        self.assertTrue(TestSmilParse.smil_probe())

        # Good file path, is file not dir, but bad file name:
        self.SMIL_FILE = r'\\capstage01\data\davep\joey_sa16-204.smil'
        TestSmilParse = sfp.SmilParse(self.SMIL_FILE)
        self.assertFalse(TestSmilParse.smil_probe())

        # Bad XML content should be rejected by defusedxml.
        self.SMIL_FILE = r'\\capstage01\data\davep\joey_sa16badxml-2048.smil'
        TestSmilParse = sfp.SmilParse(self.SMIL_FILE)
        with self.assertRaises(xml.etree.ElementTree.ParseError):
            TestSmilParse.smil_probe()

    def test_smil_ingest(self):
        ''' Test traversal of xml structure,
            and mp4 file checks.  For smil_ingest()
            to return true, the SMIL_FILE basedir needs
            correctly spelled/named, non-zero-byte mp4 files.
        '''
        self.SMIL_FILE = r'\\capstage01\data\davep\joey_sa16-2048.smil'
        TestSmilParse = sfp.SmilParse(self.SMIL_FILE)
        self.assertTrue(TestSmilParse.smil_ingest())


if __name__ == '__main__':
    unittest.main()
