#DO OCEANS RISING FOR THIS!!! HAVE A SLIDER OR A YEAR THING
# HAVE EMISSIONS ETC BEING TRACKED

# Import the required packages
import numpy as np
import pygmt
from PIL import ImageTk
import PIL.Image
#import tkinter as tk
import customtkinter
from tkinter import Canvas




class OceanFrame(customtkinter.CTkFrame):#INPUT OF DATA WINDOW
    def __init__(self,master, **kwargs):
        super().__init__(master, **kwargs)
        self.map_type_label = customtkinter.CTkLabel(self,text="Sea Level Rise: 0 metres",font=sfont)
        self.map_type_label.pack(padx=20,pady=(10,5))
        self.sea_level=customtkinter.CTkSlider(master=self,from_=0,to=1000,width=1720)
        self.sea_level.bind("<ButtonRelease-1>",self.master.map_frame.move)
        self.sea_level.set(0)
        self.sea_level.pack(padx=20,pady=(0,20),fill="both")


class InfoFrame(customtkinter.CTkFrame):#INPUT OF DATA WINDOW
    def __init__(self,master, **kwargs):
        super().__init__(master, **kwargs)
        self.img = PIL.Image.open("stats.png")
        self.infographic = ImageTk.PhotoImage(self.img)
        label = customtkinter.CTkLabel(self, image=self.infographic,text="")
        label.pack(padx=10,pady=10)

class StatsFrame(customtkinter.CTkFrame):#INPUT OF DATA WINDOW
    def __init__(self,master, **kwargs):
        super().__init__(master, **kwargs)
        self.img = PIL.Image.open("info.png")
        self.infographic = ImageTk.PhotoImage(self.img)
        label = customtkinter.CTkLabel(self, image=self.infographic,text="")
        label.pack(padx=10,pady=10)

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
        self.draw_map(0,"Colour","Satellite")

        #MOUSE MOVEMENT AND POSITION
        self.canvas.bind("<Motion>",self.motion)
        self.canvas.bind("<Button-1>",self.zoom_in)
        self.canvas.bind("<Button-3>",self.zoom_out)

    def move(self,e):
        rise = app.ocean_frame.sea_level.get()
        app.ocean_frame.map_type_label.configure(text="Sea Level Rise: "+str(int(rise))+" metres")
        app.update()
        self.draw_map(rise ,0,0)

    def draw_map(self,rise,color,map_type):
        print("trrug")
        create_3D(rise)
        self.original = PIL.Image.open(color_dataset["10k"])
        ocean = PIL.Image.open("plot.png").resize((10800,5400))
        #COMBINE IMAGES HERE!
        self.original.paste(ocean, (0,0), mask = ocean) 
        

        self.canvas.delete("all")
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
        self.minsize(1800,860)
        self.resizable(False,False)
        self.title("PROBLEM 2")
        w, h = self.winfo_screenwidth(), self.winfo_screenheight()

        #MAIN TITLE
        font=("Lexend", 76,"bold")
        self.title=customtkinter.CTkLabel(master=self,text="Climate Change & Sea Level Rise",font=font)
        self.title.place(relx=0.5,y=50,anchor="center")

        #MAP FRAME
        self.map_frame = MapFrame(master=self,width=1200,height=660)
        self.map_frame.place(x=280,y=100)

        #STATS FRAME
        self.stats_frame=StatsFrame(master=self,width=240,height=720)
        self.stats_frame.place(x=20,y=20)

        #INFO FRAME
        self.info_frame=InfoFrame(master=self,width=240,height=720)
        self.info_frame.place(x=1540,y=20)

        #OCEAN FRAME
        self.ocean_frame = OceanFrame(master=self,width=1760,height=200)
        self.ocean_frame.place(x=20,y=760)




### FUNCTIONS
def create_3D(rise):
    grid = pygmt.datasets.load_earth_relief(resolution="20m", region=[-180,180, -90, 90])
    # Set the elevation threshold for high altitude
    sea_level = rise  # Adjust this value based on your requirements


    # Create masks for areas above and below the elevation threshold
    below_threshold_mask = grid < sea_level

    below_threshold_grid = grid * below_threshold_mask

    clip = pygmt.grdclip(grid=grid, above=[sea_level,"NaN"],below=[-10,"NaN"])

    # Create a PyGMT figure
    fig = pygmt.Figure()

    # Plot the below-threshold areas with a different color
    fig.grdimage(grid=clip,cmap=True,nan_transparent=True)

    fig.savefig("plot.png")
    img = PIL.Image.open("plot.png")

    # Convert the image to RGBA mode (if not already in RGBA)
    img = img.convert('RGBA')

    # Get the image data
    data = img.getdata()

    # Create a new image with blue background
    new_data = [(29,86,115, 255) if pixel[:3] != (255, 255, 255) else pixel for pixel in data]

    new_data = [(0,0,0,0) if pixel[:3] == (255, 255, 255) else pixel for pixel in new_data]

    # Update the image data
    img.putdata(new_data)

    # Save the result
    img.save("plot.png")



if __name__ == "__main__":
    sfont=("Lexend", 20,"bold")
    color_dataset={"1k":"dataset/colour_dataset/earthmap1k.jpg",
                    "2k":"dataset/colour_dataset/8081_earthmap2k.jpg",
                    "4k":"dataset/colour_dataset/8081_earthmap4k.jpg",
                    "10k":"dataset/colour_dataset/8081_earthmap10k.jpg"}

    displacement_dataset={"1k":"dataset/displacement_dataset/earthbump1k.jpg",
                    "2k":"dataset/displacement_dataset/8081_earthbump2k.jpg",
                    "4k":"dataset/displacement_dataset/8081_earthbump4k.jpg",
                    "10k":"dataset/displacement_dataset/8081_earthbump10k.jpg"}

    customtkinter.set_appearance_mode("light")
    app=App()
    app.mainloop()
