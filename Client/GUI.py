import tkinter as tk
from PIL import ImageTk, Image

class GUI:
    def setupwindow(self):
        self.root = tk.Tk() # sets up the window
        self.root.title("Camera GUI") # title of the window

        self.windowwidth:int = 500 # width of the window
        self.windowheight:int = 400 # height of the window

        self.root.geometry(f'{self.windowwidth}x{self.windowheight}') # sets the height and width of the window according to the values of the ints before this line of code

    def on_resize(self): # Here I am trying to make it so that the size of the images change when I change the size of the window but I am kinda stuck ngl :/
        self.windowwidth = self.root.winfo_width()
        self.windowheight = self.root.winfo_height()
        print(self.windowheight, self.windowwidth)


    def openimages(self):
        self.photos:list = [] # stores the photos so that they don't get garbage collected
        for i in range(1,5):
            imgopen = Image.open(f"Client\images\cam{i}.jpg") # goes through all of the images and opens them

            img_resize = imgopen.resize((self.windowwidth//5,self.windowheight//5)) # resizes the image

            tk_img = ImageTk.PhotoImage(img_resize)

            self.photos.append(tk_img) # adds all of the photos that are read into the self.photos list

            label = tk.Label(self.root, image=tk_img) # setting up the photos to be displayed
            label.place(x=(i - 0.8) * (self.windowwidth // 4.5), y=0) # seperate all of the photos
            
        self.root.mainloop()



    def buttonfunctions(): # I am gonna be adding buttons to the GUI, and in this function, there are going to be button functions
        print("WIP")


def main(): # function used to test all of the functions in the GUI class
    gui = GUI()
    gui.setupwindow()
    gui.openimages()

main()