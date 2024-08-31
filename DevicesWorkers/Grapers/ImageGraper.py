import numpy as np
import threading
import cv2



# this function should be rewriten for the Linux or spicifcaly for the raspberry pi who evr is writing this should
# plz Keep the Structure and architecture the same if you have better methode than this we can discuss it before we
# rewrite the code if you want to use a faster library then you can just keep the structure the same so we can

class AccessImages():
    def __init__(self, input_device_index) -> None:
        self.cap:cv2.VideoCapture = cv2.VideoCapture(input_device_index) # we try to open the camera stright away so we can capture the photage
        if not self.cap.isOpened(): # we check if the camera is opened if it did not then we have a issue and raise and error
            raise "Cannot open camera The camera either does not exist or other device is using it" #this might need to be changed later on

        self.GraperContinuouslyState:bool = False # this will tell us if we are captureing image already
        self.WritingData:bool = False # this var will help us to know when the data is being written so we dont try to use the data while it is being written
                                      # this could cuz errors as if data is being copyed while being written the data that is copyed is most like currupted

        self.DataOutput:list[np.uint8] = ... # here we make the var for storing the chunk temprearly so we can use it later


    def StartGraping(self):
        self.GraperContinuouslyState = True
        while self.GraperContinuouslyState:
            # Check if the camera is still open
            if not self.cap.isOpened():
                print("Camera is disconnected or not accessible.")
                self.GraperContinuouslyState = False  # Exit the loop
                break

            # Try to grab a frame
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to grab a frame. Camera may be disconnected.")
                self.GraperContinuouslyState = False  # Exit the loop
                break

            # When the frame is successfully captured
            self.WritingData = True
            self.DataOutput = frame  # Store the frame in the shared variable
            self.WritingData = False  # Reset the flag after writing the data
            
        # After the loop ends, release the camera resources
        self.cap.release()
        print("Stopped grabbing images and camera released.")


    def GrapImageContinuouslyOnThread(self) -> None: # this function will simply run the function above on a thread so it is not limmited by the 
                                                     # while loop unless you want to run it your self on a different threading or async library
        threading.Thread(target=self.StartGraping).start()


    def Quite(self) -> None: # this function can be called by the user any time
        try:
            self.GraperContinuouslyState = False
            self.cap.release() # this function will close the channal that connects to the camera
        except:
            pass



    def __exit__(self) -> None: # this Function will shut down everything this scrip initiate to achieve what it does
                                # this Function will be called before garbage collection any way
        try:
            self.GraperContinuouslyState = False
            self.cap.release() # this function will close the channal that connects to the camera
        except:
            pass