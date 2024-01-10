# Import the required packages
import numpy as np
import pygmt
from PIL import ImageTk
import PIL.Image
#import tkinter as tk
import customtkinter as tk
print("Libraries Loaded")

def redraw_3D():
    # Load sample earth relief data
    grid = pygmt.datasets.load_earth_relief()
    fig = pygmt.Figure()
    region=[-14, 30, 35, 60]

    fig.grdimage(
        grid="dataset/colour_dataset/earthmap1k.jpg",
        region=region,cmap="gray", frame=True
    )
    fig.coast(
        region=region,shorelines=True
    )

    print("Figure Created")
    fig.savefig("plot.png")
    plot()


def redraw_isolines():
    grid = pygmt.datasets.load_earth_relief(resolution="01d")
    
    fig = pygmt.Figure()
    fig.grdimage(grid="dataset/colour_dataset/earthmap1k.jpg")
    fig.grdcontour(
        annotation=1000,
        interval=250,
        grid=grid,
        limit=[-4000, -2000],
        projection="M10c",
        frame=True,
    ) 

    print("Figure Created")
    fig.savefig("plot.png")
    plot()


def plot():
    global img
    #Empty Frame and add new map
    for c in map_frame.winfo_children():
        c.destroy()
    img = ImageTk.PhotoImage(PIL.Image.open("plot.png").resize((886,444)))
    panel = tk.CTk.Label(map_frame, image = img)
    panel.pack(expand=False,side="left")


#Refresh image
def refresh():
    if map_type_var.get()=="3D perspective displacement":
        redraw_3D()
    else:
        redraw_isolines()


if __name__ == "__main__":
    root = tk.CTk.Tk()
    root.geometry("1150x500")
    root.title("VISUALISATION 1")
    img=""

    ##GUI
    #Options Frame
    options_frame=tk.CTk.Frame(master=root,width=200,height=700)
    options_frame.pack_propagate(0)
    options_frame.pack(side="left",expand=True)
    #Map Frame
    map_frame=tk.CTk.Frame(master=root,width=900,height=700)
    map_frame.pack_propagate(0)
    map_frame.pack(side="left",expand=True)

    #Refresh Button
    refresh_button=tk.CTk.Button(master=options_frame,text="Refresh",command=refresh)
    refresh_button.place(x=20,y=200)

    ##Map Type
    map_type_label=tk.CTk.Label(options_frame,text="Map Type")
    map_type_label.place(x=10,y=10)
    # Set the default value of the variable 
    options=["3D perspective displacement","Isolines"]
    map_type_var = tk.StringVar(root) 
    map_type_var.set("3D perspective displacement") 
    map_type=tk.CTk.OptionMenu(options_frame,map_type_var,*options)
    map_type.place(x=20,y=40)
    ##Zoom
    #Region
    #Type
    #Quality
    #Colours


    #Render the map
    redraw_3D()


    root.mainloop()

