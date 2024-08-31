import numpy as np
import threading
import pyaudio





class AccessSounds:
    def __init__(self, input_device_index=None, output_device_index=None)-> None: # the input devices are intergers which are the index to input and output devices


        self.CHUNK:int = 128 # this represent the number of frequency we record in each chunk(array)
        self.FORMAT:int = pyaudio.paInt32 # this int is spcial because it is only 32 bits
        self.CHANNELS:int = 1 # one entry point for the audio
        self.RATE:int = 44100 # this is the rate the aduio will be captured as so make sure it is lower than what the device can capture
        self.Player = pyaudio.PyAudio() #this create the audio device

        #for further understanding on between each value of the Chunk there is a delay which depends on the Chunk/Rate/Channels
        #formula:
        #          (Total Number Of Sample) / ( (Sample Rate)*(Number Of Chanlles) ) = Total Duration


        self.stream = self.Player.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            output=True,
            frames_per_buffer=self.CHUNK,
            input_device_index=input_device_index,
            output_device_index=output_device_index
        )# we simply open a stream to prepare it to capture data



        self.GraperContinuouslyState:bool = False # this will tell us if we are captureing audio already
        self.WritingData:bool = False # this var will help us to know when the data is being written so we dont try to use the data while it is being written
                                      # this could cuz errors as if data is being copyed while being written the data that is copyed is most like currupted
        
        self.DataOutput:list[np.int32] = ... # here we make the var for storing the chunk temprearly so we can use it later 

    def GrapSound(self)->list[np.int32]: # this data type is a formate that we use to the chunk it is a list with integers which represenetd by 32 bit values  in memory
        if not self.GraperContinuouslyState: #we should not be able to capture the data twice at the same time if you want to do that just capture it using the GrapSoundContinuously function
            try:
                data = np.frombuffer(self.stream.read(self.CHUNK), dtype=np.int32)
                return data
            except:
                return None
            


    def Play(self, data:list[np.int32])->None: # this function will take the data we get from the GrapSound function and will play the sound using the output device
                                               # make sure that you have the correct output deveice
        self.stream.write(data.tobytes())


    def GrapSoundContinuously(self) -> None: # this function will get the Chunks and will store them in a spereate place we can access them and this function should be ran on a thread
        self.GraperContinuouslyState = True #setting this function to False will terminalte this function running
        while self.GraperContinuouslyState:
            try:
                data = np.frombuffer(self.stream.read(self.CHUNK), dtype=np.int32) # this will grap the data
                self.WritingData = True  # this will change the bool to True so we can use it to know when we are writing data
                self.DataOutput = data   # this will move the data to the Output buffer
                self.WritingData = False # this will change the bool to False so we can tell the other function to copy the data if they want
            except:
                pass


    def GrapSoundContinuouslyOnThread(self) -> None: # this function will simply run the function above on a thread so it is not limmited by the 
                                                     # while loop unless you want to run it your self on a different threading or async library
        threading.Thread(target=self.GrapSoundContinuously).start()







    def Quite(self) -> None: # this function can be called by the user any time
        try:
            self.GraperContinuouslyState = False
            self.stream.stop_stream()
            self.stream.close()
            self.Player.terminate()
        except:
            pass



    def __exit__(self) -> None: # this Function will shut down everything this scrip initiate to achieve what it does
                                # this Function will be called before garbage collection any way
        try:
            self.GraperContinuouslyState = False
            self.stream.stop_stream()
            self.stream.close()
            self.Player.terminate()
        except:
            pass


if __name__ == '__main__':
    x = AccessSounds()
    while True:
        x.Play(x.GrapSound())