import pandas as pd
import requests
import json
import pyperclip
from datapungibea import generalSettings 


# (1) Auxiliary functions ######################################################
def _getBaseRequest(baseRequest={},connectionParameters={},userSettings={}):
    '''
      Write a base request.  Could have other such functions, one for each type of base request.
    '''
    if baseRequest =={}:
       connectInfo = generalSettings.getGeneralSettings(connectionParameters = connectionParameters, userSettings = userSettings )
       return(connectInfo.baseRequest)
    else:
       return(baseRequest)

def _getBaseCode(codeEntries): 
    '''
      eg: start with an array vEntries, _getBaseCode(*vEntries)
    '''
    code = '''
import requests
import json    

#(1) get user API key (not advised but can just write key and url in the file)
#    file should contain: {{"BEA":{{"key":"YOUR KEY","url": "{}" }}}}

apiKeysFile = "{}"
with open(apiKeysFile) as jsonFile:
   apiInfo = json.load(jsonFile)
   url,key = apiInfo["BEA"]["url"], apiInfo["BEA"]["key"]    
     '''.format(*codeEntries)
    return(code)

def _clipcode(self):
    try:
        pyperclip.copy(self._lastLoad['code'])
    except:
        print("Loaded session does not have a code entry.  Re-run with verbose option set to True. eg: v.drivername(...,verbose=True)")

# (2) Drivers ###################################################################
class getDatasetlist():
    def __init__(self,baseRequest={},connectionParameters={},userSettings={}):
        self._connectionInfo = generalSettings.getGeneralSettings(connectionParameters = connectionParameters, userSettings = userSettings )
        self._baseRequest    = _getBaseRequest(baseRequest,connectionParameters,userSettings)
        self._lastLoad       = {}  #data stored here to assist functions such as clipcode
    
    def datasetlist(self,params = {},verbose=False):
        query = self._baseRequest
        query['params'].update({'method':'GETDATASETLIST'})
        
        retrivedData = requests.get(**query)
        
        df_output = self._cleanOutput(query,retrivedData)
        
        if verbose == False:
            self._lastLoad = df_output
            return(df_output)
        else:
            code = self._getCode(query)
            output = dict(dataFrame = df_output, request = retrivedData, code = code)  
            self._lastLoad = output
            return(output)  
    
    def _cleanOutput(self,query,retrivedData):
        if query['params']['ResultFormat'] == 'JSON':
            df_output =  pd.DataFrame( retrivedData.json()['BEAAPI']['Results']['Dataset'] )
        else:
            df_output =  pd.DataFrame( retrivedData.xml()['BEAAPI']['Results']['Dataset'] )  #TODO: check this works
    
        return(df_output)

    def _getCode(self,query):
        #general code to all drivers:
        try:
            url        = query['url']
            apiKeyPath = self._connectionInfo.userSettings["ApiKeysPath"]
        except:
            ur         = " incomplete connection information "
            apiKeyPath = " incomplete connection information "

        baseCode = _getBaseCode([url,apiKeyPath])
        
        #specific code to this driver:
        queryClean = query
        queryClean['url'] = 'url'
        queryClean['params']['UserID'] = 'key'
        
        
        queryCode = '''
query = {}
retrivedData = requests.get(**query)

dataFrame =  pd.DataFrame( retrivedData.json()['BEAAPI']['Results']['Dataset'] ) #replace json by xml if this is the request format
        '''.format(json.dumps(queryClean))
        
        queryCode = queryCode.replace('"url": "url"', '"url": url')
        queryCode = queryCode.replace('"UserID": "key"', '"UserID": key')
        
        return(baseCode + queryCode)
    
    def clipcode(self):
        _clipcode(self)

    def _driverMetadata(self):
        self.metadata =     [{
            "displayName":"List of Datasets",
            "method"     :"datasetlist",   #Name of driver main function - run with getattr(data,'datasetlist')()
            "params"     :{},
        }]


class getNIPA():
    def __init__(self,baseRequest={},connectionParameters={},userSettings={}):
        '''
          the baseRequest contains user Key, url of datasource, and prefered output format (JSON vs XML)
        '''
        self._baseRequest = _getBaseRequest(baseRequest,connectionParameters,userSettings) 
        self._lastLoad    = {}  #data stored here to asist other function as clipboard
    
    def NIPA(self,
        tableName,
        frequency      = 'Q',
        year           = 'X',
        payload        = {'method': 'GETDATA', 'DATABASENAME': 'NIPA', 'datasetname': 'NIPA', 'ParameterName': 'TableID'},
        tryFrequencies = False,  #TODO: remove
        outputFormat   = "tablePretty",
        verbose        = False
    ):
        '''
            User only need to specify the NIPA tableName, other parameters are defined by default.  Year (set to X) and Frequency (set to Q)
            can be redefined with payload = {Year = 1990, Frequency = 'A'}, for example.
            
            payload - will override the default
            
            outputFormat - table, tablePretty will return tables (the latter separates the metadata and pivots the table to index x time).
                           Else, returns the JSON, XML.
        '''
        # TODO: put the payload ={} all data in lowercase, else may repeat the load (say frequency=A and Frquency = Q will load A and Q)
        # load user preferences defined in userSettings, use suggested parameters, override w fun entry
        query = self._baseRequest
        query['params'].update({'TABLENAME': tableName})
        query['params'].update({'FREQUENCY':frequency})
        query['params'].update({'YEAR':year})
        query['params'].update(payload)
        
        # TODO: try loading different frenquencies if no return
        #
        retrivedData = requests.get(**query)
        
        output         = self._cleanOutput(query,retrivedData,outputFormat) #a dict of a df or df and meta (tablePretty)
        
        if verbose == False:
            self._lastLoad = output['dataFrame']
            return(self._lastLoad)
        else:
           output['code']    = self._getCode(query)
           output['request'] = retrivedData
           self._lastLoad = output
           return(output)       
    
    def _cleanOutput(self,query,retrivedData, outputFormat):
        if query['params']['ResultFormat'] == 'JSON':
            df_output =  pd.DataFrame(retrivedData.json()['BEAAPI']['Results']['Data'])
        else:
            df_output =  pd.DataFrame(retrivedData.json()['BEAAPI']['Results']['Data'])  #TODO: check this works
         
        output = {'dataFrame':df_output}
        
        if outputFormat == "tablePretty":
            df_output['LineNumber'] = pd.to_numeric(df_output['LineNumber'])
            df_output['DataValue'] = pd.to_numeric(df_output['DataValue'])
            
            meta = df_output.drop(['DataValue', 'TimePeriod'], axis=1).drop_duplicates()
            meta = meta.set_index(['LineNumber', 'SeriesCode', 'LineDescription']).reset_index()
            
            df_output = df_output[['LineNumber', 'SeriesCode', 'LineDescription', 'DataValue', 'TimePeriod']]
            df_output = pd.pivot_table(df_output, index=['LineNumber', 'SeriesCode', 'LineDescription'], columns='TimePeriod', values='DataValue', aggfunc='first')
            
            output = {'dataFrame':df_output,'metadata':meta}
            
        return(output)
    
    def _getCode(self,query):
        #general code to all drivers:
        try:
            url        = query['url']
            apiKeyPath = self._connectionInfo.userSettings["ApiKeysPath"]
        except:
            url         = " incomplete connection information "
            apiKeyPath = " incomplete connection information "

        baseCode = _getBaseCode([url,apiKeyPath])
        
        #specific code to this driver:
        queryClean = query
        queryClean['url'] = 'url'
        queryClean['params']['UserID'] = 'key'
        
        
        queryCode = '''
query = {}
retrivedData = requests.get(**query)

dataFrame =  pd.DataFrame( retrivedData.json()['BEAAPI']['Results']['Dataset'] ) #replace json by xml if this is the request format
        '''.format(json.dumps(queryClean))
        
        queryCode = queryCode.replace('"url": "url"', '"url": url')
        queryCode = queryCode.replace('"UserID": "key"', '"UserID": key')
        
        return(baseCode + queryCode)
    
    def clipcode(self):
        _clipcode(self)
    
    def _driverMetadata(self):
        self.metadata =     [{
            "displayName":"List of Datasets",
            "method"     :"datasetlist",   #Name of driver main function - run with getattr(data,'datasetlist')()
            "params"     :{},
        }]


class getGetParameterList():
    def __init__(self,baseRequest={},connectionParameters={},userSettings={}):
        '''
          the baseRequest contains user Key, url of datasource, and prefered output format (JSON vs XML)
        '''
        self._baseRequest = _getBaseRequest(baseRequest,connectionParameters,userSettings) 
        self._lastLoad    = {}  #data stored here to asist other function as clipboard
    
    def getParameterList(self,
        datasetname,
        payload        = {'method': 'GetParameterList'},
        verbose        = False
    ):
        '''
            User only need to specify the NIPA tableName, other parameters are defined by default.  Year (set to X) and Frequency (set to Q)
            can be redefined with payload = {Year = 1990, Frequency = 'A'}, for example.
            
            payload - will override the default
            
            outputFormat - table, tablePretty will return tables (the latter separates the metadata and pivots the table to index x time).
                           Else, returns the JSON, XML.
        '''
        # TODO: put the payload ={} all data in lowercase, else may repeat the load (say frequency=A and Frquency = Q will load A and Q)
        # load user preferences defined in userSettings, use suggested parameters, override w fun entry
        query = self._baseRequest
        query['params'].update({'datasetname':datasetname})
        query['params'].update(payload)
        
        retrivedData = requests.get(**query) 
        output       = self._cleanOutput(query,retrivedData) #a dict of a df or df and meta (tablePretty)
        
        if verbose == False:
            self._lastLoad = output['dataFrame']
            return(output['dataFrame'])
        else:
           output['code']    = self._getCode(query)
           output['request'] = retrivedData
           self._lastLoad = output
           return(output)       
    
    def _cleanOutput(self,query,retrivedData):
        if query['params']['ResultFormat'] == 'JSON':
            df_output =  pd.DataFrame(retrivedData.json()['BEAAPI']['Results']['Parameter'])
        else:
            df_output =  pd.DataFrame(retrivedData.json()['BEAAPI']['Results']['Parameter'])  #TODO: check this works
         
        output = {'dataFrame':df_output}
                    
        return(output)
    
    def _getCode(self,query):
        #general code to all drivers:
        try:
            url        = query['url']
            apiKeyPath = self._connectionInfo.userSettings["ApiKeysPath"]
        except:
            url         = " incomplete connection information "
            apiKeyPath = " incomplete connection information "

        baseCode = _getBaseCode([url,apiKeyPath])
        
        #specific code to this driver:
        queryClean = query
        queryClean['url'] = 'url'
        queryClean['params']['UserID'] = 'key'
        
        
        queryCode = '''
query = {}
retrivedData = requests.get(**query)

dataFrame =  pd.DataFrame( retrivedData.json()['BEAAPI']['Results']['Dataset'] ) #replace json by xml if this is the request format
        '''.format(json.dumps(queryClean))
        
        queryCode = queryCode.replace('"url": "url"', '"url": url')
        queryCode = queryCode.replace('"UserID": "key"', '"UserID": key')
        
        return(baseCode + queryCode)
    
    def clipcode(self):
        _clipcode(self)
    
    def _driverMetadata(self):
        self.metadata =     [{
            "displayName":"Parameter of Dataset",
            "method"     :"GetParameterList",   #Name of driver main function - run with getattr(data,'datasetlist')()
            "params"     :{},
        }]

class getGetParameterValues():
    def __init__(self,baseRequest={},connectionParameters={},userSettings={}):
        '''
          the baseRequest contains user Key, url of datasource, and prefered output format (JSON vs XML)
        '''
        self._baseRequest = _getBaseRequest(baseRequest,connectionParameters,userSettings) 
        self._lastLoad    = {}  #data stored here to asist other function as clipboard
    
    def getParameterValues(self,
        datasetName,
        parameterName,         
        payload        = {'method': 'getParameterValues'},
        verbose        = False
    ):
        '''
            User only need to specify the NIPA tableName, other parameters are defined by default.  Year (set to X) and Frequency (set to Q)
            can be redefined with payload = {Year = 1990, Frequency = 'A'}, for example.
            
            payload - will override the default
            
            outputFormat - table, tablePretty will return tables (the latter separates the metadata and pivots the table to index x time).
                           Else, returns the JSON, XML.
        '''
        # TODO: put the payload ={} all data in lowercase, else may repeat the load (say frequency=A and Frquency = Q will load A and Q)
        # load user preferences defined in userSettings, use suggested parameters, override w fun entry
        query = self._baseRequest
        query['params'].update({'datasetname':datasetName})
        query['params'].update({'parameterName':parameterName})
        query['params'].update(payload)
        
        retrivedData = requests.get(**query) 
        output       = self._cleanOutput(query,retrivedData) #a dict of a df or df and meta (tablePretty)
        
        if verbose == False:
            self._lastLoad = output['dataFrame']
            return(output['dataFrame'])
        else:
           output['code']    = self._getCode(query)
           output['request'] = retrivedData
           self._lastLoad = output
           return(output)       
    
    def _cleanOutput(self,query,retrivedData):
        if query['params']['ResultFormat'] == 'JSON':
            df_output =  pd.DataFrame(retrivedData.json()['BEAAPI']['Results']['ParamValue'])
        else:
            df_output =  pd.DataFrame(retrivedData.json()['BEAAPI']['Results']['ParamValue'])  #TODO: check this works
         
        output = {'dataFrame':df_output}
                    
        return(output)
    
    def _getCode(self,query):
        #general code to all drivers:
        try:
            url        = query['url']
            apiKeyPath = self._connectionInfo.userSettings["ApiKeysPath"]
        except:
            url         = " incomplete connection information "
            apiKeyPath = " incomplete connection information "

        baseCode = _getBaseCode([url,apiKeyPath])
        
        #specific code to this driver:
        queryClean = query
        queryClean['url'] = 'url'
        queryClean['params']['UserID'] = 'key'
        
        
        queryCode = '''
query = {}
retrivedData = requests.get(**query)

dataFrame =  pd.DataFrame( retrivedData.json()['BEAAPI']['Results']['Dataset'] ) #replace json by xml if this is the request format
        '''.format(json.dumps(queryClean))
        
        queryCode = queryCode.replace('"url": "url"', '"url": url')
        queryCode = queryCode.replace('"UserID": "key"', '"UserID": key')
        
        return(baseCode + queryCode)
    
    def clipcode(self):
        _clipcode(self)
    
    def _driverMetadata(self):
        self.metadata =     [{
            "displayName":"Parameter of Dataset",
            "method"     :"GetParameterList",   #Name of driver main function - run with getattr(data,'datasetlist')()
            "params"     :{},
        }]

if __name__ == '__main__':
    #from datapungibea.drivers import getNIPA
    #v = getNIPA()
    #v.NIPA('T10101')
    
    #from datapungibea.drivers import getNIPA #getDatasetlist
    #v = getNIPA() #getDatasetlist()
    #print(v.NIPA('T10101',verbose=True))
    ##print(v._lastLoad['code'])

    from datapungibea.drivers import getGetParameterList #getDatasetlist
    v = getGetParameterList()
    print(v.getParameterList('NIPA',verbose = True)['code'])

    from datapungibea.drivers import getGetParameterValues #getDatasetlist
    v = getGetParameterValues()
    print(v.getParameterValues('NIPA','TableID'))