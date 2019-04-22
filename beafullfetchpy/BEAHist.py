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
  'mainUrl'  : 'https://apps.bea.gov/histdata/',
  'NIPAUrl'  : 'https://apps.bea.gov/histdata/histChildLevels.cfm?HMI=7',
}

def NIPAHistMain( NIPAUrl, mainUrl ):
    '''
     NIPAUrl a string poiting to the site of NIPA historical data.  For each quater, vintage, release data, it has a link to the historical NIPA data
     mainUrl the URL of the BEA historical data site.
     
     Returns a df with of all quarter, vintage, release data, link
    '''    
    #connect to main BEA Historical table and get tables
    source = urllib.request.urlopen( NIPAUrl ).read()
    soup = bs.BeautifulSoup( source, 'lxml' )
    htable = soup.table
    
    #get the main table and standardize its entries ('1. Advance' vs 'Advance' in lines etc)
    dfMain = pd.read_html( str( htable ), header = 1)[1]  #get the table entries, could go to the html directly.
    dfMain.columns = ['yearQuarter','vintage','releaseDate']
    dfMain['vintage'] = dfMain['vintage'].apply( lambda x: re.sub('.\. ','',x) )  
    dfMain['vintage'] = dfMain['vintage'].apply( lambda x: re.sub('Final','Third',x) )
    dfMain['vintage'] = dfMain['vintage'].apply( lambda x: re.sub('Preliminary','Second',x) )
    
    #get hrefs from the loaded table
    links = []
    for link in htable.table.find_all('tr'):
        #links.append(link)
        aux = link.a
        if aux != None:
            links.append(aux.get('href'))
    
    dfMain['vintageLink'] = links
    dfMain['vintageLink'] = dfMain['vintageLink'].apply( lambda x: mainUrl+x)  #appends the main url bc the link given misses this part
    
    return( dfMain )

def NIPAHistExcelLinks( dfline, beaUrl ):
  
  dataSpecs = dfline.to_dict('records')[0]  #get the first occurance of dfline (presumable a line already) 
     
  source = urllib.request.urlopen( dataSpecs['vintageLink'] ).read()
  soup   = bs.BeautifulSoup( source, 'lxml' )
  htable = soup.body.find_all('table')
  
  outValues = []
  for table in htable: #this will skip tables that don't have headings
    try: 
      dftab =  pd.read_html( str(table) , header = 1 )[0]
      auxlink = list( map( lambda x: x.get('href'), table.find_all('a') ))
      #links.append( [auxlink] )
      dftab['excelLink'] = list(map(lambda x: beaUrl+x,auxlink))
      if not dftab.empty:
        for key in dataSpecs: 
            dftab[key] = dataSpecs[key] 
        outValues.append(dftab)
    except:
      pass
   
  output = dict(zip( ['main','uderlying'], outValues ))
  
  return(output)


maindf = NIPAHistMain( cfg['NIPAUrl'], cfg['mainUrl'] )
dfline = maindf.loc[0]
out = NIPAHistExcelLinks( dfline, cfg['beaUrl'] )



def getHistTable( tableName, yearQuarter, vintage = "Third", timeUnit = "Q", cfg = cfg ):
  sectionNum = tableName[1]
  r = re.compile( tableName.replace('T','') + '.*' + timeUnit )  #will search for sheet names with this regex.
  maindf  = NIPAHistMain( cfg['NIPAUrl'], cfg['mainUrl'] )
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


  datetime.timedelta( month = 1 )


dfline.to_dict( )