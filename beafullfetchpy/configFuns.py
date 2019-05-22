import json
import pkg_resources

def getKey(beaEntryName = 'BEA'):
    path = (getConfig())['ApiKeysPath']
    try:
        with open(path) as jsonFile:
             key = (json.load(jsonFile))[beaEntryName]
        return(key)
    except:
        print('Could not retrive key of ' + beaEntryName + ' from \n '+path)
        pass   

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

def getConfig():
    '''
        loads the configuration file.
    '''
    userSettingsPath = getResourcePath('/config/userSettings.json')
    try:
        with open(userSettingsPath) as jsonFile:
             config = json.load(jsonFile)
        return(config)
    except:
        print('beafullfetchpy/configFuns: Could not open the configuration file: \n beafullfetchpy/config/userSettings.json')
        pass


def setConfig_apiKeyPath(newPath):
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