import pandas as pd
import requests

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
    print(NIPA('T10101'))