'''
    installer for modelChecker
'''

import os
import sys
import shutil

from os import path
from os import rename
from os import unlink
from distutils.dir_util import copy_tree
from time import sleep


homedir = os.path.expanduser('~')
mayaVersions = ['2016','2017','2018','2019','2020']
os = sys.platform
setupFilePath = path.dirname(path.abspath('__file__')) + '/'


def getOS():
    if os == 'linux' or os == 'linux2':
        # linux
        mayaUserPath = homedir + '/Library/Preferences/Autodesk/maya/'
        if path.exists(mayaUserPath):
            return mayaUserPath
        else:
            print('Maya user path not found')
    elif os == 'darwin':
        # OS X
        mayaUserPath = homedir + '/Library/Preferences/Autodesk/maya/'
        if path.exists(mayaUserPath):
            return mayaUserPath
        else:
            print('Maya user path not found')
    elif os == 'win32':
        # Windows
        mayaUserPath = homedir + '/Documents/maya/'
        if path.exists(mayaUserPath):
            return mayaUserPath
        else:
            print('Maya user path not found')
        

def install():
    mayaUserPath = getOS()
    for mayaversion in mayaVersions:
        
        ### Insert config in "shelf_Custom.mel" file to add modelChecker button to Custom shelf
        #
        allMayaShelvesPath = []
        allMayaShelvesPath.append(mayaUserPath + mayaversion + '/prefs/shelves/')

        for mayaShelfPath in allMayaShelvesPath:        
            if path.exists(mayaShelfPath):

                file1 = mayaShelfPath + 'shelf_Custom.mel'
                file2 = setupFilePath + 'shelfIcon.mel'
                file3 = mayaShelfPath + 'shelf_Custom.mel.tmp'

                # Backup shelf_Custom.mel
                shutil.copy(file1, file1 + '.bak')

                # Append config text to file
                filenames = [file1, file2]
                with open(file3, 'w') as outfile:
                    for fname in filenames:
                        with open(fname) as infile:
                            outfile.write(infile.read())

                # Remove first closure bracket to sanity code
                # Read in the file
                with open(file3, 'r') as file :
                    filedata = file.read()

                # Replace the target string
                filedata = filedata.replace('}', '', 1)

                # Write the file out again
                with open(file3, 'w') as file:
                    file.write(filedata)

                # Restore original name
                unlink(file1)
                rename(file3, file1)

                print('Adding modelChecker button to Maya ' + mayaversion + ' custom shelf...')
                sleep(0.3)

                # copy icon to Maya icons default folder
                iconFile = 'modelChecker_icon.png'
                iconSrc = setupFilePath + '/src/' + iconFile
                iconTarget = mayaUserPath + mayaversion + '/prefs/icons/' + iconFile
                shutil.copy(iconSrc, iconTarget)
                print('Copying ' + iconFile + ' to ' + mayaUserPath + mayaversion + '/prefs/icons/')
                sleep(0.3)

                
        ### Copy src contents to destination 
        #
        allMayaScriptPath = []
        allMayaScriptPath.append(mayaUserPath + mayaversion + '/scripts/')

        for p in allMayaScriptPath:        
            if path.exists(p):
                # copy subdirectory example
                src = setupFilePath + '/src/'
                target = p + '/modelChecker/'

                copy_tree(src, target)
                
                print('Copying modelChecker.py to ' + mayaUserPath + mayaversion + '/scripts/modelChecker/' )
                sleep(0.3)

                print('modelChecker installed successfully for Maya ' + mayaversion + '!\n')

   
getOS()
install()