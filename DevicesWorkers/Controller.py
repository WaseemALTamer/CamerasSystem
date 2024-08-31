# this file is responsable to use the Grapers library to start
# collecting image data from all the different cameras avalible
# this will file will also keep the Photoage of the image for 
# and attempt to store them after 15 seconds this should be 
# able to handel all the Captures devices that we have for 
# starters it is fine if we only save the data without turnning
# it into .mp4 or .avi formates


from Grapers import DevicesGraper, ImageGraper, SoundGraper
import numpy as np
import time


# this class will be used as the structure class
class CameraDevice:
    def __init__(self, CameraIndex:int , Name:str) -> None: #the index of the camera will only be used once
        self.Name:str = Name
        self.Graper:ImageGraper.AccessImages = ImageGraper.AccessImages(CameraIndex)


        self.Graper.GrapImageContinuouslyOnThread()
        # note that the index of the camera
        # will not be stored this is because
        # camera index is not set on stone

    @property
    def Running(self) -> bool:
        return self.Graper.GraperContinuouslyState
    
    @property
    def DeviceOutput(self) -> list[np.uint8]:
        return self.Graper.DataOutput
    
    @property
    def DataBeingWriten(self) -> bool:
        return self.Graper.WritingData



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
        return self.Graper.DataOutput
    
    @property
    def DataBeingWriten(self) -> bool:
        return self.Graper.WritingData




class Controller():
    def __init__(self) -> None:

        # we are giong to grap all the input devices we can for starters
        # can keep track of everything we have avalible we should also
        # try to detect if there is anything that was pluged in so we
        # can use it for its inputs so here is what we are going to do
        # we are going to keep checking for any input devices when the
        # main thread is free and we are going to start graping if there
        # is a new device

        self.Devices:list[CameraDevice, AudioDevice] = []
        


        self.ImageArray = []

        self.initCaptureDevice()
        time.sleep(2)
        #self.Test()



        pass

    def initCaptureDevice(self):
        CaptureDevicesNames:list[str] = DevicesGraper.AvailableDevices.GrapCaptureDeviecesListffmpeg() # grap the name of all  the capture dvices
        for Index, DeviceName in enumerate(CaptureDevicesNames): # loop through the names to check if we already have them
            for Object in self.Devices: # this loop through the devices we already have
                if Object.Running and Object.Name == DeviceName: # check if teh device is running and we have the name
                    CaptureDevicesNames[Index] = None # if so make the name None so we cant create another one of them
                    break
                elif Object.Name == DeviceName: # if the devices name is not running but still exist
                    Object = CameraDevice(Index, DeviceName) # we can rerun it
                    CaptureDevicesNames[Index] = None # then we can remove if so it is does not have to be re ran with the ones that we have no data on
                    break


        for Index, DeviceName in enumerate(CaptureDevicesNames): # simply loop through hte names back and run the ones that made it through 
            if DeviceName != None: # if the value is none that means it is already running and working else go through the if statement
                self.Devices.append(
                    CameraDevice(Index, DeviceName) # we intialte the camera and append it to the array that contain all the input devices
                )

        print(self.Devices)


    def Test(self):
        timer = time.time() + 15
        fps = 30

        while True:
            self.ImageArray.append(self.Devices[0].DeviceOutput)
            time.sleep(1/fps)
            if time.time() > timer:
                break


        print(len(self.ImageArray))
        print("Test Done")





