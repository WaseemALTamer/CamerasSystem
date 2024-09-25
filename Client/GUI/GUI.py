import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
import threading
from DevicesGraper import AvailableDevices
import time



############# Here is where what the buttons' functions are going to be stored!!! ########

class button_functions:
    def __init__(self):
        pass

    def GrabDevices(self):
        self.win = tk.Tk()
        self.win.geometry("200x200")
        self.win.config(background="#1F1F1F")
        self.grabcam = AvailableDevices.GrapCaptureDeviecesListffmpeg()
        self.device_names = Button(self.win, text=self.grabcam, background="#1F1F1F", foreground="#FFFFFF").pack()

    def record(self):
        pass


    def screenshot(self):
        pass

class video_footage:
    pass














class GUI:
    def __init__(self) -> None:
        # sets up the window
        self.root = tk.Tk() 
        self.root.title("Camera GUI")
        self.Width, self.Height = 1280, 720
        self.root.geometry(f'{self.Width}x{self.Height}')

        #create the MainCanvas
        self.MainCanvas = Canvas(self.root, 
                                    background="#1F1F1F",
                                    highlightthickness=0
                                    )
        self.MainCanvas.place(relheight=1, relwidth=1 ,relx=0, rely=0)# Place The Canvas

        # lists where the images and their labels are gonna be stored
        self.ImageLabels:list[tk.Label] = []
        self.TempImage = []
        self.ImagesArray = [] 

        # Reads the images and displays them on the screen and also sets them up for them to be resized
        self._Resizethread = None
        self.OpenImages()
        self.PlaceImageLabels()
        self.MainCanvas.bind("<Configure>", self.on_resize)
        self.MainCanvas.grid_columnconfigure(2, weight=1)

        #set up the button functions
        self.buttfunc = button_functions()
        self.check_cameras = Button(self.MainCanvas, text="Check Available Cameras", command=self.buttfunc.GrabDevices, width=50, height=1)
        #self.root.wm_attributes('-transparentcolor', 'white')  # You can set 'white' or any color you want to be transparent




    def on_resize(self, event=None):
        if (self.Width, self.Height) != (event.width, event.height):
            self.Width, self.Height = event.width, event.height
            self._Resizethread = threading.Thread(target=self.ResizeImage)
            self._Resizethread.start()

    def PlaceImageLabels(self):
        for Index, Object in enumerate(self.ImageLabels):
            self.rowing = Index//2
            self.columning = Index % 2
            Object.grid(row=self.rowing, column=self.columning, padx=5, pady=5)

    def ResizeImage(self):
        for Index, Object in enumerate(self.ImageLabels):
            if self._Resizethread != threading.current_thread():
                return
            if self.Width <= 5 or self.Height <= 5:
                return
            _img = ImageTk.PhotoImage(self.ImagesArray[Index].resize((self.Width//5, self.Height//5)))
            Object.config(image=_img)
            Object.Image = _img
        self.PlaceImageLabels()

    def OpenImages(self):
        for Index in range(1,5):
            _img = Image.open(f"Client\images\cam{Index}.jpg")
            tk_img = ImageTk.PhotoImage(_img.resize((self.Width//5, self.Height//5)))
            self.label = Label(self.MainCanvas, image=tk_img)
            self.label.Image = tk_img
            
            self.ImageLabels.append(self.label)
            self.ImagesArray.append(_img)
            self.label.bind("<Enter>", self.hovering_over_img)
            self.label.bind("<Leave>", self.leaveing_image)

    def test_button_press(self):
        print("you're gay")

    def placebuttons(self):
        self.check_cameras.grid(column=2, row = 0, sticky="nse")

        # record button
        record_img = Image.open(r"Client\GUI\record_button.png")
        self.tk_record = ImageTk.PhotoImage(record_img.resize((30,30)))
        self.placerec = Button(self.MainCanvas, image=self.tk_record, bg="#1F1F1F", bd = 0, command=self.test_button_press)


    def hovering_over_img(self, event):
        self.placerec.grid(column=1, row = 0, sticky="ws")


    def leaveing_image(self, event):
        #time.sleep(5)
        self.placerec.grid_remove()





if __name__ == "__main__":
    gui = GUI()
    gui.placebuttons()
    gui.root.mainloop()