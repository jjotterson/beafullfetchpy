import pandas as pd              #
import numpy as np               # 
import requests as rq            # get json
import bs4 as bs                 # scraping websites
import urllib.request            # work/connect to url    
import re                        # regular expression
#import datetime
#from CFGBeaHist import *        # get basic config.


cfg = {
  'beaUrl'   : 'https://apps.bea.gov/',
  'histUrl'  : 'https://apps.bea.gov/histdata/',
  'NIPAHistUrl'  : 'https://apps.bea.gov/histdata/histChildLevels.cfm?HMI=7',
}

def NIPAHistUrlOfQYVintage( 
        NIPAHistUrl  = 'https://apps.bea.gov/histdata/histChildLevels.cfm?HMI=7', #location of table of historical databases
        histUrl      = 'https://apps.bea.gov/histdata/',                          #missing part of the historical database https 
        replaceSpaceWith = "%20"
    ):
    '''
     Table of the url of the Quarter Year Vintage Data

     Inputs:
       NIPAUrl a string poiting to the site of NIPA historical data.  For each quater, vintage, release data,
     it gives a link to the historical NIPA data (missing the mainUrl part)
     
     replaceSpaceWith %20 is because certain pages will load open without this correction
     
     Output:
       Returns a table listing the name, vintage, time units of the historical data and their http links 
       These are not links to data, but a place that points to excel tables (the output of interest).
    '''    
    #connect to main BEA Historical table and get tables
    source = urllib.request.urlopen( NIPAHistUrl ).read()
    soup = bs.BeautifulSoup( source, 'lxml' )
    htable = soup.table
    
    #get the main table and standardize its entries ('1. Advance' vs 'Advance' in lines etc)
    dfUrlQYVintage = pd.read_html( str( htable ), header = 1)[1]  #get the table entries, could go to the html directly.
    dfUrlQYVintage.columns = ['yearQuarter','vintage','releaseDate']
    dfUrlQYVintage['vintage'] = dfUrlQYVintage['vintage'].apply( lambda x: re.sub('.\. ','',x) )  
    dfUrlQYVintage['vintage'] = dfUrlQYVintage['vintage'].apply( lambda x: re.sub('Final','Third',x) )
    dfUrlQYVintage['vintage'] = dfUrlQYVintage['vintage'].apply( lambda x: re.sub('Preliminary','Second',x) )
    dfUrlQYVintage['vintage'] = dfUrlQYVintage['vintage'].apply( lambda x: re.sub('Initial','Advance',x) )
    
    #get hrefs from the loaded table
    links = []
    for link in htable.table.find_all('tr'):
        #links.append(link)
        aux = link.a        
        if aux != None:
            links.append(aux.get('href'))
    
    dfUrlQYVintage['vintageLink'] = links
    dfUrlQYVintage['vintageLink'] = dfUrlQYVintage['vintageLink'].apply( lambda x: (histUrl+x).replace(" ", replaceSpaceWith) )  #appends the main url bc the link given misses this part
    
    return( dfUrlQYVintage )

def NIPAHistUrlOfQYVintageTypeSection( 
          LineOfdfUrlQYVintage,                    #a line of the table output of  NIPAHistUrlOfQYVintage
          beaUrl = 'https://apps.bea.gov/'      
    ):
    '''
       From the url of quarter year vintage data (see NIPAHistUrlOfQYVintage) make a table of the url of the 
        quarter year vintage type (main/underlying etc) and section
       The output urls point to excel tables.        
    '''  
       
    source = urllib.request.urlopen( LineOfdfUrlQYVintage['vintageLink'] ).read()
    soup   = bs.BeautifulSoup( source, 'lxml' )
    htable = soup.body.find_all('table')
    
    outValues = []
    for table in htable: #this will skip tables that don't have headings
      try: 
        dftab =  pd.read_html( str(table) , header = 1 )[0]
        auxlink = list( map( lambda x: x.get('href'), table.find_all('a') ))
        #links.append( [auxlink] )
        dftab['excelLink'] = list(map(lambda x: beaUrl+x ,auxlink))    #here replace " " with %20
        if not dftab.empty:
          for key in LineOfdfUrlQYVintage: 
              dftab[key] = LineOfdfUrlQYVintage[key] 
          outValues.append(dftab)
      except:
        pass
     
    if len(outValues) == 3:      #Varies a lot, some years have three tables (main, FA / Millions, underlying, other years 1 (main)                                             
      output = dict(zip( ['main','FAorMillions','underlying'], outValues ))
    elif len(outValues) == 2:
      output = dict(zip( ['main','underlying'], outValues ))
    else:
      output = dict(zip( ['main'], outValues ))
    
    return(output)


def getAllLinksToHistTables(readSaved = False):
    '''
      Concatenate the tables of the excel data urls.

      If readSaved = True, will read the pre-saved data
    '''
    
    if readSaved == True:
      urlOfExcelTables = pd.read_json('/Users/jjotterson/Dropbox/Projects/PythonPackages/beafullfetchpy/beafullfetchpy/data/NIPAUrlofExcelHistData.json',orient="records")  #TODO: fix this, need to include Manifest.in
      return( urlOfExcelTables )
     
    dfUrlQYVintage = NIPAHistUrlOfQYVintage()
    
    urlOfExcelTables = pd.DataFrame()
    for line in range(len(dfUrlQYVintage)):
        LineOfdfUrlQYVintage = dfUrlQYVintage.to_dict('records')[line]
        out = NIPAHistUrlOfQYVintageTypeSection( LineOfdfUrlQYVintage )
        
        for type in out:
          out[type]['type'] = type
        
        urlOfExcelTables = pd.concat([urlOfExcelTables] + list(out.values()),sort=False)
       
    return( urlOfExcelTables )

def getNIPADataFromListofLinks( tableOfLinks , asJson = False):
    '''
      
    '''
    nipaData = tableOfLinks.to_dict(orient='records')
    count = 0 
    for row in nipaData:
        link = row['excelLink']
        if asJson == False:
            try:
                row['data'] = pd.read_excel(link.replace(" ","%20"), sheet_name=None)
            except:
                try:
                    row['data'] = pd.read_excel(link.replace(" ","%20"), sheet_name=None) 
                except:   
                    print("cannot read: " + link)
        else:
            try:
                row['data'] = pd.read_excel(link.replace(" ","%20"), sheet_name=None).to_dict(orient='records')
            except:
                try: 
                    row['data'] = pd.read_excel(link.replace(" ","%20"), sheet_name=None).to_dict(orient='records')
                except:
                    print('cannot read: ' + link)
        count = count + 1    
        if count%250 == 0:
          print( 'got item '+ str(count) )
    return( nipaData )

def getHistTable( tableName, yearQuarter, vintage = "Third", timeUnit = "Q", cfg = cfg ):
    sectionNum = tableName[1]
    r = re.compile( tableName.replace('T','') + '.*' + timeUnit )  #will search for sheet names with this regex.
    maindf  = NIPAHistUrlOfQYVintage( cfg['NIPAHistUrl'], cfg['histUrl'] )
    dfline  = maindf[ (maindf.yearQuarter == yearQuarter) & (maindf.vintage == vintage) ]
    excelLinks = NIPAHistExcelLinks( dfline , cfg['beaUrl'] )['main']
    dfExcelSelected = excelLinks[ excelLinks.Title.str.contains('Section {}'.format(sectionNum)) ]
    
    output = pd.DataFrame()
    if dfExcelSelected.empty:
       print("Table does not exist in time period!")
       return( output )
    
    #for now, will only get the Section x data, not the Section x (Pre) (pre 1969) that might exist
    #to do: when (pre) exist open and concatenate it.
    exLink = excelLinks[ excelLinks.Title == 'Section {}'.format(sectionNum) ].excelLink.tolist()[0]
    excelAll = pd.read_excel( exLink, None)  #get all tables
    
    table = excelAll[ list( filter( r.match, excelAll.keys()) )[0] ]
    
    #get metadata (date range for now):
    #r2 = re.compile('.* data from .* To .*'.lower())
    #vv = table.iloc[:,0].astype(str).str.lower().tolist()
    #dates = list( filter( lambda x: r2.match(x), vv  ) )[0]
    
    #clean up the table.
    table = table[ table.iloc[:,2].notna() ].iloc[:,2:]
    table = table.rename(columns={ table.columns[0]: 'variable' }).set_index('variable')
    table = table.apply(pd.to_numeric, errors='coerce')
    table = table.dropna( how = 'all' ) 
    
    #put dates
    Nobs = table.shape[1]
    if timeUnit == 'Q':
      ffreq = 'QS' #else will end a quarter before...
    
    dateRange = list( pd.date_range(end=yearQuarter.replace(', ',''), periods=Nobs,freq=ffreq ) )
    dates = pd.PeriodIndex( dateRange, freq = timeUnit)
    
    table.columns = dates
    return(table)


#  datetime.timedelta( month = 1 )

def getAndSaveData(range,filename,excelTables, quiet = True):
    tableRange = excelTables.iloc[range]
    
    fullnipaData = getNIPADataFromListofLinks(tableRange)

    serialized = pickle.dumps(fullnipaData)
        
    with open(filename,'wb') as file_object:
        file_object.write(serialized)

    if quiet == False:
        print( "finished loading!")
        print(range)

def formatBeaRaw( beaHistRaw )

if __name__ == '__main__':
    #dfUrlQYVintage = NIPAHistUrlOfQYVintage()
    #LineOfdfUrlQYVintage = dfUrlQYVintage.to_dict('records')[line]
    #out = NIPAHistUrlOfQYVintageTypeSection( LineOfdfUrlQYVintage )
    #
    #excelTables = getAllLinksToHistTables()
    #excelTables = excelTables[['index', 'yearQuarter', 'vintage', 'Title', 'Details', 'type', 'releaseDate', 'vintageLink', 'excelLink']]
    #excelTables.to_json('data/NIPAUrlofExcelHistData.json',orient="records")  #todo: fix this file pointer.
    excelTables = getAllLinksToHistTables(readSaved=True)
    import sys
    import pickle



    for i in range(int(sys.argv[1]),int(sys.argv[1])+1000):
        rr = range( i, i+1 )
        filename = 'beafullfetchpy/beaData/beaHist' + str(i)
        getAndSaveData(rr, filename, excelTables)
        i = i + 1
        if i % 100 == 1:
            print( i )


    #rr = range( int(sys.argv[1]), int(sys.argv[2]) )
    #filename = sys.argv[3]
    #getAndSaveData(rr,filename,excelTables)

    
    #fullnipaData = getNIPADataFromListofLinks(excelTables)
    #
    #
    #import pickle 
    #serialized = pickle.dumps(fullnipaData)
    #filename = 'serialized.native'
    #
    #with open(filename,'wb') as file_object:
    #    file_object.write(serialized)
    #
    #
    filename = 'beafullfetchpy/beaData/beaHist1'
    with open(filename,'rb') as file_object:
        raw_data = file_object.read()


    beaHistRaw = pickle.loads(raw_data)



raw = beaHistRaw[0]['data']
formatedData = []
for x in raw:

    # Data
    if x not 'Contents':
      Results = {}
      table = raw[x]
      #
      Results['Notes'] = {
          'NoteRef': x,     #TODO remove -A, Qtr, -Q etc -M
          'NoteText': " - ".join( [table.columns[0]] + table.iloc[:5,0].to_list() )
      }
      #main data and footnote comments
      dataTab = table.iloc[7:]  #TODO: check when quarters are indicated in the next line
      #column names
      colNames = table.iloc[6].to_list()
      colNames[1] = 'LineDescription'
      colNames[2] = 'SeriesCode'
      dataTab.columns = colNames
      dataTab.reset_index(drop=True,inplace=True)

      #store footnotes on the notes part of the results
      footnotes = dataTab.loc[dataTab['LineDescription'].isnull() & dataTab['Line'].notnull()].iloc[:, 0].to_list()
      Results['Notes']['Footnotes'] = dict(zip(range(1,1+len(footnotes)),footnotes))
      dataTab = dataTab.loc[dataTab['LineDescription'].notnull()]

      #include graph structure:
      indents = dataTab.LineDescription.map(lambda x: len(x) - len(x.lstrip(' '))).to_list()
      dataTab.insert(3, 'Indentations', indents)

      #save table structure
      Results['Notes']['TableStructure'] = dataTab.reset_index().iloc[:,:5].fillna('').to_dict('list')

      #clean up table
      #remove subsection headings (these have no data)
      dataTab = dataTab.loc[dataTab['SeriesCode'].notna()]

      dataTab.LineDescription = dataTab.LineDescription.map(lambda x: re.sub('\\\\.\\\\', '', x) )
      dataTab.LineDescription = dataTab.LineDescription.map(lambda x: re.sub('[\w]*:','',x))  #removes Less:, Equals:...
      dataTab.LineDescription = dataTab.LineDescription.map(lambda x : x.lstrip(" "))  #do this last to avoid the case when space is created

      #reshape data and save
      mindex = pd.MultiIndex.from_frame(dataTab.iloc[:, :4])



