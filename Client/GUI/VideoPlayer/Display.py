# this file is going to contain the  main Display Window
# which links all the  classes and  widgets  togather to
# achieve  Displaying  the content and data we have this
# file is  desgined  to only carry  out one scene if you
# want more scences then  you  can  write  another  file 
# which this file transtion to when you finish from this
# window you can also detect the events from  the  other
# file for efficiancy







from VideoPlayerPG import VideoPlayer
from TickSystem import FpsController
import threading
import pygame
import time




class MainWindow:
    def __init__(self,
                 Width:int=1280,
                 Height:int=720,
                 DesiredFps:int=120
                 
                 ) -> None: # This functions will only contain Public Varables
                            # to interact with the gui

        self.Resloution:list[int,int] = [Width,Height] # we keep it in an array so all classes 
                                                       # have access to it when it is passed down

        self.Window:pygame.display.Surface = None
        self.State:bool = False

        self.Frame_Rate_Controller:FpsController = FpsController(DesiredFps)
        
        self.Player:VideoPlayer = None # this is a weigit it is in the init file to make you aware of it
        
        self.Weigits:list[bool] = []


    def InitializeWindow(self):
        pygame.init()
        self.Window = pygame.display.set_mode(self.Resloution, pygame.RESIZABLE)

        self.Player:VideoPlayer = VideoPlayer(self.Window, 
                                              WindowResloution=self.Resloution, 
                                              VideoDirecotry="1080p.mp4",
                                              relheight=1,
                                              relwidth=1,
                                              relx=0.5,
                                              rely=0.5,
                                              anchor="CENTER"
                                              ) # intialise the Weigit
        
        self.Weigits.append(self.Player) # lets store it in the weigits array so we keep track of
                                         # it

        pygame.display.set_caption("VideoPlayer")


    def MainLoop(self):



        self.State = True
        while self.State:

            # We go through the Weigits and update them one by one
            # this ensures that we give each and every weigit time
            # to process the changes they  have while  not  having
            # them run on a sepereate therad it is the  weigit job
            # to make sure they are efficient enough for the while
            # script
             
            for Weigit in self.Weigits:
                Weigit.Update()



            # this handles the events
            for event in pygame.event.get():

                # the close button event 
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.State = False
                    break

                # window resize event
                elif event.type == pygame.VIDEORESIZE:
                    # Update the display surface to the new size
                    self.Resloution[0], self.Resloution[1] = event.size[0], event.size[1] # this will update the resloution for everything

                for Weigit in self.Weigits: # pass the event it to the weigit for interaction with the weigits
                    Result = Weigit.EventHandeler(event) # store the result of the event
                    if Result: # if the event result is true that means it belongs to that weigit
                        break




                pygame.display.update() #Update the window when ever there is event

            for Weigit in self.Weigits: # check if any of the  Weigit  Scheduled an update
                                        # this is important because we dont want to update
                                        # when we dont have to for prfomance it is  eaiser
                                        # to check all the Weigits and children Weigits we
                                        # have rather than updating it when we  dont  have
                                        # to as nothing would have changed this may be not
                                        # efficant later on down the line  if  you  create
                                        # more than 1000 Weigits for example  
                if Weigit.UpdateScheduled and self.State:
                    pygame.display.update()
                    Weigit.UpdateScheduled = False
                    break

            
            self.Frame_Rate_Controller.BlockUntilNextFrame()





def StartPlaying(x):

    x.InitializeWindow()
    x.MainLoop()

if __name__ == "__main__":
    x = MainWindow()
    threading.Thread(target=StartPlaying, args=(x,)).start() # this is how you start the
    time.sleep(5)
    x.State = False
    

    
    #x.MainLoop()