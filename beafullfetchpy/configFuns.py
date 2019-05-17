import json


def getKey(beaEntryName = 'BEA'):
    path = (getConfig())['ApiKeysPath']
    try:
        with open(path) as jsonFile:
             key = (json.load(jsonFile))[beaEntryName]
        return(key)
    except:
        print('Could not retrive key of ' + beaEntryName + ' from \n '+path)
        pass   


def getConfig():
    '''
        loads the configuration file.
    '''
    try:
        with open('beafullfetchpy/config/userSettings.json') as jsonFile:
             config = json.load(jsonFile)
        return(config)
    except:
        print('Could not open the configuration file: \n beafullfetchpy/config/userSettings.json')
        pass


def setConfig_apiKeyPath(newPath):
    '''
       sets the api key path in the package config file
    '''
    try:
        with open('beafullfetchpy/config/userSettings.json') as jsonFile:
             config = json.load(jsonFile)
    except:
        print('Could not open the configuration file: \n beafullfetchpy/config/userSettings.json')
        pass
    
    config['ApiKeysPath'] = newPath

    try:
        with open('beafullfetchpy/config/userSettings.json','w') as jsonFile:
            json.dump(config,jsonFile)
        print('Path to the API Keys updated! New Path: \n' + config['ApiKeysPath'])
    except:
        print('Could not save the configuration to file: \n beafullfetchpy/config/userSettings.json \n Path API Key not updated')
        pass