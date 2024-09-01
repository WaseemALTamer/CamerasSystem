# this file is responsable to use the Grapers library to start
# collecting image data from all the different cameras avalible
# this will file will also keep the Photoage of the image for 
# and attempt to store them after 15 seconds this should be 
# able to handel all the Captures devices that we have for 
# starters it is fine if we only save the data without turnning
# it into .mp4 or .avi formates


from Grapers import DevicesGraper, ImageGraper, SoundGraper
from TickSystem import FpsController
from datetime import datetime
import numpy as np
import time
import cv2
import os


# this class will be used as the structure class
class CameraDevice:
    def __init__(self, CameraIndex:int , Name:str) -> None: #the index of the camera will only be used once
        self.Name:str = Name
        self.Graper:ImageGraper.AccessImages = ImageGraper.AccessImages(CameraIndex)


        self.CameraMic:AudioDevice = None # we are going to use this to attach the mic to the camera that has the
                                          # a mic so we can record both sound and image from the camera if possible
                                          # this will come later on but we will do it

        self.Recording:bool = False # this bool will tell us if this speicifc Camera is
                                    # recording for the 15 seconds

        self.CurrentRecordingFolder:str = None # this will help us keep track of the name of the file we are writing on

        self.CurrentRecordingFile:cv2.VideoWriter = None # this is a cv2 file that we use to access the file from so we
                                                         # can write on


        self.Graper.GrapImageContinuouslyOnThread()
        # note that the index of the camera
        # will not be stored this is because
        # camera index is not set on stone

    @property
    def Running(self) -> bool:
        return self.Graper.GraperContinuouslyState
    
    @property
    def Resloution(self) -> tuple[int,int]:
        return (self.Graper.Width, self.Graper.Height)
    
    @property
    def DeviceOutput(self) -> list[np.uint8]:
        while self.Graper.WritingData:
            time.sleep(1/120)
        return self.Graper.DataOutput
    



# this class will be used as the structure class
class AudioDevice:
    def __init__(self) -> None:
        self.Name:str = ...
        self.Graper:SoundGraper.AccessSounds = SoundGraper.AccessSounds()


        self.Graper.GrapSoundContinuouslyOnThread()


    @property
    def Running(self)->bool: # loop back
        return self.Graper.GraperContinuouslyState
        # will not be stored this is because

    @property
    def DeviceOutput(self) -> list[np.int32]:
        while self.Graper.WritingData:
            time.sleep(1/120)
        return self.Graper.DataOutput




class Controller():
    def __init__(self) -> None:

        # we are giong to grap all the input devices we can for starters
        # can keep track of everything we have avalible we should also
        # try to detect if there is anything that was pluged in so we
        # can use it for its inputs so here is what we are going to do
        # we are going to keep checking for any input devices when the
        # main thread is free and we are going to start graping if there
        # is a new device

        self.CaptureDevices:list[CameraDevice] = [] # changed this var name because so it only has Camera Devices
                                                    # lets attach the aduio device that belongs to the camera to
                                                    # the device it self rather than keep it sepratly

        self.RecorderState:bool = False # this var will be the one that tells us if we are already recording
                                        # this var is mostly responsable for the While loop statemnt







    def initCaptureDevice(self):
        CaptureDevicesNames:list[str] = DevicesGraper.AvailableDevices.GrapCaptureDeviecesListffmpeg() # grap the name of all  the capture dvices
        for Index, DeviceName in enumerate(CaptureDevicesNames): # loop through the names to check if we already have them
            for ObjectIndex, Object in enumerate(self.CaptureDevices): # this loop through the devices we already have
                if Object.Running and Object.Name == DeviceName: # check if teh device is running and we have the name
                    CaptureDevicesNames[Index] = None # if so make the name None so we cant create another one of them
                    break
                elif Object.Name == DeviceName: # if the devices name is not running but still exist
                    self.CaptureDevices[ObjectIndex] = CameraDevice(Index, DeviceName) # we can rerun it
                    CaptureDevicesNames[Index] = None # then we can remove if so it is does not have to be re ran with the ones that we have no data on
                    break


        for Index, DeviceName in enumerate(CaptureDevicesNames): # simply loop through hte names back and run the ones that made it through 
            if DeviceName != None: # if the value is none that means it is already running and working else go through the if statement
                self.CaptureDevices.append(
                    CameraDevice(Index, DeviceName) # we intialte the camera and append it to the array that contain all the input devices
                )

        print(self.CaptureDevices)





    def RecordPhotoageForAllCameras(self, Time:int=15, 
                                    DesiredFps:int=30, 
                                    Output="FootageOutput", 
                                    Encoder:str="XVID"):

        # this function should be able to to access all the cameras
        # and store write the data into a file for every 15 second
        # and then move on to the next file this function sohuld be
        # ran on a thread as this function will loop through Capture
        # devices and record everything it can continuasly on the
        # hard drive, Check the c2 library to know which encoders
        # you want to use and which one are suitable for our work

        self.RecorderState = True # we change the recorder state to True so we can start the while loop
                                  # this also alowes us to shut down the while loop any time we want
                                  # without forcing the files to be  closed  because this  can  cause 
                                  # currupted outpued video



        Encoder = cv2.VideoWriter_fourcc(*Encoder)  # Codec for the video so we can write the data
                                                    # in a certain formate with while  not  taking
                                                    # much space 

        while self.RecorderState:

            self.initCaptureDevice() # this function should not inititate the cameras it should just capture the photoage


            RunningDevices:list[CameraDevice] = [] # this function will simply store all the Devices that are running
                                                   # so even if we detect a camera that was intialesd we dont write
                                                   # anything on it until the next set of 15 second but if a Device
                                                   # was diconnected while recording then we simply just cut the video
                                                   # and keep up until the second that we recorded



            for Device in self.CaptureDevices: # we loop the the avalible devices
                if Device.Running: # if the device we encounter is running
                    
                    RunningDevices.append(Device) # we append the device

            WhileLoopController = FpsController(DesiredFps=DesiredFps) # we make a new instatnace for the blocker so we can
                                                                       # bock the loop and relase it next frame

            Date = datetime.now() # lets create instances of datetime so we know where exactly we need to
                                  # store the data for which file

            FolderName:str = f"{Output}/{Date.year}/{Date.day}.{Date.month}/{Date.hour}.{Date.minute}.{Date.second}"



            for Device in RunningDevices: # we loop through it we set all the Devices to recording state
                                          # and also give the devices the folder and file they will be
                                          # dumping there data at
                Device.Recording = True
                Device.CurrentRecordingFolder = F"{FolderName}/{Device.Name}"    # we spicify the name further
                                                                                  # so we  know  exactly  which 
                                                                                  # camera it is when writing it

                if not os.path.exists(Device.CurrentRecordingFolder): # if the direcotry does not exist we simply make the
                                                                      # direcotry
                    os.makedirs(Device.CurrentRecordingFolder)


                # thie line below is VideoWriter object which allowes us to write the file on the go
                Device.CurrentRecordingFile = cv2.VideoWriter(f'{Device.CurrentRecordingFolder}/Video.avi', Encoder, DesiredFps, Device.Resloution)  




            StopWatchStamp:float = time.time() + Time # we create a StopWatchStamp so we know so we know where to
                                                      # stop our next while loop

            while StopWatchStamp >= time.time(): # now we simply keep looping through the loop and collecting the
                                                 # fps until we hit the stopWatchstamp we also need to block the
                                                 # while loop for until the next frame occures
                
                for Device in RunningDevices:
                    
                    if not Device.Running: # check if the device stopped for any reason
                        if Device.Recording: # check if the device is still recording
                            Device.Recording = False # change the bool the false to inform
                                                     # other threads

                            Device.CurrentRecordingFile.release()# release the file so it is not
                                                                 # corrupted and view  the  data
                                                                 # later on
                            Device.CurrentRecordingFile = None

                        continue # move to the next device

                    Data = Device.DeviceOutput # this will grap the data of the device
                                               # if it is still running


                    if Data is not None: # if the data is there then we can write the data
                                         # in the file we created
                        Device.CurrentRecordingFile.write(Data)

                



                #WhileLoopController.ShowFps()
                WhileLoopController.BlockUntilNextFrame() # we block the while loop until the next Frame
                                                          # this works by a tick system and running the
                                                          # other lines of code will effect for how long
                                                          # this function will block the main loop

            for Device in RunningDevices: # we then loop through the Devices and release them
                                          # so we can view the data
                try:
                    Device.Recording = False
                    Device.CurrentRecordingFile.release()
                    Device.CurrentRecordingFile = None
                except:
                    pass


