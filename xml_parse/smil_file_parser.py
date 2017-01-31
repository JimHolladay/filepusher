#===============================================================================
# smil_file_parser.py for FilePusher
# 
# This validates the smil file and its contents.  It requires a specific dict
# to process with the following items: name, priority, smil_validation and
# full_path. 
#
# for use with python 3.5
#===============================================================================
''' This module checks a SMIL file's filename and contents for validity.'''

import file_and_folder
import os
import re
from defusedxml import ElementTree
from config.log_settings import log2log

class SmilParse():
    
    def __init__(self, item):
        if item.destination == "":
            self._FULL_PATH = item.full_path
            self._DIR_NAME = os.path.dirname(item.full_path) + "/"
        else:
            self._FULL_PATH = item.destination + item.name
            self._DIR_NAME = os.path.dirname(item.destination) + "/" 
        self._BASE_NAME = item.name

    def _fcheck(self):
        ''' Test the smil file itself. '''
        smil_fcheck_status = False
        if not os.path.exists(self._FULL_PATH):
            log2log("warning", "SmilParse: " + self._FULL_PATH + " doesn't exist.")
        elif not os.path.isfile(self._FULL_PATH):
            log2log("warning", "SmilParse: " + self._FULL_PATH + " is not a file.")
        elif not os.stat(self._FULL_PATH).st_size > 0:
            log2log("warning", "SmilParse: " + self._FULL_PATH + " has no contents.")
        else:
            smil_fcheck_status = True
        return smil_fcheck_status

    def _fname(self):
        ''' Use RegEx to check smil file name structure. '''
        stub = '^[a-zA-Z0-9]{4}_[a-zA-Z0-9]*'
        bitrate = '-[0-9]{4}'
        ext = '.smil$'
        pattern = stub + bitrate + ext
        if re.search(pattern, self._BASE_NAME):
            smil_fname_status = True
        else:
            smil_fname_status = False
        return smil_fname_status

    def _fcontent(self):
        ''' Parse the XML content to determine validity. This includes testing
        the individual video files listed in the smil file.'''
        smil_content_status = False
        errorcount = 0 
        
        #Build the Regex
        stub = '^[a-zA-Z0-9]{4}_[a-zA-Z0-9]*'
        bitrate = '-[0-9]{3,4}'
        suffix = '_[0-9]{3,4}x[0-9]{3,4}'
        ext = '.mp4$'
        pattern = stub + bitrate + suffix + ext       
        
        # Test each file listed in the smil file
        with open(self._FULL_PATH, 'r') as f:
            tree = ElementTree.parse(f)
                      
            for node in tree.iter('video'):
                mp4str = re.split(':', node.attrib.get('src'))[1]
                mp4file = self._DIR_NAME + mp4str                
                smil_content_status = False
                if not re.search(pattern, mp4str):
                    log2log("warning", "SmilParse: " + 
                            'Malformed mp4 file name string in SMIL: {}'.format(mp4str))
                    errorcount += 1
                    break
                elif not re.search(pattern, mp4str):
                    log2log("warning", "SmilParse: " +  
                            'Malformed mp4 filename on disk: {}'.format(mp4str))
                    errorcount += 1
                    break
                elif not os.path.exists(mp4file):
                    log2log("warning", "SmilParse: " + 'file not found: {}'.format(mp4file))
                    errorcount += 1
                    break
                else:
                    try:
                        open(mp4file, 'r')               
                        if not os.path.getsize(mp4file) > 0 and errorcount == 0:
                            log2log("warning", "SmilParse: " + 
                                    'filesize is 0 bytes: {}'.format(mp4str))
                            break
                    except (PermissionError, IOError):
                        log2log("warning", "SmilParse: " + 
                                'file in use: {}'.format(mp4str))
                        errorcount += 1
                        break
        if errorcount == 0:
            smil_content_status = True
        return smil_content_status

    def smil_probe(self):
        ''' Run three local methods to validate everything associated with the 
        .smil file. '''
        bReturn = False
        if (not self._fcheck() or 
            not self._fname() or 
            not self._fcontent()):
            log2log("warning", "SmilParse: " + 'Something is wrong with {}'.format(self._FULL_PATH))
        else:
            bReturn = True
        return bReturn
    
    def smil_dereference(self):
        file_list = []
        if self.smil_probe():
            with open(self._FULL_PATH, 'r') as f:
                tree = ElementTree.parse(f)            
                for node in tree.iter('video'):
                    mp4str = re.split(':', node.attrib.get('src'))[1]
                    mp4file = self._DIR_NAME + mp4str
                    file_list.append(mp4file)
        else:
            log2log('debug', "Smil probe failed on " + self._BASE_NAME)
        return file_list
    
if __name__ == '__main__':
    MyObj = SmilParse(SMIL_FILE)
    MyObj.smil_probe()
