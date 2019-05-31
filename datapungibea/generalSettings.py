'''
  datapungi.generalSettings
  ~~~~~~~~~~~~~~~~~~

  General information on the data source (with disclaimer for accuracy), and 
  general information on the package itself - this is to be passed to 
  a GUI.  Also, this gets updated to include information on the 
  individual methods used to get databases of the datasource
'''

import datapungibea.utils as utils

class generalSettings():
    def __init__(self,sessionParameters={},userSettings={}):
        ''' 
         __sessionParameters  - API key and the url (most used) of the datasource
           entry should look like:
           {'key': 'your key', 'description': 'BEA data', 'address': 'https://apps.bea.gov/api/data/'}
         __datasourceOverview - a quick description of the datasource and its license
         __packageMetadata - basic info on the package - to be used in a GUI or catalog of 
            methods that read data.  Also, "databases" will get automaticall updated with
            info on the methods that get specific dataset from the datasource.  A typical 
            entry should look like:
            {
                 "displayName":"List of Datasets",
                 "method"     :"datasetlist",   #NOTE run with getattr(data,'datasetlist')()
                 "params"     :{},              #No parameters in this case.
            }
        '''
        #Load, for example, API Key and the (most used) path to the datasource
        self.__getSessionParameters(sessionParameters,userSettings)
        
        self.__datasourceOverview = '''
         Userguides:
          https://apps.bea.gov/api/_pdf/bea_web_service_api_user_guide.pdf
          https://www.bea.gov/tools/   or  https://apps.bea.gov/API/signup/index.cfm
         
          Basically, there are three types of meta: 
            (1) GETDATASETLIST      top level, get the name of all tables.  
            (2) GetParameterList    given a table, what parameters it needs to download (eg. NIPA)
            (3) GetParameterValues  given a parameter of a table, which values you can choose. (eg. TableID)
         
         Sample python code (getting the list of datasets):
         
            import requests 
            payload = {
                'UserID':  ENTER YOUR BEA API Key Here, 
                'method': 'GETDATASETLIST',
                'ResultFormat': "JSON"
            }
            beaDatasets = requests.get( 'https://apps.bea.gov/api/data/', params = payload )
        
         Licenses (always check with the data provider):
            Data used is sourced from the Bureau of Economic Analysis 
            As stated on the Bureau of Economic Analysis website: 
            - Unless stated otherwise, information published on this site is in the public 
               domain and may be used or reproduced without specific permission. 
            - As a U.S. government agency, BEA does not endorse or recommend any 
              commercial products or services.                                            
            - Any reference or link to the BEA Web site must not contain information 
              that suggests an endorsement or recommendation by BEA.                  
            For more information, see: 
             https://www.bea.gov/help/guidelines-for-citing-bea  
        '''   
           
        self.__packageMetadata = {
            "name":             "datapungibea",
            "loadPackageAs" :   "dpbea",
            "apiClass":         "data",
            "displayName":      "BEA",
            "description":      "Acess data from Bureau of Economic Analysis (BEA)",
            "databases":        [
                {
                 "displayName":"List of Datasets",
                 "method"     :"datasetlist",   #NOTE run with getattr(data,'datasetlist')()
                 "params"     :{},
                },
                {
                 "displayName":"NIPA",
                 "method"     :"NIPA",   #NOTE run with getattr(data,'datasetlist')()
                 "params"     :{'Year':'X','Frequency':'Q'}, #Parameters and default options.
                },
                ],
         }              
           
    
    def __getSessionParameters(self,sessionParameters={},userSettings={}):
        if not sessionParameters == {}:
           self.__getSessionParameters = sessionParameters
           return 
        
        if not userSettings == {}:
            self.__sessionParameters =  utils.getKey(userSettings=userSettings) 
            return
        
        self.__sessionParameters = utils.getKey()





'''

                {
                 "displayName":"List of Datasets",
                 "method"     :"datasetlist",   #NOTE run with getattr(data,'datasetlist')()
                 "params"     :{},
                },
                {
                 "displayName":"NIPA",
                 "method"     :"NIPA",   #NOTE run with getattr(data,'datasetlist')()
                 "params"     :{'Year':'X','Frequency':'Q'}, #Parameters and default options.
                },
             ],
        }
'''