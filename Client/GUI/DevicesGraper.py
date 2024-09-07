import subprocess
import cv2




#this class is to mostly graps data about the input devices like camera and microphone
class AvailableDevices:



    #=====================================Functions to grap devices names================================ this uses ffmpeg



    def detect_ffmpeg_devices()->str: # this output a string text run " ffmpeg -list_devices true -f dshow -i dummy " in terminal
                                      # to check what the string formate is


        """ this function will simulate a terminal Command and will return the value
            it will run a ffmpeg command for input devices detection note that the
            data should be further extracted to end up with a list of devices that we
            can use this will be mostly used to extract the names rather than the index
            mostly for the use of ffmpeg to record data with audio and video with the
            avalable input devices """



        # Run the FFmpeg command to list video and audio devices
        command:list[str] = ['ffmpeg', '-list_devices', 'true', '-f', 'dshow', '-i', 'dummy']
        
        # Run the command and capture the output
        result:subprocess.CompletedProcess = subprocess.run(command, stderr=subprocess.PIPE, text=True)
        
        # Print the result
        ffmpeg_output:str = result.stderr  # FFmpeg outputs the device list to stderr
        return ffmpeg_output



    def extract_devices_names(ffmpeg_terminal_text:str) -> list[ list[str], list[str]]: # this function will return the video devices and audio devices
                                                                                        # respectivly by taking the ffmpeg output 


        # Parse the output for video and audio devices
        video_devices:list[str] = [] 
        audio_devices:list[str] = []
        lines:list[str] = ffmpeg_terminal_text.split('\n')


        for line in lines:
            if "(video)" in line: # Check if the line has (video) as (video) indecate it is a camera device 

                # the Lines we want will be like <[dshow @ 00000000029100a0]  "Microphone (USB Audio Device)" (video)>
                # we simply need to strip the name by finding the first '"' and the second ' " ' and taking what ever is
                # inside


                start:str = line.find('"') 
                result:str = line[start + 1:] # the one is added because we need to get rid of the ' " ' as well
                end:str = result.rfind('"')
                result:str = result[:end]

                video_devices.append(result) # we append the result and move to the next line if there is
                continue
                
            
            if "(audio)" in line:

                # same thing is happening in the if statment as before

                start = line.find('"')
                result = line[start + 1:]
                end = result.rfind('"')
                result = result[:end]

                audio_devices.append(result)
                continue

        return [video_devices, audio_devices] # we return the names of the video devices and the audio devices we access them by [0]
                                              # for video and [1] for audio



    # this function will return the names of the Devices avalibale you can also run the two functions above sepretly to achieve the same results
    def GrapDevicesNames() -> list[list[str], list[str]]: # this function will just use the first two functions the to grap the data
                                                           # and extract the data
        return AvailableDevices.extract_devices_names(AvailableDevices.detect_ffmpeg_devices())


    #=====================================End of Functions to grap devices names================================ feel free to re use the functions
        



    #=====================================Functions to grap devices Index====================================== these functions will extract information for cv2 
    #                                                                                                           library for cameras mostly


    def GrapCaptureDeviecesIndexCv2(max_devices=4) -> list[int]: # his function searches for input devices through there index
                                                              # if it is not avalibel nothing happen if it is we just record
                                                              # the index very simple function but it needs imporvement down
                                                              # the line
        available_devices:list[int] = []
        
        for i in range(max_devices):  # iterate through the devices that we want it to look for we sat a max of 4 devices to look for
            cap = cv2.VideoCapture(i) # it tryes to acces the device
            if cap.isOpened():        # if it success then we can just append the index 
                # If statment has worked the camera opens successfully consider it available because it was opened
                available_devices.append(i)
                cap.release()# we have to release it so it does not stay open this
            else:
                break # if we did not go through that means that there is no cameras that are avalibe after it


        # plz who ever is working on this function or will use this function imporve it make it faster
        # most of the time the cameras will be one after the other so dont make it check for no reason
        # also can you make that such that it does not have to open the camera

        return available_devices


    def GrapCaptureDeviecesListffmpeg() -> list[str]: # this function is going to return hash map with the index as a key with the data of 
                                                                 # camera, this function is mainly writen for pure profermence so we not have to worry
                                                                 # about speed cuz we are using a hash map

                                                                 
        """ this function will be using the prevouse function that have been
            writen for capturing input device from from the ffmpeg command
            check the previous functions to know how it works """


        CaptureDevieces:list[str] = AvailableDevices.GrapDevicesNames()[0]
        CaptureDeviecesNum:int = len(CaptureDevieces) # this line will capture all the video and audio input devices extract the
                                                      # the capture devices number



        # this function may not work on different systems this is mainly is used for proformance to extract how many video capture devices we have
        # and the names of the capture devices the names may not be in the correct index so if that the case we need to fix that later on somehow
        return CaptureDevieces
