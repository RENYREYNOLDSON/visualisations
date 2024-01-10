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
        self.map_type.set("Satellite")
        self.map_type.place(x=20,y=40,w=400)

        #DATASET RESOLUTION
        resolution_label = customtkinter.CTkLabel(self,text="Resolution")
        resolution_label.place(x=15,y=80,anchor="nw")
        self.resolution = customtkinter.CTkSegmentedButton(master=self,values=["1k","2k","4k","10k"],width=500,command=self.update_map)
        self.resolution.set("1k")
        self.resolution.place(x=20,y=110,w=400)

        #COLOURS
        data_color_label = customtkinter.CTkLabel(self,text="Satellite Colour")
        data_color_label.place(x=15,y=150,anchor="nw")
        self.data_color = customtkinter.CTkSegmentedButton(master=self,values=["Colour","Displacement"],width=500,command=self.update_map)
        self.data_color.set("Colour")
        self.data_color.place(x=20,y=180,w=400)

        #REGION


        #LABELS?


        #SHOW OCEANS??
        #ISO RESOLUTION
        #ISO COLOURS

        #PROJECTION

        #SAVE
        save = customtkinter.CTkButton(self,text="Save Visualisation")
        save.place(x=20,y=300)

    def update_map(self,value):
        resolution = self.resolution.get()
        color = self.data_color.get()
        map_type = self.map_type.get()

        app.map_frame.draw_map(resolution,color,map_type)





class MapFrame(customtkinter.CTkFrame):#INPUT OF DATA WINDOW
    def __init__(self,master, **kwargs):
        super().__init__(master, **kwargs)
        self.line_x,self.line_y=None,None
        self.map_x,self.map_y=0,0
        self.zoom=1
        self.shown_image=None

        # Create Canvas
        self.canvas = Canvas(self,bd=0, highlightthickness=0)
        self.canvas.configure(width=1200,height=900,scrollregion=(0,0,1800,900))
        self.canvas.pack(fill="both",expand=True,padx=20,pady=(20,10))
        # Canvas Scroll Bar
        hbar=customtkinter.CTkScrollbar(self,orientation="horizontal",height=30)
        hbar.pack(side="bottom",fill="x",pady=(0,10),padx=10)
        hbar.configure(command=self.canvas.xview)
        self.canvas.config(xscrollcommand=hbar.set)

        # Add Image
        self.draw_map("1k","Colour","Isolines")

        #MOUSE MOVEMENT AND POSITION
        self.canvas.bind("<Motion>",self.motion)
        self.canvas.bind("<Button-1>",self.zoom_in)
        self.canvas.bind("<Button-3>",self.zoom_out)

    def draw_map(self,resolution,color,map_type):
        if map_type=="Isolines":
            create_isolines()
            file="plot.png"
        elif map_type=="3D Map":
            pass
        else:
            if color=="Colour":
                file = color_dataset[resolution]
            else:
                file = displacement_dataset[resolution]

        self.canvas.delete("all")
        self.original = PIL.Image.open(file)
        self.zoom_draw()

    def motion(self,event):
        xPos=self.canvas.xview()[0]*1800
        if self.line_x!=None:
            self.canvas.delete(self.line_x)
            self.canvas.delete(self.line_y)
        self.line_x=self.canvas.create_line(xPos+event.x,0,xPos+event.x,900,width=3)
        self.line_y=self.canvas.create_line(xPos+0,event.y,xPos+1200,event.y,width=3)

    def zoom_in(self,event):
        #Get Position Of Area Clicked, Use ZOOM also and add current position
        xPos=self.canvas.xview()[0]*1800
        self.map_x = self.map_x+(event.x+xPos-450)/self.zoom
        self.map_y = self.map_y+(event.y-225)/self.zoom
        self.zoom=self.zoom*2
        self.zoom_draw()

    def zoom_out(self,event):
        #Get Position Of Area Clicked, Use ZOOM also and add current position
        xPos=self.canvas.xview()[0]*1800
        self.map_x = self.map_x-(event.x+xPos-450)/self.zoom
        self.map_y = self.map_y-(event.y-225)/self.zoom
        self.zoom=self.zoom*0.5
        self.zoom_draw()

    def zoom_draw(self):
        if self.zoom==1:
            self.map_x,self.map_y=0,0

        x=self.map_x*self.original.width/1800
        y=self.map_y*self.original.height/1800

        if self.shown_image!=None:
            self.canvas.delete(self.shown_image)
        self.cropped=self.original.crop((x,y,x+int(self.original.width/self.zoom),y+int(self.original.height/self.zoom)))
        self.pil = self.cropped.resize((1800,900))
        self.img = ImageTk.PhotoImage(self.pil)
        self.shown_image=self.canvas.create_image(0,0,image=self.img,anchor="nw")



### MAIN APP CLASS
class App(customtkinter.CTk):#MAIN APP WINDOW
    def __init__(self):
        #CREATING THE CUSTOM TKINTER WINDOW
        super().__init__()
        self.minsize(1200,700)
        self.resizable(False,False)
        self.title("PROBLEM 1")
        w, h = self.winfo_screenwidth(), self.winfo_screenheight()

        #OPTIONS FRAME
        self.options_frame = OptionsFrame(master=self,width=300,height=660)
        self.options_frame.place(x=20,y=20)
        #MAP FRAME
        self.map_frame = MapFrame(master=self,width=840,height=660)
        self.map_frame.place(x=340,y=20)


### FUNCTIONS
def create_3D():
    pass

def create_isolines():
    # Load sample earth relief data
    grid = pygmt.datasets.load_earth_relief(resolution="01d", region=[-180,180, -90, 90])
    fig = pygmt.Figure()

    fig.grdimage(
        grid=grid,
        cmap="haxby"
    )

    fig.grdcontour(
        grid=grid,
        # set the contour interval
        interval=1000,
        # set the interval for annotated contour lines at 1,000 meters
        annotation=2000,
    )
    fig.savefig("plot.png")


if __name__ == "__main__":
    color_dataset={"1k":"dataset/colour_dataset/earthmap1k.jpg",
                    "2k":"dataset/colour_dataset/8081_earthmap2k.jpg",
                    "4k":"dataset/colour_dataset/8081_earthmap4k.jpg",
                    "10k":"dataset/colour_dataset/8081_earthmap10k.jpg"}

    displacement_dataset={"1k":"dataset/displacement_dataset/earthbump1k.jpg",
                    "2k":"dataset/displacement_dataset/8081_earthbump2k.jpg",
                    "4k":"dataset/displacement_dataset/8081_earthbump4k.jpg",
                    "10k":"dataset/displacement_dataset/8081_earthbump10k.jpg"}

    customtkinter.set_appearance_mode("dark")
    app=App()
    app.mainloop()



#TO DO
# Add 3d Plots
# Add Different resolutions of my plots
# Add Other Options for my plots