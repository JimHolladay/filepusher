#! usr/bin/env python

"""
Tests the 'xml_parse.smile_file_parser.py' module.
"""
import os
import unittest
import xml

from .. xml_parse import smil_file_parser as sfp


class TestSmilFileParser(unittest.TestCase):
    """ This is the tests for the smil file parser. """
    def test_class_init(self):
        """ Creates a SmilParse() instance and tests __init__. """
        smil_file = r'\\capstage01\data\davep\joey_sa16-2048.smil'
        test_smil_parse = sfp.SmilParse(smil_file)

        self.assertEqual(smil_file, test_smil_parse.full_path)
        self.assertEqual(os.path.dirname(smil_file), test_smil_parse.dir_name)
        self.assertEqual(os.path.basename(smil_file), test_smil_parse.base_name)

    def test_smil_probe(self):
        """ Test file existence, file name & content validity. """

        # Good file path, is file not dir, and can open it:
        smil_file = r'\\capstage01\data\davep\joey_sa16-2048.smil'
        test_smil_parse = sfp.SmilParse(smil_file)
        self.assertTrue(test_smil_parse.smil_probe())

        # Good file path, is file not dir, but bad file name:
        smil_file = r'\\capstage01\data\davep\joey_sa16-204.smil'
        test_smil_parse = sfp.SmilParse(smil_file)
        self.assertFalse(test_smil_parse.smil_probe())

        # Bad XML content should be rejected by defusedxml.
        smil_file = r'\\capstage01\data\davep\joey_sa16badxml-2048.smil'
        test_smil_parse = sfp.SmilParse(smil_file)
        with self.assertRaises(xml.etree.ElementTree.ParseError):
            test_smil_parse.smil_probe()

    def test_smil_ingest(self):
        """ Test traversal of xml structure,
            and mp4 file checks.  For smil_ingest()
            to return true, the SMIL_FILE basedir needs
            correctly spelled/named, non-zero-byte mp4 files.
        """
        smil_file = r'\\capstage01\data\davep\joey_sa16-2048.smil'
        test_smil_parse = sfp.SmilParse(smil_file)
        self.assertTrue(test_smil_parse.smil_dereference())


if __name__ == '__main__':
    unittest.main()
