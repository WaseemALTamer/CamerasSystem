import tkinter as tk
from tkVideoPlayer import TkinterVideo
import time

class VideoPlayer: 
    def __init__(self, Master:tk.Label):
        self.Master = Master


        # Load video
        self.video = TkinterVideo(master=self.Master, scaled=True, consistant_frame_rate=True)
        self.video.load("Video3.mp4")
        self.video.pack(expand=True, fill="both")
        self.video.FrameRateScaler = 0.5


        self.StartingTime = time.time()

        self.video.play()


    def toggle_play(self, event):
        
        if self.video.is_paused():
            self.video.play()
        else:
            self.video.pause()

        self.video.seek(10)


    def Ended(self, event):
        print(time.time() - self.StartingTime)

    def Loaded(self, event):
        self.StartingTime = time.time()

    def OnLoadFrame(self, event):
        print(self.video._time_stamp)



if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('620x480')
    
    Player = VideoPlayer(root)
    Player.Master.bind("<space>", Player.toggle_play)

    Player.Master.bind("<<Loaded>>", Player.Loaded)
    Player.Master.bind("<<Ended>>", Player.Ended)

    Player.Master.bind("<<FrameGenerated>>",Player.OnLoadFrame)
    
    
    root.mainloop()
