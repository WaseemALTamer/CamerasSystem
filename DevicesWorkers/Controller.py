# this file is responsable to use the Grapers library to start
# collecting image data from all the different cameras avalible
# this will file will also keep the Photoage of the image for 
# and attempt to store them after 15 seconds this should be 
# able to handel all the Captures devices that we have for 
# starters it is fine if we only save the data without turnning
# it into .mp4 or .avi formates


from Grapers import DevicesGraper, ImageGraper, SoundGraper
import numpy as np


# this class will be used as the structure class
class CameraDevice:
    def __init__(self) -> None:
        self.Name:str
        self.Device: ...
        self.DeviceOutput:list[np.uint8]
        # note that the index of the camera
        # will not be stored this is because
        # camera index is not set on stone






class Controller():
    def __init__(self) -> None:

        # we are giong to grap all the input devices we can for starters
        # can keep track of everything we have avalible we should also
        # try to detect if there is anything that was pluged in so we
        # can use it for its inputs so here is what we are going to do
        # we are going to keep checking for any input devices when the
        # main thread is free and we are going to start graping if there
        # is a new device





        pass