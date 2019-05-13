import tkinter as tk
import tkinter.ttk as ttk
import sys
import os
import subprocess
import json
import re

class beaGuiModel:  
    def __init__(self,exitProcess=0):  
        self.getLicenses()
        self.getHelp()
    def set_exitProcess(self, exitProcess=0):
        self.exitProcess = exitProcess
    def getLicenses(self):
        self.licenses = licenses()
    def getHelp(self):
        self.help = helpIcons()

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


class beaGuiView(tk.Frame):
    '''
      Fixes the overall geometry of the app.  Note: writing based mainly in pack not grid since the 
      overall shape (vertical or horizontal blocks that fill the whole space) fits this framework better.
    '''
    def __init__(self, model, master=None):
        super().__init__(master)   #TODO: remove and put in control? is this even possible?
        self.model = model         #TODO: maybe mediate all interaction vai Control
        self.fontsel = "Times"
        self.Appconfigs()
        # self.create_widgets()
        self.MainContainers()
        self.mainPanel()
        self.sideNav()
        self.master.bind('<Button-1>', self.keep_flat)
    def keep_flat(self,event):       # on click,
        #print(event)
        #print("this is the widget")
        #print(event.widget)
        event.widget.config(relief=tk.FLAT) # enforce an option
    def Appconfigs(self, title="BEA Full Data Fetch (beafullfetch)"):
        self.master.title(title)
        # self.master.option_add('*Font','Times')
        self.master.geometry('{}x{}'.format(950, 800))
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
    
    def makeNotebook(self,frameName,todos):
        '''
           frameName - name of parent Frame
           todos - dictionary(key, array) 
             key - name of the sheet
             array - a list of strings that will be logged
        '''
        #self.style = ttk.Style(self)  #ttk styling
        #self.style.configure("TLabel", background='#272822',foreground = "white")
        #self.style.configure("TNotebook", background='#272822',foreground = "white")
        #self.style.configure("TNotebook.Tab", background='#48483E',foreground = "white")
        #self.style.map("TNotebook.Tab", background=[("selected",'#272822' )], foreground=[("selected", '#272822')]);
        #self.style.configure("TFrame", background='#272822',foreground = "white")
        try:
            self.notebook.destroy()
        except:
            pass
        print('hello')
        self.style = ttk.Style(self)
        try:    #TODO: move this out, should only create the theme once.    
            self.style.theme_create( "Noteb", parent="alt", settings={
                    "TFrame"   : {"configure":{'background':'#272822','foreground':'white'}}, 
                    "TLabel"   : {"configure":{'background':'#272822','foreground':'white'}}, 
                    "TNotebook": {"configure": {"tabmargins": [0, 0, 0, 0], 'background':'#272822' ,'borderwidth':1} },
                    "TNotebook.Tab": {
                        "configure": {"padding": [4, 4], "background": '#272822','foreground':'white' ,'underline':0},
                        "map":       {"background": [("selected", '#48483E')],
                                      "expand": [("selected", [0, 0, 0, 0])] } } } )
        except: 
            pass
        self.style.theme_use("Noteb")  
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
       self.app = beaGuiView(self.model,master=self.root)
       self.get_ctrl()                     #run the Controls that populate entries in view from model and load button functions.
       self.ctrl_quit = self.root.destroy
       self.sessionData = 0
    ## contorl part of beaGuiView #################################################
    def get_ctrl(self): 
        #all buttons are flat when clicked 
        self.app.btn_database.config( command = self.btn_databaseFun  )
        self.app.btn_add     .config( command = self.btn_addFun       )      
        self.app.btn_download.config( command = self.btn_downloadFun  )
        self.app.btn_load    .config( command = self.btn_loadFun      )    
        self.app.btn_code    .config( command = self.btn_codeFun      )    
        self.app.btn_help    .config( command = self.btn_helpFun      )    
        self.app.btn_settings.config( command = self.btn_settingsFun  )    
    
    def btn_databaseFun(self):
        self.clearUnpackFrameMainPackLeft()
        self.app.frameTitle(self.app.frameMain_left, "Search Datasets")
        print("database button clicked")

    def btn_addFun(self): 
        self.clearUnpackFrameMainPackLeft()
        print("addFun      button clicke")

    def btn_downloadFun(self): 
        self.clearUnpackFrameMainPackLeft()
        self.app.frameTitle(self.app.frameMain_left, "Download Data")
        print("downloadFun button clicke")

    def btn_loadFun(self): 
        self.clearUnpackFrameMainPackLeft()
        self.app.frameTitle(self.app.frameMain_left, "Load Data to Current Session")
        print("loadFun     button clicke")

    def btn_codeFun(self): 
        self.clearUnpackFrameMainPackLeft()
        self.app.frameTitle(self.app.frameMain_left, "Code to Extract Data")
        print("codeFun     button clicke")

    def btn_helpFun(self): 
        self.clearUnpackFrameMainPackLeft()
        #self.app.frameTitle(self.app.frameMain_left, "Help")
        #self.app.frameText(self.app.frameMain_left,self.model.help)
        #self.app.frameTitle(self.app.frameMain_left, "About")
        #self.app.frameText(self.app.frameMain_left,self.model.licenses,cfg={'height':30})
        todos = {
                   "Help": [self.model.help],
                   "About": [self.model.licenses]
                  
         }
        self.app.makeNotebook(self.app.frameMain_left,todos)
        print(type(self.model.licenses))
        print("helpFun     button clicke")     

    def btn_settingsFun(self): 
        self.clearUnpackFrameMainPackLeft()
        self.app.frameTitle(self.app.frameMain_left, "Settings")
        print("settingsFun     button clicke")  
    
    def clearUnpackFrameMainPackLeft(self):
        '''
          Removes the frames in frameMain, clear them, loads leftFrame back  
        '''
        self.unpackFrameMainSubframes()
        self.clearFrameMainSubframes()
        self.app.frameMain_left.pack(**self.app.frameMain_left_packCfg)

    def unpackFrameMainSubframes(self):
        for child in self.app.frameMain.winfo_children():
            child.pack_forget()
    
    def clearFrameMainSubframes(self):
        for child in self.app.frameMain.winfo_children():
            for subchild in child.winfo_children():
                subchild.destroy()
    ## end of view control part ################################################    
    ## controls :               ################################################




if __name__ == '__main__':
    c = beaGuiControler()
    c.app.mainloop()
    x = c.sessionData

tk.Entry()


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





'''