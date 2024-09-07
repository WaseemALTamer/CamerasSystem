from TickSystem import FpsController 
import threading
import logging
import time
import av





class Graper:

    def __init__(self) -> None:

        self._stop = False
        self._seek_sec = None
        self._seek = False
        self._paused = False
        self._time_stamp = None
        self._duration = None

        self.FrameRate = 0.0
        self.Frame_Rate_Scaler = 1
        self.Frame_Rate_Controller = None
        self._current_img = None
        self._image_ready = False

        self.path = None
        self._load_thread = None




    def _load(self): # this function will be ran on anothread thread because we want the frame blocker to work
                     # we want the frames to be grapped separately 

        with av.open(self.path) as self._container:

            self._container.streams.video[0].thread_type = "AUTO"
            
            self._container.fast_seek = True
            self._container.discard_corrupt = False

            stream = self._container.streams.video[0]



            self._frame_number = 0

            self.stream_base = stream.time_base

            self._duration = float(stream.duration * stream.time_base)

            self.FrameRate = stream.average_rate * self.Frame_Rate_Scaler


            self.Frame_Rate_Controller = FpsController(self.FrameRate)





            while not self._stop:

                if self._seek and not self._stop: # seek to specific second
                    # the seek time is given in av.time_base, the multiplication is to correct the frame
                    self._container.seek(self._seek_sec*1000000)
                    frame = next(self._container.decode(video=0)) # grab the next frame
                    CurrentFrame = float(frame.pts * stream.time_base) # calclate the time of the frame


                    if CurrentFrame >= self._seek_sec and not self._stop: # check if the frame time is before
                        try: # we have to try because this is running on a thread
                            self._container.seek((self._seek_sec - 5)*1000000) # if it is then seek the before 5 sec
                        except:
                            pass

                    self._seek = False # we set the seek to false so it dose not correct where we are
                                        # as we are seeking it from a seek bar this is mostly for gui
                    
                    # we can loop through the frames until we get to the desired frame
                    while CurrentFrame <= self._seek_sec and not self._seek and not self._stop:

                        try:
                            frame = next(self._container.decode(video=0)) # keep getting the next frame
                            CurrentFrame = float(frame.pts * stream.time_base) # update the current frame time so we know where we are at so far
                        except:
                            pass










                try:
                    frame = next(self._container.decode(video=0))

                    self._time_stamp = float(frame.pts * stream.time_base)

                    if (2 * self.Frame_Rate_Controller.Tick) <= (time.time() - self.Frame_Rate_Controller.TickTimer):
                        self.Frame_Rate_Controller.TickTimer += self.Frame_Rate_Controller.Tick
                        continue

                    self._current_img = frame.to_image()
                    self._image_ready = True
                    

            

            

                    #self.Frame_Rate_Controller.ShowFps()
                    self.Frame_Rate_Controller.BlockUntilNextFrame()    # this is much better methode than the time.sleep()
                                                                        # this utlise the simple mousle that will achieve
                                                                        # the Desired Frame rate through keeping track of a tick
                                                                        # system i still left the code for the previous methode
                                                                        # so you can use that if you dont care about playing the
                                                                        # video faster or slower


                except Exception as e:
                    if e.errno == 541478725:
                        print("End of file")
                        self.pause()
                        pass
                    else:
                        print(e.errno)



                while self._paused: # we can block the thread if we are paused but only after the next frame is loaded
                    time.sleep(0.0001) # to allow other threads to function better when its paused


                    self.Frame_Rate_Controller.TickTimer = time.time()  # reset the TickTimer this will help
                                                                        # tell our code that we are not behind on
                                                                        # fps
                    continue

    def PlayRate(self):
        pass

    def load(self, path: str):
        """ loads the file from the given path """
        self.stop()
        self.path = path
        self.play()
        self._paused = True

    def stop(self):
        """ stops reading the file """
        self._paused = True
        self._stop = True

    def pause(self):
        """ pauses the video file """
        self._paused = True

    def play(self):
        """ plays the video file """
        self._paused = False
        self._stop = False

        if not self._load_thread:
            # print("loading new thread...")
            self._load_thread = threading.Thread(target=self._load, daemon=True)
            self._load_thread.start()

    def seek(self, sec: int):
        """ seeks to specific time""" 

        self._seek = True
        self._seek_sec = sec