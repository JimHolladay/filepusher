#===============================================================================
# file_and_folder.py for FilePusher
# 
# This file contains the class for both the file and folder objects 
#
# for use with python 3.5
#===============================================================================
'''  This module holds the classes for both files and folders. '''

class FileObject(object):
    
    def __init__(self, name, full_path):
        self.name = name
        self.full_path = full_path
        self.target = dict()
        self.smil_validation = False
        self.destination = ""
        self.start_time = ""
        self.finish_time = ""
        
class FolderObject(object):
    
    def __init__(self, name, full_path):
        self.name = name
        self.full_path = full_path
        self.target = dict()
        self.smil_validation = True
        self.destination = ""
        self.start_time = ""
        self.finish_time = ""