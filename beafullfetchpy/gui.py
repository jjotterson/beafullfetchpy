import tkinter as tk
import sys
import os
import subprocess
import json
import re

class beaGuiModel:  
    def __init__(self,exitProcess=0):  
        pass
    def set_exitProcess(self, exitProcess=0):
        self.exitProcess = exitProcess
       
    
class beaGuiView(tk.Frame):
    def __init__(self, model, master=None):
        super().__init__(master)   #TODO: remove and put in control? is this even possible?
        self.model = model         #TODO: maybe mediate all interaction vai Control
        self.fontsel = "Times"
        self.Appconfigs()
        # self.create_widgets()
        self.MainContainers()
        self.mainPanel()
        self.sideNav()
    
    def Appconfigs(self, title="BEA Full Data Fetch (beafullfetch)"):
        self.master.title(title)
        # self.master.option_add('*Font','Times')
        self.master.geometry('{}x{}'.format(950, 600))
    def MainContainers(self):
        # Main containers
        self.frameMain = tk.Frame(
            self.master, width=400, height=50, pady=3, padx=1, bd=2, relief=tk.FLAT,  background='#272822')   
        self.frameSideNav = tk.Frame(
            self.master, width=400, height=50, pady=3, padx=1, bd=2,  background='#48483E')
        
        # layout of the main containers
        #root.grid_rowconfigure(1, weight=1)
        #root.grid_columnconfigure(0, weight=1)
        
        self.frameSideNav.pack(side = tk.LEFT, fill=tk.Y  )
        self.frameMain.pack(side = tk.LEFT, fill=tk.Y  )
        
    def mainPanel(self):
        # top frame widgets
        #
        # Geometry
        self.top_left = tk.Frame(self.frameMain,  width=550, height=190)
        self.top_left.grid(row=0, column=0, sticky="ns")
        #
        # Content
        tk.Label(self.top_left, text="Data Info", font=(self.fontsel, 20),
                 anchor=tk.W, justify=tk.LEFT, fg = 'white',background='#272822' ).grid(row=0,  column=0, sticky='e')
   


    def sideNav(self): #############################################################
        # Summary frame widgets
        # Geometry
        self.sidenav_topframe = tk.Frame(self.frameSideNav,background='#48483E')
        self.sidenav_topframe.pack()
       
        self.sidenav_bottomframe = tk.Frame(self.frameSideNav,background='#48483E')
        self.sidenav_bottomframe.pack(side=tk.BOTTOM)
        #
        btnCfg = dict(anchor=tk.W, relief = tk.FLAT,justify=tk.LEFT, background='#48483E', activebackground='#48483E',activeforeground='white',fg = 'white' )
        btnBaseGrid = dict(column=0, sticky='w',padx = 10, pady=10)
        #top buttons
        self.btn_database = tk.Button(self.sidenav_topframe, text="Database", anchor=tk.W, relief = tk.FLAT,justify=tk.LEFT, background='#48483E',highlightbackground='#3E4149', activebackground='#48483E',activeforeground='white',fg = 'blue').grid(row=0,  **btnBaseGrid)
        self.btn_database = tk.Button(self.sidenav_topframe, text="Add",      **btnCfg ).grid(row=1,  **btnBaseGrid)
        self.btn_database = tk.Button(self.sidenav_topframe, text="Download", **btnCfg ).grid(row=2,  **btnBaseGrid)
        self.btn_database = tk.Button(self.sidenav_topframe, text="Load",     **btnCfg ).grid(row=3,  **btnBaseGrid)  
        self.btn_database = tk.Button(self.sidenav_topframe, text="Code",     **btnCfg ).grid(row=4,  **btnBaseGrid)
        self.btn_database = tk.Button(self.sidenav_topframe, text="Code to Clipboard",  **btnCfg  ).grid(row=5,  **btnBaseGrid)
        self.btn_database = tk.Button(self.sidenav_topframe, text="Help",     **btnCfg ).grid(row=6,  **btnBaseGrid)
        #bottom button
        self.btn_database = tk.Button(self.sidenav_bottomframe, text="About", **btnCfg  ).grid(row=8,  **btnBaseGrid)




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
         pass
    #    self.app.btn_name.config( command = self.btn_nameFun  )
    #    self.app.btn_commit.config(command = self.btn_commitFun )
    #    self.app.btn_exit.config(  command = self.btn_exitFun )
    #def btn_exitFun(self):
    #    self.model.exitProcess = 1
    #    self.ctrl_quit()  #need the () else it is a function 
    #
    #def btn_commitFun(self):
    #    #get data typed in the "entry" fields - data typed in
    #    self.model.notify = self.app.mailLog.get()
    #    self.model.request = self.app.approvalLog.get()
    #    self.model.emailText = self.app.emailText.get("1.0",tk.END)
    #    self.ctrl_quit()
    ## end of view control part ###################################################    
    ## controls of git run itself: ################################################




if __name__ == '__main__':
    c = beaGuiControler()
    c.app.mainloop()
    x = c.sessionData


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



https://cairosvg.org/
https://stackoverflow.com/questions/6589358/convert-svg-to-png-in-python
