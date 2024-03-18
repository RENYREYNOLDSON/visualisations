# Import the required packages
import numpy as np
import pygmt
from PIL import ImageTk
import PIL.Image
#import tkinter as tk
import customtkinter
from tkinter import Canvas


class OptionsFrame(customtkinter.CTkFrame):#INPUT OF DATA WINDOW
    def __init__(self,master, **kwargs):
        super().__init__(master, **kwargs)
        #MAP TYPE
        map_type_label = customtkinter.CTkLabel(self,text="Map Type")
        map_type_label.place(x=15,y=10,anchor="nw")
        self.map_type = customtkinter.CTkSegmentedButton(master=self,values=["Satellite","3D Map", "Isolines"],width=500,command=self.update_map)
        self.map_type.set("3D Map")
        self.map_type.place(x=20,y=40,w=260)

        #DATASET RESOLUTION
        resolution_label = customtkinter.CTkLabel(self,text="Resolution")
        resolution_label.place(x=15,y=80,anchor="nw")
        self.resolution = customtkinter.CTkSegmentedButton(master=self,values=["1k","2k","4k","10k"],width=500,command=self.update_map)
        self.resolution.set("1k")
        self.resolution.place(x=20,y=110,w=260)

        #COLOURS
        data_color_label = customtkinter.CTkLabel(self,text="Satellite Colour")
        data_color_label.place(x=15,y=150,anchor="nw")
        self.data_color = customtkinter.CTkSegmentedButton(master=self,values=["Colour","Displacement"],width=500,command=self.update_map)
        self.data_color.set("Colour")
        self.data_color.place(x=20,y=180,w=260)

        #####################
        #SCALE?
        data_color_label = customtkinter.CTkLabel(self,text="Scale Models")
        data_color_label.place(x=15,y=220,anchor="nw")
        self.scale = customtkinter.CTkCheckBox(master=self,text="Scale the models when zooming")
        self.scale.place(x=20,y=250,w=260)
        #Isoline heights
        data_color_label = customtkinter.CTkLabel(self,text="Isoline Heights -5000m-2000m")
        data_color_label.place(x=15,y=290,anchor="nw")
        self.iso_height = customtkinter.CTkSlider(master=self,from_=-5000,to=2000,width=500,command=self.update_map)
        self.iso_height.set(100)
        self.iso_height.place(x=20,y=320,w=260)
        #Isoline intervals
        data_color_label = customtkinter.CTkLabel(self,text="Isoline Intervals 100-2000")
        data_color_label.place(x=15,y=360,anchor="nw")
        self.interval = customtkinter.CTkSlider(master=self,from_=100,to=2000,width=500,command=self.update_map)
        self.interval.set(1000)
        self.interval.place(x=20,y=390,w=260)
        #3D heights
        data_color_label = customtkinter.CTkLabel(self,text="3D Amplitude 0-10x")
        data_color_label.place(x=15,y=430,anchor="nw")
        self.d_height = customtkinter.CTkSlider(master=self,from_=0.1,to=10,width=500,command=self.update_map)
        self.d_height.set(1.5)
        self.d_height.place(x=20,y=460,w=260)
        #data resolution
        data_color_label = customtkinter.CTkLabel(self,text="Data Resolution")
        data_color_label.place(x=15,y=500,anchor="nw")
        self.data_res = customtkinter.CTkSegmentedButton(master=self,values=["Low","Medium","High"],width=500,command=self.update_map)
        self.data_res.set("Low")
        self.data_res.place(x=20,y=530,w=260)
        #COLOUR
        data_color_label = customtkinter.CTkLabel(self,text="Show Colour")
        data_color_label.place(x=15,y=570,anchor="nw")
        self.colour = customtkinter.CTkCheckBox(master=self,text="Show colour on the models")
        self.colour.place(x=20,y=600,w=260)

        #####################


    def update_map(self,value):
        resolution = self.resolution.get()
        color = self.data_color.get()
        map_type = self.map_type.get()
        scale = self.scale.get()
        iso_height=self.iso_height.get()
        d_height=self.d_height.get()
        interval=self.interval.get()
        data_res=self.data_res.get()
        colour=self.colour.get()

        app.map_frame.draw_map(resolution,color,map_type,scale,iso_height,d_height,interval,data_res,colour)





class MapFrame(customtkinter.CTkFrame):#INPUT OF DATA WINDOW
    def __init__(self,master, **kwargs):
        super().__init__(master, **kwargs)
        self.line_x,self.line_y=None,None
        self.map_x,self.map_y=0,0
        self.zoom=1
        self.shown_image=None

        # Create Canvas
        self.canvas = Canvas(self,bd=0, highlightthickness=0)
        self.canvas.configure(width=1200,height=600,scrollregion=(0,0,1200,600))
        self.canvas.pack(fill="both",expand=True,padx=20,pady=(20,20))
        # Canvas Scroll Bar
        """
        hbar=customtkinter.CTkScrollbar(self,orientation="horizontal",height=30)
        hbar.pack(side="bottom",fill="x",pady=(0,10),padx=10)
        hbar.configure(command=self.canvas.xview)
        self.canvas.config(xscrollcommand=hbar.set)
        """

        # Add Image
        #self.draw_map("1k","Colour","3D Map")

        #MOUSE MOVEMENT AND POSITION
        self.canvas.bind("<Motion>",self.motion)
        self.canvas.bind("<Button-1>",self.zoom_in)
        self.canvas.bind("<Button-3>",self.zoom_out)

    def draw_map(self,resolution,colorset,map_type,scale,iso_height,d_height,interval,data_res,colour):
        region=[-180,180,-90,90]
        if scale:
            region=toRegion(self.map_x,self.map_y,self.zoom)
        if map_type=="Isolines":
            create_isolines(region,iso_height,interval,data_res,colour)
            file="plot.png"
        elif map_type=="3D Map":
            create_3D(region,d_height,data_res,colour)
            file="plot.png"
        else:
            if colorset=="Colour":
                file = color_dataset[resolution]
            else:
                file = displacement_dataset[resolution]

        self.canvas.delete("all")
        self.original = PIL.Image.open(file)
        self.zoom_draw()

    def motion(self,event):
        if self.line_x!=None:
            self.canvas.delete(self.line_x)
            self.canvas.delete(self.line_y)
        self.line_x=self.canvas.create_line(event.x,0,event.x,900,width=3)
        self.line_y=self.canvas.create_line(0,event.y,1200,event.y,width=3)

    def zoom_in(self,event):
        #Get Position Of Area Clicked, Use ZOOM also and add current position
        self.map_x = self.map_x+(event.x-300)/self.zoom
        self.map_y = self.map_y+(event.y-150)/self.zoom
        self.zoom=self.zoom*2
        self.zoom_draw()

    def zoom_out(self,event):
        #Get Position Of Area Clicked, Use ZOOM also and add current position
        if self.zoom>1:
            self.map_x = self.map_x-(event.x)/self.zoom
            self.map_y = self.map_y-(event.y)/self.zoom
            self.zoom=self.zoom*0.5
            self.zoom_draw()

    def zoom_draw(self):
        if self.zoom==1:
            self.map_x,self.map_y=0,0

        x=self.map_x*self.original.width/1200
        y=self.map_y*self.original.height/600

        if self.shown_image!=None:
            self.canvas.delete(self.shown_image)
        self.cropped=self.original.crop((x,y,x+int(self.original.width/self.zoom),y+int(self.original.height/self.zoom)))
        self.pil = self.cropped.resize((1200,600))
        self.img = ImageTk.PhotoImage(self.pil)
        self.shown_image=self.canvas.create_image(0,0,image=self.img,anchor="nw")



### MAIN APP CLASS
class App(customtkinter.CTk):#MAIN APP WINDOW
    def __init__(self):
        #CREATING THE CUSTOM TKINTER WINDOW
        super().__init__()
        self.minsize(1600,700)
        #self.resizable(False,False)
        self.title("PROBLEM 1")
        w, h = self.winfo_screenwidth(), self.winfo_screenheight()

        #OPTIONS FRAME
        self.options_frame = OptionsFrame(master=self,width=300,height=660)
        self.options_frame.place(x=20,y=20)
        #MAP FRAME
        self.map_frame = MapFrame(master=self,width=840,height=660)
        self.map_frame.place(x=340,y=20)

        


### FUNCTIONS
def create_3D(region,d_height,data_res,colour):
    grid = pygmt.datasets.load_earth_relief(resolution=resolutions[data_res], region=region)
    fig = pygmt.Figure()
    if colour:
        surf="s"
    else:
        surf=None
    
    fig.grdview(
        grid=grid,
        perspective=[130, 30],
        frame=["xa", "yaf", "WSnE"],
        zsize=str(d_height)+"c",
        # Set the surftype to "surface"
        surftype=surf,
        # Set the CPT to "geo"
        cmap="geo",
    )

    fig.savefig("plot.png")

def create_isolines(region,iso_height,interval,data_res,colour):
    # Load sample earth relief data
    grid = pygmt.datasets.load_earth_relief(resolution=resolutions[data_res], region=region)
    print(region)
    fig = pygmt.Figure()
    if colour:
        fig.grdimage(
            grid=grid,
            cmap="haxby"
        )

    fig.grdcontour(
        grid=grid,
        # set the contour interval
        interval=interval,
        # set the interval for annotated contour lines at 1,000 meters
        annotation=2000,
        limit=[iso_height,1000000]
    )
    fig.savefig("plot.png")

def toRegion(x,y,zoom):
    x1=(x/(1200*zoom))*360-180
    y1=(y/(600*zoom))*180-90
    x2=x1+(360/zoom)
    y2=y1+(180/zoom)
    return [int(x1),int(x2),int(y1),int(y2)]


if __name__ == "__main__":
    color_dataset={"1k":"dataset/colour_dataset/earthmap1k.jpg",
                    "2k":"dataset/colour_dataset/8081_earthmap2k.jpg",
                    "4k":"dataset/colour_dataset/8081_earthmap4k.jpg",
                    "10k":"dataset/colour_dataset/8081_earthmap10k.jpg"}

    displacement_dataset={"1k":"dataset/displacement_dataset/earthbump1k.jpg",
                    "2k":"dataset/displacement_dataset/8081_earthbump2k.jpg",
                    "4k":"dataset/displacement_dataset/8081_earthbump4k.jpg",
                    "10k":"dataset/displacement_dataset/8081_earthbump10k.jpg"}
    
    resolutions={"Low":"01d","Medium":"30m","High":"10m"}

    customtkinter.set_appearance_mode("dark")
    app=App()
    app.options_frame.update_map(0)
    #app.after(0, lambda:app.state('zoomed'))
    app.mainloop()



