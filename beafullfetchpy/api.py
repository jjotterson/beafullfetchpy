import pandas as pd
import requests
from beafullfetchpy import configFuns as cfgf


try:
    from beafullfetchpy import config as userConfig
except:
    print(
        "Run userPreferences to save API Key and prefered format (XML vs JSON) to memory \n" +
        "  else Run in session or add to script \n    userOptions = {'UserID': 'enter key here', 'ResultFormat': 'JSON' } \n" + 
        "  else include API key and prefered format in each function call")  
        #TODO: do this as class - so that can add this to object atribute, not define on brackground userOptions = {} but bff.userOptions ==

def basePayload(payload):
    payload = {x: userConfig.userOptions[x]
               for x in ['UserID', 'ResultFormat']}
    payload.update(settings)

class data():
    def __init__(self,userConfig = {}, userKeys = {}):
      self.meta()       
      try:                                      #TODO: replace by getters and setters - use the set function in configFuns as a setter 
          if userConfig == {}:
              self._userConfig = cfgf.getConfig()   
          if userKeys == {}:
              self._userKeys   = cfgf.getKey()     
      except:
          print('could not load user BEA API Key and other key parameters')
      self._query = {
          'url'   : self._userKeys['address'],
          'params':    dict(UserID=self._userKeys['key'],ResultFormat=self._userConfig["ResultFormat"])
      }
    
    def datasetlist(self,verbose=False):
        query = self._query
        query['params'].update({'method':'GETDATASETLIST'})
        
        retrivedData = requests.get(**query)
        
        if query['params']['ResultFormat'] == 'JSON':
            df_output =  pd.DataFrame( retrivedData.json()['BEAAPI']['Results']['Dataset'] )
        else:
            df_output =  pd.DataFrame( retrivedData.xml()['BEAAPI']['Results']['Dataset'] )  #TODO: check this works
        
        if verbose == False:
            return(df_output)
        else:
            code = '''
              import requests
              import json    
              
              #(1) get user API key (not advised but can just write key and url in the file)
              #    file should contain: {{"BEA":{{"key":"YOUR KEY","address":"https://apps.bea.gov/api/data/"}}}}
              
              apiKeysFile = "{}"
              with open(apiKeysFile) as jsonFile:
                 apiInfo = json.load(jsonFile)
                 url,key = apiInfo["BEA"]["address"], apiInfo["BEA"]["key"]       
            '''.format(self._userConfig["ApiKeysPath"])
            output = dict(dataFrame = df_output, request = retrivedData, code = code)  
            return(output)  
    
    def help(self):
        BEAAPIhelp = '''
         Userguides:
          https://apps.bea.gov/api/_pdf/bea_web_service_api_user_guide.pdf
          https://www.bea.gov/tools/   or  https://apps.bea.gov/API/signup/index.cfm
         
          Basically, there are three types of meta: 
            (1) GETDATASETLIST      top level, get the name of all tables.  
            (2) GetParameterList    given a table, what parameters it needs to download (eg. NIPA)
            (3) GetParameterValues  given a parameter of a table, which values you can choose. (eg. TableID)
        '''   
        print( BEAAPIhelp )
    
    def meta(self):  #TODO: write as setter
        self.metadata = {
            "name":"beafullfetchpy",
            "apiClass":"data",
            "displayName":"BEA",
            "description":"Bureau of Economic Analysis (BEA)",
            "datasets":[
                {
                 "displayName":"Datasets",
                 "method":"datasetlist"   #NOTE run with getattr(data,'datasetlist')()
                },
             ],
        }
  
        


def NIPA(
    tableName,
    payload={'method': 'GETDATA', 'DATABASENAME': 'NIPA', 'datasetname': 'NIPA', 'Year': 'X', 'Frequency': 'Q', 'ParameterName': 'TableID'},
    outputFormat="tablePretty",
    beaHttp='https://apps.bea.gov/api/data/',
    tryFrequencies=False
   ):
    '''
      User only need to specify the NIPA tableName, other parameters are defined by default.  Year (set to X) and Frequency (set to Q)
      can be redefined with payload = {Year = 1990, Frequency = 'A'}, for example.
      
      payload - will override the default
      
      outputFormat - table, tablePretty will return tables (the latter separates the metadata and pivots the table to index x time).
                     Else, returns the JSON, XML.
      
      beaHttp - the addess of the BEA API
    '''
    # TODO: put the payload ={} all data in lowercase, else may repeat the load (say frequency=A and Frquency = Q will load A and Q)
    # load user preferences defined in userConfig, use suggested parameters, override w fun entry
    payloadValues = {x: userConfig.userOptions[x] for x in ['UserID', 'ResultFormat']}
    payloadValues.update({'TABLENAME': tableName})
    payloadValues.update(payload)
    
    # TODO: try loading different frenquencies if no return
    #
    nipa = requests.get(beaHttp, params=payloadValues)
    
    # output format
    if outputFormat == "table":
        # TODO: check if xml or json
        return(pd.DataFrame(nipa.json()['BEAAPI']['Results']['Data']))
    elif outputFormat == "tablePretty":
        table = pd.DataFrame(nipa.json()['BEAAPI']['Results']['Data'])
        table['LineNumber'] = pd.to_numeric(table['LineNumber'])
        table['DataValue'] = pd.to_numeric(table['DataValue'])
        
        meta = table.drop(['DataValue', 'TimePeriod'], axis=1).drop_duplicates()
        meta = meta.set_index(['LineNumber', 'SeriesCode', 'LineDescription']).reset_index()
        
        table = table[['LineNumber', 'SeriesCode', 'LineDescription', 'DataValue', 'TimePeriod']]
        table = pd.pivot_table(table, index=['LineNumber', 'SeriesCode', 'LineDescription'], columns='TimePeriod', values='DataValue', aggfunc='first')
        
        return({'metadata': meta, 'table': table})
    else:
        return(nipa)



if __name__ == '__main__':
    
    d = data()
    print(d)
    #print(NIPA('T10101'))