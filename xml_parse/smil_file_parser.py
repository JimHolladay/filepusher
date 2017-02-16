# ===============================================================================
# smil_file_parser.py for FilePusher
#
# This validates the smil file and its contents.  It requires a specific dict
# to process with the following items: name, priority, smil_validation and
# full_path.
#
# for use with python 3.5
# ===============================================================================
""" This module checks a SMIL file's filename and contents for validity."""
import os
import re

from defusedxml import ElementTree

from .. configuration.log_settings import log2log


class SmilParse(object):
    """This is the class that ingests the smil files."""
    def __init__(self, item):
        if item.destination == "":
            self.full_path = item.full_path
            self.dir_name = os.path.dirname(item.full_path) + "/"
        else:
            self.full_path = item.destination + item.name
            self.dir_name = os.path.dirname(item.destination) + "/"
        self.base_name = item.name

    def _fcheck(self):
        """ Test the smil file itself. """
        smil_fcheck_status = False
        if not os.path.exists(self.full_path):
            log2log("warning", "SmilParse: " + self.full_path + " doesn't exist.")
        elif not os.path.isfile(self.full_path):
            log2log("warning", "SmilParse: " + self.full_path + " is not a file.")
        elif not os.stat(self.full_path).st_size > 0:
            log2log("warning", "SmilParse: " + self.full_path + " has no contents.")
        else:
            smil_fcheck_status = True
        return smil_fcheck_status

    def _fname(self):
        """ Use RegEx to check smil file name structure. """
        stub = '^[a-zA-Z0-9]{4}_[a-zA-Z0-9]*'
        bitrate = '-[0-9]{4}'
        ext = '.smil$'
        pattern = stub + bitrate + ext
        smil_fname_status = bool(re.search(pattern, self.base_name))
        return smil_fname_status

    def _fcontent(self):
        """" Parse the XML content to determine validity. This includes testing
        the individual video files listed in the smil file."""
        smil_content_status = False
        error_count = 0

        # Build the Regex
        stub = '^[a-zA-Z0-9]{4}_[a-zA-Z0-9]*'
        bit_rate = '-[0-9]{3,4}'
        suffix = '_[0-9]{3,4}x[0-9]{3,4}'
        ext = '.mp4$'
        pattern = stub + bit_rate + suffix + ext

        # Test each file listed in the smil file
        with open(self.full_path, 'r') as file:
            tree = ElementTree.parse(file)

            for node in tree.iter('video'):
                mp4str = re.split(':', node.attrib.get('src'))[1]
                mp4file = self.dir_name + mp4str
                smil_content_status = False
                if not re.search(pattern, mp4str):
                    log2log("warning", "SmilParse: " +
                            'Malformed mp4 file name string in SMIL: {}'.format(mp4str))
                    error_count += 1
                    break
                elif not re.search(pattern, mp4str):
                    log2log("warning", "SmilParse: " +
                            'Malformed mp4 filename on disk: {}'.format(mp4str))
                    error_count += 1
                    break
                elif not os.path.exists(mp4file):
                    log2log("warning", "SmilParse: " + 'file not found: {}'.format(mp4file))
                    error_count += 1
                    break
                else:
                    try:
                        open(mp4file, 'r')
                        if not os.path.getsize(mp4file) > 0 and error_count == 0:
                            log2log("warning", "SmilParse: " +
                                    'file size is 0 bytes: {}'.format(mp4str))
                            break
                    except (PermissionError, IOError):
                        log2log("warning", "SmilParse: " +
                                'file in use: {}'.format(mp4str))
                        error_count += 1
                        break
        if error_count == 0:
            smil_content_status = True
        return smil_content_status

    def smil_probe(self):
        """ Run three local methods to validate everything associated with the
        .smil file. """
        b_return = False
        if (not self._fcheck() or
                not self._fname() or
                not self._fcontent()):
            log2log("warning", "SmilParse: " + 'Something is wrong with {}'.format(self.full_path))
        else:
            b_return = True
        return b_return

    def smil_dereference(self):
        """ Return file list from smil file. """
        file_list = []
        if self.smil_probe():
            with open(self.full_path, 'r') as file:
                tree = ElementTree.parse(file)
                for node in tree.iter('video'):
                    mp4str = re.split(':', node.attrib.get('src'))[1]
                    mp4file = self.dir_name + mp4str
                    file_list.append(mp4file)
        else:
            log2log('debug', "Smil probe failed on " + self.base_name)
        return file_list
