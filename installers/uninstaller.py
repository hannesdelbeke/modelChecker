'''
    Uninstaller for modelChecker
'''

import os
import sys
import shutil

from os import path
from os import rename
from os import unlink
from os import remove
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
        

def uninstall():
    mayaUserPath = getOS()
    for mayaversion in mayaVersions:
        
        ### Remove config in "shelf_Custom.mel" file to remove modelChecker button from Custom shelf
        #
        allMayaShelvesPath = []
        allMayaShelvesPath.append(mayaUserPath + mayaversion + '/prefs/shelves/')

        for mayaShelfPath in allMayaShelvesPath:        
            if path.exists(mayaShelfPath):

                # Restore original file
                rename(mayaShelfPath + 'shelf_Custom.mel', mayaShelfPath + 'shelf_Custom.mel.tmp')
                rename(mayaShelfPath + 'shelf_Custom.mel.bak', mayaShelfPath + 'shelf_Custom.mel')
                rename(mayaShelfPath + 'shelf_Custom.mel.tmp', mayaShelfPath + 'shelf_Custom.mel.bak')
                
                print('Removing modelChecker button from Maya ' + mayaversion + ' custom shelf...')
                sleep(0.3)

                # Remove icon from Maya icons default folder
                iconFilename = 'modelChecker_icon.png'
                iconPath = mayaUserPath + mayaversion + '/prefs/icons/'
                iconFile = iconPath + iconFilename
                remove(iconFile)
                print('Removing modelChecker_icon.png from ' + mayaUserPath + mayaversion + '/prefs/icons/')
                sleep(0.3)

                
        ### Removing modelChecker folder 
        #
        allMayaScriptPath = []
        allMayaScriptPath.append(mayaUserPath + mayaversion + '/scripts/')

        for p in allMayaScriptPath:        
            if path.exists(p):
                target = p + '/modelChecker/'
                shutil.rmtree(target, ignore_errors=True)

                print('Removing modelChecker from ' + mayaUserPath + mayaversion + '/scripts/' )
                sleep(0.3)

                print('modelChecker uninstalled successfully from Maya ' + mayaversion + '!\n')

   
getOS()
uninstall()