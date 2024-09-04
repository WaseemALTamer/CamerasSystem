import tkinter as tk
from tkinter import ttk
from tkVideoPlayer import TkinterVideo
from ttkthemes import ThemedStyle
import time






class VideoSlider:
    def __init__(self, Master:tk.Label, Video:TkinterVideo) -> None:
        self.Master = Master
        self.Video = Video


        self.progress_value = tk.IntVar(root)
        self.progress_slider = tk.Scale(root, variable=self.progress_value, from_=0, to=0, orient="horizontal", command=self.SeekSecond)
        self.progress_slider.pack(side="left", fill="x", expand=True)
        self.VideoPaused = False

        self.progress_slider.bind("<ButtonPress-1>", self.On_ScaleClick)
        self.progress_slider.bind("<ButtonRelease-1>", self.On_ScaleRelease)

        Master.bind("<<Loaded>>", self.On_Loaded)
        Master.bind("<<SecondChanged>>",self.On_LoadFrame)


    def On_ScaleClick(self, event):
        if not self.Video.is_paused():
            self.Video.pause()

    def On_ScaleRelease(self, event):
        self.Video.seek(self.progress_value.get())
        if self.VideoPaused == False and self.Video.is_paused():
            self.Video.play()

    def SeekSecond(self, event):
        print(self.progress_value.get())

    def On_Loaded(self, event):
        self.progress_slider.config(to=self.Video._video_info["duration"])
        self.StartingTime = time.time()

    def On_LoadFrame(self, event):
        self.progress_value.set(self.Video._time_stamp)




class VideoPlayer: 
    def __init__(self, Master:tk.Label):
        self.Master = Master

        self.style = None

        # Load video this should be changed later on
        self.video = TkinterVideo(master=self.Master, scaled=True, consistant_frame_rate=True)
        self.video.load("Video2.mp4")
        self.video.pack(expand=True, fill="both")

        self.video.Frame_Rate_Scaler = 1

        self.Slider = VideoSlider(Master,self.video)


        self.StartingTime = time.time()
        self.video.play()




    def toggle_play(self, event):
        if self.video.is_paused():
            self.video.play()
        else:
            self.video.pause()


    def On_Ended(self, event):
        print(time.time() - self.StartingTime)





if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('620x480')
    
    
    Player = VideoPlayer(root)
    Player.Master.bind("<space>", Player.toggle_play)
    

    
    
    root.mainloop()
