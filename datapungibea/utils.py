'''
datapungibea.utils
~~~~~~~~~~~~~~~~~~

This module provides utility functions that are used 
within datapungibea and by the users when they want 
to update internal configs.
'''

import json
import pkg_resources

def getKey(userSettings = {}):
    '''
      :param userSettings: (optional) dictionary of  ``'ApiKeysPath': a path to json with API Keys`` and  ``'ApiKeyLabel': label (key) of JSON entry containing the key``
      If userSettings is an empty dictionary (default option), method will try to load it from saved userSettings.  
    '''
    if userSettings == {}:
        userSettings = getUserSettings()

    try:
        with open(userSettings['ApiKeysPath']) as jsonFile:
             key = (json.load(jsonFile))[userSettings['ApiKeyLabel']]
        return(key)
    except:
        print('Could not retrive key of ' + userSettings['ApiKeyLabel'] + ' from \n '+ userSettings['ApiKeysPath'])
        return   

def getResourcePath(relativePath, resource_package = __name__):
    '''
     Given relative, get its full path
     eg: relative path: /config/userSettings.json
     will return
     beafullfetchpy path + relative path
     note: can replace resource_package with package name:
     eg: 'beafullfetchpy'
    '''
    fullPath = pkg_resources.resource_filename(resource_package, relativePath)
    return(fullPath)

def getUserSettings():
    '''
        loads the userSettings file.
    '''
    userSettingsPath = getResourcePath('/config/userSettings.json','datapungibea') #TODO: remove package name.
    try:
        with open(userSettingsPath) as jsonFile:
             config = json.load(jsonFile)
        return(config)
    except:
        print('datapungibea/utils.py: Could not open the userSettings: \n datapungibea/config/userSettings.json')
        pass


def setUserSettings(newPath):  #TODO: check if still valid
    '''
       sets the api key path in the package config file
    '''
    userSettingsPath = getResourcePath('/config/userSettings.json')
    try:
        with open(userSettingsPath) as jsonFile:
             config = json.load(jsonFile)
    except:
        print('Could not open the configuration file: \n beafullfetchpy/config/userSettings.json')
        pass
    
    config['ApiKeysPath'] = newPath

    try:
        with open(userSettingsPath,'w') as jsonFile:
            json.dump(config,jsonFile)
        print('Path to the API Keys updated! New Path: \n' + config['ApiKeysPath'])
    except:
        print('Could not save the configuration to file: \n beafullfetchpy/config/userSettings.json \n Path API Key not updated')
        pass