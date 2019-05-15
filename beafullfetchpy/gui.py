import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import sys
import os
import subprocess
import json
import re
import csv
import pandas as pd

class beaGuiModel:  
    def __init__(self,exitProcess=0):  
        self.getLicenses()
        self.getHelp()
        self.getHelpBEAAPI()
    def set_exitProcess(self, exitProcess=0):
        self.exitProcess = exitProcess
    def getLicenses(self):
        self.licenses = licenses()
    def getHelp(self):
        self.help = helpIcons()
    def getHelpBEAAPI(self):
        self.helpBEAAPI = helpBEAAPI()

def licenses():       
    licenseDict = '''
   beafullfetchpy is a python program written to get data from the Bureau of Economic 
   Analysis (BEA) in a programmatic way (ie, via APIs). The package was written 
   by James Otterson - this package is distributed in the hope that it may be 
   useful to some. The usual disclaimers apply (downloading and installing this 
   software is at your own risk, and no support or guarantee is provided, I do not 
   take liability and so on), but please let me know if you have any problems, 
   suggestions, comments, etc.. 
   
   Licenses:
    \u2022 Data used is sourced from the Bureau of Economic Analysis 
      As stated on the Bureau of Economic Analysis website: 
      - Unless stated otherwise, information published on this site is in the public 
         domain and may be used or reproduced without specific permission. 
      - As a U.S. government agency, BEA does not endorse or recommend any 
        commercial products or services.                                            
      - Any reference or link to the BEA Web site must not contain information 
        that suggests an endorsement or recommendation by BEA.                  
      For more information, see: 
       https://www.bea.gov/help/guidelines-for-citing-bea  
    
    \u2022 Font Awesome Free License can be found here:  
      https://fontawesome.com/license/free 
    
    \u2022 beafullfetchpy  
      This package is under the MIT Free license
''' 
    return(licenseDict)

def helpIcons():
    helpText = '''
   \u2022 Database Icon - use to navigate the BEA databases
   \u2022 Add Icon  - use to restrict the dataset
   \u2022 Download icon - use to save the selected data to a drive
   \u2022 Load icon - use it to load the data to the current python sessions running the app
   \u2022 Code icon - use it to get the code that can be used to load the data in a python section
   \u2022 Settings icon - use it to manage your API Keys
'''
    return(helpText)

def helpBEAAPI():
    helpBEAAPI = '''
    The userguide of the of BEA API can be found in:

    https://apps.bea.gov/api/_pdf/bea_web_service_api_user_guide.pdf
    
    To access it and create an API Key, see:
    
    https://www.bea.gov/tools/   or  https://apps.bea.gov/API/signup/index.cfm
    
    Metadata:
    there are types of meta: 
      (1) GETDATASETLIST      top level, get the name of all tables.  
      (2) GetParameterList    given a table, what parameters it needs to download (eg. NIPA)
      (3) GetParameterValues  given a parameter of a table, which values you can choose. (eg. TableID of a NIPA table)

    Sample python code (getting the list of datasets):
    
    import requests 
    payload = {
        'UserID':  ENTER YOUR BEA API Key Here, 
        'method': 'GETDATASETLIST',
        'ResultFormat': "JSON"
    }
    beaDatasets = requests.get( 'https://apps.bea.gov/api/data/', params = payload )

'''
    return(helpBEAAPI)


class beaGuiView(tk.Frame):
    '''
      Fixes the overall geometry of the app.  Note: writing based mainly in pack not grid since the 
      overall shape (vertical or horizontal blocks that fill the whole space) fits this framework better.
    '''
    def __init__(self, model, master=None):
        super().__init__(master)   #TODO: remove and put in control? is this even possible?
        self.model = model         #TODO: maybe mediate all interaction vai Control - no need for this so far
        self.fontsel = "Times"
        self.Appconfigs()
        self.ttkStyles()    #load styling
        # self.create_widgets()
        self.MainContainers()
        self.mainPanel()
        self.sideNav()
        self.master.bind('<Button-1>', self.keep_flat)
    def keep_flat(self,event):       # on click,
        #print(event)
        #print("this is the widget")
        #print(event.widget)
        event.widget.config(relief=tk.FLAT) # enforce an option, TODO: fix error notice "relief, unknown option" when using ttk
        
    def Appconfigs(self, title="BEA Full Data Fetch (beafullfetch)"):
        self.master.title(title)
        # self.master.option_add('*Font','Times')
        self.master.geometry('{}x{}'.format(1300, 850))
    def MainContainers(self):
        # Main containers
        self.frameMain = tk.Frame(
            self.master, width=400, height=50, pady=3, padx=1, bd=2, relief=tk.FLAT,  background='#272822')   
        self.frameSideNav = tk.Frame(
            self.master, width=400, height=50, pady=3, padx=1, bd=2,  background='#48483E')  #rgb 72,72,62
        # layout of the main containers
        #root.grid_rowconfigure(1, weight=1)
        #root.grid_columnconfigure(0, weight=1)
        
        self.frameSideNav.pack(side = tk.LEFT, fill=tk.Y  )
        self.frameMain.pack(side = tk.LEFT, fill=tk.Y  )
        
    def mainPanel(self):
        # top frame widgets
        #
        # Geometry - cfgs and start right panel.
        self.frameMain_left_cfg      = dict(master=self.frameMain,  width=550, height=190,background='#272822')
        self.frameMain_left_packCfg  = dict(side=tk.LEFT, fill = tk.Y)
        self.frameMain_right_cfg     = dict(master=self.frameMain,  width=550, height=190,background='#272822')
        self.frameMain_right_packCfg = dict(side=tk.LEFT, fill = tk.Y)        
        self.frameMain_left = tk.Frame(**self.frameMain_left_cfg)
        self.frameMain_left.pack(**self.frameMain_left_packCfg)
        #
        # Content
        #tk.Label(self.top_left, text="Data Info", font=(self.fontsel, 20), anchor=tk.W, justify=tk.LEFT, fg = 'white',background='#272822' ).grid(row=0,  column=0, sticky='e')
        


    def sideNav(self): #############################################################
        # Summary frame widgets
        # Geometry
        self.sidenav_topframe = tk.Frame(self.frameSideNav,background='#48483E')
        self.sidenav_topframe.pack()
       
        self.sidenav_bottomframe = tk.Frame(self.frameSideNav,background='#48483E')
        self.sidenav_bottomframe.pack(side=tk.BOTTOM)
        #
        btnCfg = dict(anchor=tk.W, relief = tk.FLAT,justify=tk.LEFT, background='#48483E', activebackground='#48483E',activeforeground='white',fg = 'white' )
        btnBaseGrid = dict(column=0, sticky='w',padx = 0, pady=10)
        #top buttons
        self.btn_database = tk.Button(self.sidenav_topframe,    text="Database", **btnCfg )
        self.btn_add      = tk.Button(self.sidenav_topframe,    text="Add",      **btnCfg )
        self.btn_download = tk.Button(self.sidenav_topframe,    text="Download", **btnCfg )
        self.btn_load     = tk.Button(self.sidenav_topframe,    text="Load",     **btnCfg )
        self.btn_code     = tk.Button(self.sidenav_topframe,    text="Code",     **btnCfg )
        self.btn_help     = tk.Button(self.sidenav_topframe,    text="Help",     **btnCfg )
        self.btn_settings = tk.Button(self.sidenav_bottomframe, text="Settings", **btnCfg )
        #geometry:  
        self.btn_database.grid(row=0,  **btnBaseGrid)
        self.btn_add     .grid(row=1,  **btnBaseGrid)    
        self.btn_download.grid(row=2,  **btnBaseGrid)
        self.btn_load    .grid(row=3,  **btnBaseGrid)     
        self.btn_code    .grid(row=4,  **btnBaseGrid)   
        self.btn_help    .grid(row=5,  **btnBaseGrid)    
        self.btn_settings.grid(row=0,  **btnBaseGrid)    
        #image - if error, need to run a case without error, close all windows and then re-run.
        self.img_btn_database = tk.PhotoImage(file = "beafullfetchpy/static/imgs/database-solid.gif")
        self.img_btn_add      = tk.PhotoImage(file = "beafullfetchpy/static/imgs/plus-square-solid.gif")
        self.img_btn_download = tk.PhotoImage(file = "beafullfetchpy/static/imgs/download-solid.gif")
        self.img_btn_load     = tk.PhotoImage(file = "beafullfetchpy/static/imgs/arrow-circle-down-solid.gif")
        self.img_btn_code     = tk.PhotoImage(file = "beafullfetchpy/static/imgs/code-solid.gif")
        self.img_btn_help     = tk.PhotoImage(file = "beafullfetchpy/static/imgs/info-circle-solid.gif")
        self.img_btn_settings = tk.PhotoImage(file = "beafullfetchpy/static/imgs/cog-solid.gif")
        
        self.btn_database.config(image=self.img_btn_database,width="50",height="24" )
        self.btn_add     .config(image=self.img_btn_add     ,width="50",height="24" )
        self.btn_download.config(image=self.img_btn_download,width="50",height="24" )
        self.btn_load    .config(image=self.img_btn_load    ,width="50",height="24" )
        self.btn_code    .config(image=self.img_btn_code    ,width="50",height="24" )
        self.btn_help    .config(image=self.img_btn_help    ,width="50",height="24" )
        self.btn_settings.config(image=self.img_btn_settings,width="50",height="24" )
    
    def settingsPage(self):
        #geometry
        self.frameMain_left_topFrame           = ttk.Frame(master=self.frameMain_left)
        self.frameMain_left_bottomFrame        = ttk.Frame(master=self.frameMain_left)
        self.frameMain_left_bottomFrame_left   = ttk.Frame(master=self.frameMain_left_bottomFrame)
        self.frameMain_left_bottomFrame_right  = ttk.Frame(master=self.frameMain_left_bottomFrame)
        self.frameMain_left_topFrame.pack(side = tk.TOP,fill=tk.X,pady=(0,0))
        self.frameMain_left_bottomFrame.pack(side = tk.TOP,fill=tk.X,pady=(50,0))
        self.frameMain_left_bottomFrame_left.pack(side = tk.LEFT,padx=(0,150))
        self.frameMain_left_bottomFrame_right.pack(side = tk.LEFT)  #TODO: compare to right
        
        #content
        self.frameTitle(self.frameMain_left_topFrame, "Settings",pack=False)
        userConfig = {}
        with open('beafullfetchpy/config/userSettings.json') as jsonFile:
            try:
                userConfig.update(json.load(jsonFile))
            except:
                pass
        try:
            isinstance(userConfig["ApiKeysPath"],str)
        except:
            userConfig["ApiKeysPath"] = ""
        
        ttk.Label(master = self.frameMain_left_topFrame,text = 'API Keys File (JSON)' ).grid(
            row=1,column=0,columnspan=2,pady=(50,0))
        ttk.Label(master = self.frameMain_left_topFrame,text = 'Current Path:'  ).grid(row=2,column=0)
        self.currentApiKeysPath = ttk.Label(master = self.frameMain_left_topFrame,text = "    " + userConfig["ApiKeysPath"]  )
        self.currentApiKeysPath.grid(row=2,column=1,columnspan=2)
        ttk.Label(master = self.frameMain_left_topFrame,text = 'Update:'  ).grid(row=3,column=0)
        self.updateApiKeysPathEntry  = tk.Entry(master = self.frameMain_left_topFrame )
        self.updateApiKeysPathEntry.grid(row=3,column=1)
        self.updateApiKeysPathButton = ttk.Button(master = self.frameMain_left_topFrame,text = "Update" )
        self.updateApiKeysPathButton.grid(row=3,column=2,padx=(10,0))
        
        #ttk.Label(master = self.frameMain_left_bottomFrame_left,text = "Display API Keys").grid(row=3,column=0)
        self.displayApisButton = ttk.Button(master = self.frameMain_left_bottomFrame_left,text = "Display API Keys" )
        self.displayApisButton.grid(row=0,column=0,columnspan = 2, padx = (0,0), pady=(0,0))

        ttk.Label(master = self.frameMain_left_bottomFrame_left,text = "Enter (or update) API Key:", anchor = tk.W  ).grid(
            row=4,column=0,columnspan=3,pady=(40,0))
        ttk.Label(master = self.frameMain_left_bottomFrame_left,text = 'API Name: '  ).grid(row=5,column=0)
        self.newApiNameEntry  = tk.Entry(master = self.frameMain_left_bottomFrame_left )
        self.newApiNameEntry.grid(row=5,column=1)
        ttk.Label(master = self.frameMain_left_bottomFrame_left,text = 'API Key: '  ).grid(row=6,column=0)
        self.newApiKeyEntry  = tk.Entry(master = self.frameMain_left_bottomFrame_left )
        self.newApiKeyEntry.grid(row=6,column=1)
        ttk.Label(master = self.frameMain_left_bottomFrame_left,text = 'API Address: '  ).grid(row=7,column=0)
        self.newApiAddressEntry  = tk.Entry(master = self.frameMain_left_bottomFrame_left )
        self.newApiAddressEntry.grid(row=7,column=1)
        ttk.Label(master = self.frameMain_left_bottomFrame_left,text = 'API Description: '  ).grid(row=8,column=0)
        self.newApiDescriptionEntry  = tk.Entry(master = self.frameMain_left_bottomFrame_left )
        self.newApiDescriptionEntry.grid(row=8,column=1)
        self.newApiKeyNameButton = ttk.Button(master = self.frameMain_left_bottomFrame_left,text = "Enter" )
        self.newApiKeyNameButton.grid(row=8,column=2,padx=(10,0))
        
        ttk.Label(master = self.frameMain_left_bottomFrame_left,text = 'Delete API Key: '  ).grid(row=10,column=0,pady=(40,0))
        self.deleteApiKeyEntry  = tk.Entry(master = self.frameMain_left_bottomFrame_left )
        self.deleteApiKeyEntry.grid(row=10,column=1,pady=(40,0))
        self.deleteApiKeyButton = ttk.Button(master = self.frameMain_left_bottomFrame_left,text = "Enter" )
        self.deleteApiKeyButton.grid(row=10,column=2,pady=(40,0))
        #ttk.Label(master = self.frameMain_left,text = '\n \n Note:').grid(row=4,column=0)
        
        #dataFrame = pd.read_csv('contacts.csv')
        with open( userConfig["ApiKeysPath"] ) as jsonfile:
            js = json.load(jsonfile)
        dataFrame = pd.DataFrame({'API Name': list(js.keys()), 'API Key': list(js.values()) })
        self.apiTable = self.makeTable(self.frameMain_left_bottomFrame_right,dataFrame,dict(row=0,column=0))
        #print(dir(self))        
        #self.tree.grid(row=5,column=4,rowspan=5,columnspan=3,padx=(100,0))
        
        

    def frameText(self,frameName,text,pack=True,cfg={}):
        defaultCfg = dict(master=frameName,  width=550, height=10,background='#272822',fg="white") #NOTE: need same width as parent frame to allow fill x
        if not cfg == {}:
            defaultCfg.update(cfg)
        self.frameMain_left_text = tk.Text( **defaultCfg  )
        self.frameMain_left_text.pack(fill='x')
        self.frameMain_left_text.insert(tk.INSERT,text)
        self.frameMain_left_text.config(state=tk.DISABLED,relief = tk.FLAT)
     
    def frameTitle(self, frameName, title, pack = True):
        self.title = tk.Label(frameName, text=title,font=(self.fontsel, 20),  anchor=tk.W, justify=tk.LEFT, fg = 'white',background='#272822' )
        if pack :
            self.title.pack(side=tk.TOP,fill=tk.X)
        else:
            self.title.grid(row=0,  column=0, sticky='e')
    
    def ttkStyles(self):
        self.style = ttk.Style(self)
          
        self.style.theme_create( "Noteb", parent="alt", 
            settings={
                "TFrame"   : {"configure":{'background':'#272822','foreground':'white'}}, 
                "TLabel"   : {"configure":{'background':'#272822','foreground':'white',}}, 
                "TNotebook": {"configure": {"tabmargins": [0, 0, 0, 0], 'background':'#272822' ,'borderwidth':1} },
                "TNotebook.Tab": {
                    "configure": {"padding": [4, 4], "background": '#272822','foreground':'white' ,'underline':0},
                    "map":       {"background": [("selected", '#48483E')],
                                  "expand": [("selected", [0, 0, 0, 0])] } 
                } 
            } 
        )

        self.style.theme_use("Noteb")   
    
    def makeTable(self,frameName,dataFrame,gridParams,scrollLen = 10):
        '''
            scrollLen = number of lines after which the scrollbar in included
        '''
        columns = tuple('#{}'.format(x) for x in range(1,len(dataFrame.columns)+1))
        self.tree = ttk.Treeview(master = frameName, show="headings", columns=columns)
        #col headings 
        for entry in range(0,len(dataFrame.columns)):
            self.tree.heading(columns[entry], text=dataFrame.columns[entry])
        
        #TODO: fix x slider
        #xsb = ttk.Scrollbar(master=frameName, orient=tk.HORIZONTAL, command=self.tree.xview)
        #self.tree.configure(yscroll=xsb.set)

        if len(dataFrame) > scrollLen:
            ysb = ttk.Scrollbar(master=frameName, orient=tk.VERTICAL, 
                            command=self.tree.yview)
            self.tree.configure(xscroll=ysb.set)
        rowNum = 1
        for index,row in dataFrame.iterrows():
            if rowNum%2 == 1:
               rowLabel = 'oddrow'
            else:
               rowLabel = 'evenrow'          
            self.tree.insert("", tk.END, values=list(row),tags=(rowLabel,))
            rowNum = rowNum +1 
        
        #self.tree.bind("<<TreeviewSelect>>", self.print_selection)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.tree.tag_configure('oddrow',background = '#7c7c76',foreground="white")
        self.tree.tag_configure('evenrow', background='#48483E',foreground="white")
        self.tree.grid(**gridParams)
        if len(dataFrame) > scrollLen:
           sliderGrid = gridParams
           sliderGrid.update( dict(column = gridParams['column']+1, sticky=tk.N + tk.S ) )
           ysb.grid(**sliderGrid)
        #TODO: fix x slider
        #sliderGridH = gridParams
        #sliderGridH.update( dict(row = gridParams['row']+1 ) )
        #xsb.grid(**sliderGridH)
        

    def makeNotebook(self,frameName,todos):
        '''
           frameName - name of parent Frame
           todos - dictionary(key, array) 
             key - name of the sheet
             array - a list of strings that will be logged
        '''
        print('hello')
        self.notebook = ttk.Notebook(frameName, width=750, height=900)
        self.label = ttk.Label(self)
        for key, value in todos.items():
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text=key, underline=0,sticky=tk.NE + tk.SW)
            for text in value:
                ttk.Label(frame, text=text).pack(anchor=tk.W)
        self.notebook.pack()
        self.label.pack(anchor=tk.W)
        self.notebook.enable_traversal()
        self.notebook.bind("<<NotebookTabChanged>>", self.select_tab)
        print("end notebook blok")

    def select_tab(self, event):
        tab_id = self.notebook.select()
        tab_name = self.notebook.tab(tab_id, "text")
        

class beaGuiControler:
    def __init__(self):
       self.root = tk.Tk()
       self.root.configure(background='#272822')
       self.model = beaGuiModel()
       self.view = beaGuiView(self.model,master=self.root)
       self.get_ctrl()                     #run the Controls that populate entries in view from model and load button functions.
       self.ctrl_quit = self.root.destroy
       self.sessionData = 0
    ## contorl part of beaGuiView #################################################
    def get_ctrl(self): 
        #all buttons are flat when clicked 
        self.view.btn_database.config( command = self.btn_databaseFun  )
        self.view.btn_add     .config( command = self.btn_addFun       )      
        self.view.btn_download.config( command = self.btn_downloadFun  )
        self.view.btn_load    .config( command = self.btn_loadFun      )    
        self.view.btn_code    .config( command = self.btn_codeFun      )    
        self.view.btn_help    .config( command = self.btn_helpFun      )    
        self.view.btn_settings.config( command = self.btn_settingsFun  )    
    
    def btn_databaseFun(self):
        self.clearUnpackFrameMainPackLeft()
        #self.view.frameTitle(self.view.frameMain_left, "Search Datasets")
        todos = {
                   "Datasets": ["dataset"],
                   "NIPA": ["NIPA Tables"]
         }
        self.view.makeNotebook(self.view.frameMain_left,todos)
        print("database button clicked")

    def btn_addFun(self): 
        self.clearUnpackFrameMainPackLeft()
        print("addFun      button clicke")

    def btn_downloadFun(self): 
        self.clearUnpackFrameMainPackLeft()
        self.view.frameTitle(self.view.frameMain_left, "Download Data")
        print("downloadFun button clicke")

    def btn_loadFun(self): 
        self.clearUnpackFrameMainPackLeft()
        self.view.frameTitle(self.view.frameMain_left, "Load Data to Current Session")
        print("loadFun     button clicke")

    def btn_codeFun(self): 
        self.clearUnpackFrameMainPackLeft()
        self.view.frameTitle(self.view.frameMain_left, "Code to Extract Data")
        print("codeFun     button clicke")

    def btn_helpFun(self): 
        self.clearUnpackFrameMainPackLeft()
        todos = {
                   "BEA API": [self.model.helpBEAAPI],
                   "Help": [self.model.help],
                   "About": [self.model.licenses],
                  
         }
        self.view.makeNotebook(self.view.frameMain_left,todos)
        print("helpFun     button clicke")     

    def btn_settingsFun(self): 
        self.clearUnpackFrameMainPackLeft()
        self.view.settingsPage()
        self.view.updateApiKeysPathButton.configure(command=self.update_apiKeysPath)
        self.view.newApiKeyNameButton.configure(command=self.update_apiKey)
        print("settingsFun     button clicke")  
    
    def update_apiKey(self):
        #(1) get a path to the keys:
        try:
            #only write the path, no need to enter - in case want to try a temp path
            ghostApiKeyPath = str(self.view.updateApiKeysPathEntry.get()) 
        except:
            ghostApiKeyPath = ""   
        
        if not ghostApiKeyPath == "":
            apiKeyPath  = ghostApiKeyPath
        elif hasattr(self,'newApiKeyPath'):
            apiKeyPath = self.newApiKeyPath
        else:
            try:
                with open('beafullfetchpy/config/userSettings.json') as jsonFile:
                     tempDictPath = json.load(jsonFile)
                     apiKeyPath = tempDictPath['ApiKeysPath']
            except:
                messagebox.showinfo("beafullfetch", "Could not find a Path to the API key - enter one above (no need to press the button)")
        
        #(2) get the new/updated key:
        userKeys = {}
        try:
            newApiName = str(self.view.newApiNameEntry.get())
            newApiKey  = str(self.view.newApiKeyEntry.get())
            if not newApiName == '' and not newApiKey == '':
                userKeys[newApiName] = newApiKey
            else:
                messagebox.showinfo("beafullfetch", "Either API Name or Key is Empty.")
        except:
            messagebox.showinfo("beafullfetch", "Could not read new API Name and Key.")
        
        #(3) update the Api 
        try:
            with open(apiKeyPath) as jsonFile:
                tempAPIKeys = json.load(jsonFile)
        except:
            tempAPIKeys = {}
            messagebox.showinfo("beafullfetch", "Could not open file with API keys - will create one")
        
        tempAPIKeys.update(userKeys)
        print(newApiName + newApiKey + apiKeyPath)
        try:
            with open(apiKeyPath,'w') as jsonFile:
                json.dump(tempAPIKeys, jsonFile)
            messagebox.showinfo("beafullfetch", "API Key Created/Updated.")
            self.view.newApiNameEntry.delete(0,'end')
            self.view.newApiKeyEntry.delete(0,'end')
        except:
            messagebox.showinfo("beafullfetch", "Could not save new API key to file")
    
    def update_apiKeysPath(self):
        #save in self, in case it's impossible to save the data to json,
        # can use the key path entered during a session.
        self.newApiKeyPath = str(self.view.updateApiKeysPathEntry.get())
        userConfig = {}
        try:
            with open('beafullfetchpy/config/userSettings.json') as jsonFile:
                 userConfig.update(json.load(jsonFile))
        except:
            pass

        userConfig['ApiKeysPath'] = self.newApiKeyPath
        try:
            with open('beafullfetchpy/config/userSettings.json','w') as jsonFile:
                 json.dump(userConfig,jsonFile)
            self.view.currentApiKeysPath.configure(text=userConfig['ApiKeysPath'])
            messagebox.showinfo("beafullfetch", "API Keys Path updated.")
        except:
            messagebox.showinfo("beafullfetch", "Error, API Keys Path not updated but available during the session.")

    def update_BeaApiKey(self):
        newPath = str(self.view.updateApiKeysPathEntry.get())
        userConfig = {}
        try:
            with open('beafullfetchpy/config/userSettings.json') as jsonFile:
                 userConfig.update(json.load(jsonFile))
        except:
            pass

        userConfig['ApiKeysPath'] = newPath
        try:
            with open('beafullfetchpy/config/userSettings.json','w') as jsonFile:
                 json.dump(userConfig,jsonFile)
            self.view.currentApiKeysPath.configure(text=userConfig['ApiKeysPath'])
            messagebox.showinfo("beafullfetch", "API Keys Path updated.")
        except:
            messagebox.showinfo("beafullfetch", "Error, API Keys Path not updated.")    
    
    def clearUnpackFrameMainPackLeft(self):
        '''
          Removes the frames in frameMain, clear them, loads leftFrame back  
        '''
        self.unpackFrameMainSubframes()
        self.clearFrameMainSubframes()
        self.view.frameMain_left.pack(**self.view.frameMain_left_packCfg)

    def unpackFrameMainSubframes(self):
        for child in self.view.frameMain.winfo_children():
            child.pack_forget()
    
    def clearFrameMainSubframes(self):
        for child in self.view.frameMain.winfo_children():
            for subchild in child.winfo_children():
                subchild.destroy()
    ## end of view control part ################################################    
    ## controls :               ################################################




if __name__ == '__main__':
    c = beaGuiControler()
    c.view.mainloop()
    x = c.sessionData




'''
from PIL import ImageTk, Image
def svgPhotoImage(file_path_name):
        import rsvg, cairo
        "Returns a ImageTk.PhotoImage object represeting the svg file"
        # Based on pygame.org/wiki/CairoPygame and http://bit.ly/1hnpYZY
        svg = rsvg.Handle(file=file_path_name)
        width, height = svg.get_dimension_data()[:2]
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(width), int(height))
        context = cairo.Context(surface)
        # context.set_antialias(cairo.ANTIALIAS_SUBPIXEL)
        svg.render_cairo(context)
        tk_image = ImageTk.PhotoImage('RGBA')
        image = Image.frombuffer('RGBA', (width, height), surface.get_data(), 'raw', 'BGRA', 0, 1)
        tk_image.paste(image)
        return (tk_image)



from tkinter import *  
from PIL import ImageTk,Image  
root = Tk()  
canvas = Canvas(root, width = 300, height = 300)  
canvas.pack()  
#img = ImageTk.PhotoImage(Image.open("beafullfetchpy/ball.png"))  
img = tk.PhotoImage(file = "beafullfetchpy/test.gif")  
canvas.create_image(20, 20, anchor=NW, image=img)  
root.mainloop() 




https://cairosvg.org/
https://stackoverflow.com/questions/6589358/convert-svg-to-png-in-python



from Tkinter import *
root=Tk()
b=Button(root,justify = LEFT)
photo=PhotoImage(file="beafullfetchpy/test.gif")
b.config(image=photo,width="50",height="50")
b.pack(side=LEFT)
root.mainloop()



from Tkinter import *
class fe:
    def __init__(self,master):
      self.b=Button(master,justify = LEFT)
      self.photo=PhotoImage(file="beafullfetchpy/test.gif")
      self.b.config(image=self.photo,width="10",height="10")
      self.b.pack(side=LEFT)
root = Tk()
front_end=fe(root)
root.mainloop()



from tkinter import *

root = Tk()

height = 5
width = 1
for i in range(height): #Rows
    for j in range(width): #Columns
        b = Entry(root, text="",background='#48483E')
        b.grid(row=i, column=j)

mainloop()



from tkinter import ttk # necessary for the Combobox widget

# ... your code ...

class Page_2(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="The payment options are displayed below", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        global df
        tk.Label(self, text='Select option:').pack()
        self.options = ttk.Combobox(self, values=list(df.columns))
        self.options.pack()
        tk.Button(self, text='Show option', command=self.show_option).pack()

        self.text = tk.Text(self)
        self.text.pack()

        tk.Button(self, text="Restart",
                  command=lambda: controller.show_frame("StartPage")).pack()

    def show_option(self):
        identifier = self.options.get() # get option
        self.text.delete(1.0, tk.END)   # empty widget to print new text
        self.text.insert(tk.END, str(df[identifier]))

    




import csv
import sqlite3
def main():
    with open("contacts.csv", encoding="utf-8", newline="") as f, \
         sqlite3.connect("contacts.db") as conn:
        conn.execute("""CREATE TABLE contacts (
                          last_name text,
                          first_name text,
                          email text,
                          phone text
                        )""")
        conn.executemany("INSERT INTO contacts VALUES (?,?,?,?)",
                         csv.reader(f))



if __name__ == "__main__":
    main()


class NewContact(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.contact = None
        self.form = ContactForm(self)
        self.btn_add = tk.Button(self, text="Confirm",
                                 command=self.confirm)
        self.form.pack(padx=10, pady=10)
        self.btn_add.pack(pady=10)
    
    def confirm(self):
        self.contact = self.form.get_details()
        if self.contact:
          self.destroy()
    
    def show(self):
        self.grab_set()
        self.wait_window()
        return self.contact


import tkinter as tk
import tkinter.ttk as ttk

class App(tk.Tk):
 def __init__(self):
        super().__init__()
        todos = {
                   "Home": ["Do the laundry", "Go grocery shopping"],
                   "Work": ["Install Python", "Learn Tkinter", "Reply emails"],
                   "Vacations": ["Relax!"]
         }
        self.notebook = ttk.Notebook(self, width=250, height=100)
        self.label = ttk.Label(self)
        for key, value in todos.items():
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text=key, underline=0,sticky=tk.NE + tk.SW)
            for text in value:
                ttk.Label(frame, text=text).pack(anchor=tk.W)
        self.notebook.pack()
        self.label.pack(anchor=tk.W)
        self.notebook.enable_traversal()
        self.notebook.bind("<<NotebookTabChanged>>", self.select_tab)
 def select_tab(self, event):
        tab_id = self.notebook.select()
        tab_name = self.notebook.tab(tab_id, "text")
        #text = "Your current selection is: {}".format(tab_name)
        #self.label.config(text=text)




if __name__ == "__main__":
    app = App()
    app.mainloop()


import tkinter as tk 


class LoginApp(tk.Tk): 
    def __init__(self): 
        super().__init__() 
        self.username = ttk.Entry(self) 
        self.password = ttk.Entry(self, show="*") 
        self.login_btn = tk.Button(self, text="Log in", 
                                   command=self.print_login) 
        self.clear_btn = tk.Button(self, text="Clear", 
                                   command=self.clear_form)         
        self.username.pack() 
        self.password.pack() 
        self.login_btn.pack(fill=tk.BOTH) 
        self.clear_btn.pack(fill=tk.BOTH) 
     
    def print_login(self): 
        print("Username: {}".format(self.username.get())) 
        print("Password: {}".format(self.password.get()))
      
    def clear_form(self): 
        self.username.delete(0, tk.END) 
        self.password.delete(0, tk.END) 
        self.username.focus_set() 
 
if __name__ == "__main__": 
    app = LoginApp() 
    app.mainloop()



+ userConfig["ApiKeysPath"]



import csv
import tkinter as tk
import tkinter.ttk as ttk
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.root = tk.Tk()
        tk.Label(self.root,text="hi").grid(row=0,column=0)
        self.makeTable()
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("Treeview", background="black", 
                fieldbackground="black", foreground="white")
    def makeTable(self):
        self.title("Ttk Treeview")
        columns = ("#1", "#2", "#3")
        self.tree = ttk.Treeview(self.root, show="headings", columns=columns)
        self.tree.heading("#1", text="Last name")
        self.tree.heading("#2", text="First name")
        self.tree.heading("#3", text="Email")
        ysb = ttk.Scrollbar(self, orient=tk.VERTICAL, 
                            command=self.tree.yview)
        self.tree.configure(yscroll=ysb.set)
        rowNum = 1
        with open("contacts.csv", newline="") as f:
            for contact in csv.reader(f):
                if rowNum%2 == 1:
                   rowLabel = 'oddrow'
                else:
                   rowLabel = 'evenrow'          
                self.tree.insert("", tk.END, values=contact,tags=(rowLabel,))
                rowNum = rowNum +1 
        
        self.tree.bind("<<TreeviewSelect>>", self.print_selection)
        self.tree.grid(row=1, column=0)
        ysb.grid(row=1, column=1, sticky=tk.N + tk.S)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.tree.tag_configure('oddrow',background = '#7c7c76',foreground="white")
        self.tree.tag_configure('evenrow', background='#48483E',foreground="white")
        self.style = ttk.Style(self)
        #self.style.theme_create( "Treeview", parent="alt", 
        #    settings={
    def print_selection(self, event):
        for selection in self.tree.selection():
            item = self.tree.item(selection)
            last_name, first_name, email = item["values"][0:3]
            text = "Selection: {}, {} <{}>"
            print(text.format(last_name, first_name, email))
 
 
if __name__ == "__main__":
    app = App()
    app.mainloop()




'''