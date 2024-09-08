import tkinter as tk
from PIL import ImageTk, Image
import threading
from DevicesGraper import AvailableDevices

class button_functions:
    def GrabDevices(self):
        self.grabcam = AvailableDevices.GrapDevicesNames()
        print(self.grabcam)

class GUI:
    def __init__(self) -> None:
        # sets up the window
        self.root = tk.Tk() 
        self.root.title("Camera GUI")
        self.Width, self.Height = 1280, 720
        self.root.geometry(f'{self.Width}x{self.Height}')

        #create the MainCanvas
        self.MainCanvas = tk.Canvas(self.root, 
                                    background="#1F1F1F",
                                    highlightthickness=0
                                    )
        self.MainCanvas.place(relheight=1, relwidth=1 ,relx=0, rely=0)# Place The Canvas


        # lists where the images and their labels are gonna be stored
        self.ImageLabels:list[tk.Label] = []
        self.TempImage = []
        self.ImagesArray = [] 

        #set up the button functions
        self.buttfunk = button_functions()
        

        # Reads the images and displays them on the screen and also sets them up for them to be resized
        self._Resizethread = None
        self.OpenImages()
        self.PlaceImageLabels()
        self.MainCanvas.bind("<Configure>", self.on_resize)
        self.MainCanvas.grid_columnconfigure(2, weight=1)


        # Buttons
        self.turn_off = tk.Button(self.MainCanvas, text="EXIT", command=self.root.quit, width=50, height=1)
        self.check_cameras = tk.Button(self.MainCanvas, text="Check cameras", command=self.buttfunk.GrabDevices, width=50, height=1)

    def on_resize(self, event=None):
        if (self.Width, self.Height) != (event.width, event.height):
            self.Width, self.Height = event.width, event.height
            self._Resizethread = threading.Thread(target=self.ResizeImage)
            self._Resizethread.start()

    def PlaceImageLabels(self):
        for Index, Object in enumerate(self.ImageLabels):
            Object.grid(row=Index//2, column=Index%2, padx=5, pady=5)

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
            _img = Image.open(f"CamerasSystem-main\Client\images\cam{Index}.jpg")
            tk_img = ImageTk.PhotoImage(_img.resize((self.Width//5, self.Height//5)))
            label = tk.Label(self.MainCanvas, image=tk_img)
            label.Image = tk_img
            self.ImageLabels.append(label)
            self.ImagesArray.append(_img)

    def placebuttons(self):
        self.turn_off.grid(column=2, row = 0, sticky="nse")
        self.check_cameras.grid(column=2, row = 1, sticky="nse")

if __name__ == "__main__":
    gui = GUI()
    gui.placebuttons()
    gui.root.mainloop()
