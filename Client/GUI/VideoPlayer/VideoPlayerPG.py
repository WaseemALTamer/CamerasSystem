# this module is going to be resposnable for the interface and 
# the video getting displayed on the pygame window to









from VideoGraper import Graper
from SliderPG import Slider
import numpy as np
import pygame
import os




class VideoPlayer():
    def __init__(self,PygameWindow,
                 VideoDirecotry:str=None,
                 VideoPlayRate:float=None,
                 WindowResloution:list[int,int]=[1280,720],
                 relheight:float=1, # one being the whole width of the paerent weiget
                 relwidth:float=1,  # one being the whole width of the paerent weiget
                 relx:float=0,
                 rely:float=0,
                 anchor:str="NW",
                 MasterPos:list[int,int]=[0,0], # this is used if the Weigit was a Child weigit
                 ) -> None:

        self.PygameWindow = PygameWindow

        self.VideoDirecotry:str = VideoDirecotry
        self.VideoPlayRate:float = VideoPlayRate
        self.WindowResloution:list[int,int] = WindowResloution
        self.relwidth:float = relwidth
        self.relheight:float = relheight
        self.relx:float = relx
        self.rely:float = rely
        self.anchor:str = anchor
        self.MasterPos = MasterPos

        self.Resloution:list[int,int] = [self.Width, self.Heigth] # we calcalate the resloution
        self.CurrentPostion:list[int,int] = [self.Postion[0], self.Postion[1]]

        





        self.UpdateScheduled:bool = False # this will tell the main loop that we need new update
                                          # so the loop can update whenever  everything is ready


        self.ChildWeigits:pygame.display.Surface = []


        # this part of the code is responsible of intiating the video
        self.VideoGraper:Graper = None
        self.CurrentPygameFrameSurface:pygame.display.Surface = None

        if VideoDirecotry:
            self.LoadVideo(VideoDirecotry) # this passes the video data to the graper

        self.SliderBar:Slider = None


        






    @property
    def Width(self) -> int:
        return round(self.relwidth*self.WindowResloution[0])

    @property
    def Heigth(self) -> int:
        return round(self.relheight*self.WindowResloution[1])

    @property
    def _anchorDict(self) -> dict[str:tuple[int,int]]:
        return {
            "N": (-(self.Width//2), 0),
            "W": (0,-(self.Heigth//2)),
            "E": (-self.Width,-(self.Heigth//2)),
            "S": (-(self.Width//2),self.Heigth),
            "NW": (0,0),
            "NE": (-self.Width,0),
            "SW": (0,-self.Heigth),
            "SE": (-self.Width,-self.Heigth),
            "CENTER": (-(self.Width//2), -(self.Heigth//2))
        }


    @property
    def Postion(self) -> tuple[int,int]:
        Width = self.WindowResloution[0]
        Height = self.WindowResloution[1]

        AnchorDisplacement = self._anchorDict[self.anchor]

        Width =(self.relx * Width) + AnchorDisplacement[0] + self.MasterPos[0]
        Height =(self.rely * Height) + AnchorDisplacement[1] + self.MasterPos[1]

        return (Width, Height)





    def LoadVideo(self, Path:str) -> None:
        self.VideoDirecotry = Path # update the path of the video

        for i in range (len(self.ChildWeigits)): # remove th sliders or anything that it has
            self.ChildWeigits.pop(i) # this ensures that we only have the parent wiegets which
                                     # is only the videoplayer

        # we Initiate the Graper if there is a Direcotry given and it is avalibale
        if os.path.exists(Path):
            self.VideoGraper = Graper()
            if self.VideoPlayRate:
                self.VideoGraper.Frame_Rate_Scaler = self.VideoPlayRate # we want to pass how fast we we want the video speed
                                                                        # note if your pc is already bottle necked then there
                                                                        # this  wont work  and it  is  adviced  to update the
                                                                        # frame blocker in the Graper file we  also  need  to
                                                                        # pass the rate before we play the file




            self.VideoGraper.load(Path) # this will pass the video direcotry to the graper
                                        # so we can play the video

            # we now create the slider for the video because it is a local data
            self.SliderBar = Slider(
                self.PygameWindow,
                VideoGraper=self.VideoGraper,
                WindowResloution=self.Resloution,
                MasterPos = self.CurrentPostion,
                relheight=0.05,
                relwidth=1,
                relx=0.5,
                rely=1,
                anchor="S"

            )
            self.ChildWeigits.append(self.SliderBar)


        else:
            print("File Path provided does not exist")



    def EventHandeler(self, Event:pygame.event) -> bool: # this function should be ran when there is an event
                                                         # the main point of this function is to  process the
                                                         # event and pass them to the children Weigit

        # we need to pass the outcome to the Children before we  process it
        # this is because the event may be for the child this is determined
        # through the cursor postion  this  should  only  occure if it is a
        # cursor event 

        if Event.type == pygame.VIDEORESIZE:
            self.Resloution[0], self.Resloution[1] = self.Width, self.Heigth
            self.CurrentPostion[0], self.CurrentPostion[1] = self.Postion[0], self.Postion[1]

        if Event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION, pygame.VIDEORESIZE]: # if the event has to do with the mouse then pass the event to it
            for Weigit in self.ChildWeigits: # pass the event to the child and see if it belongs to the child
                Result = Weigit.EventHandeler(Event) # store the result of the event
                if Result: # if the event result is true that means it belongs to that weigit
                    return True


        # if the event is not for the children then it may be for the parent so we check that as well
        if Event.type == pygame.MOUSEMOTION:
            if self.CursorInWeigit(Event.pos): # check if the Cursor is inside the weigit
                return True # we return true to tell the main loop that that event belong to this weigit


        if Event.type == pygame.MOUSEBUTTONUP:
            if self.CursorInWeigit(Event.pos): # check if the Cursor is inside the weigit

                if self.VideoGraper and self.VideoDirecotry: # if there a video then we can play the video
                    if self.VideoGraper._paused:
                        self.VideoGraper.play()
                    else:
                        self.VideoGraper.pause()
            
                return True

        return False # we return false to tell the main loop that this event is not for us
                     # or this weigit children


    def Update(self) -> None: 
                      # this  function  should be put into
                      # the while loop in the main Display
                      # file it will update the widget and
                      # load the  next  frame  if avalible
                      # this function  should only process
                      # the image when  it  have  to do so
                      # for proformance

        # we can check if we have a new frame and display the frame if we do
        # we store its content so we dont have to repossess the frame again
        if self.VideoGraper and self.VideoGraper._image_ready:
            self.VideoGraper._image_ready = False
            self.CurrentPygameFrameSurface = pygame.surfarray.make_surface(np.transpose(self.VideoGraper._current_img , (1, 0, 2)))
            pygame_surface = pygame.transform.scale(self.CurrentPygameFrameSurface, (self.Width, self.Heigth))
            self.PygameWindow.blit(pygame_surface, self.Postion)
            self.UpdateScheduled = True
        else: # the else is only if the other weigets want the window updated
            if self.CurrentPygameFrameSurface:
                pygame_surface = pygame.transform.scale(self.CurrentPygameFrameSurface, (self.Width, self.Heigth))
                self.PygameWindow.blit(pygame_surface, self.Postion)
                # note we will not call the update Function

        for Weigit in self.ChildWeigits:
            Weigit.Update() # we give the child time to processes it self
            if Weigit.UpdateScheduled: # now we can check if any other child weigets want to Scheduled and update
                self.UpdateScheduled = True # set the parent to tell the Main window to Schedul and update




    def CursorInWeigit(self, CursorPos:tuple[int,int]) -> bool:
        CurrentPos = self.Postion
        if (CursorPos[0] >= CurrentPos[0]) and (CursorPos[1] >= CurrentPos[1]) and  (CursorPos[0] <= CurrentPos[0] + self.Width) and (CursorPos[1] <= CurrentPos[1] + self.Heigth):
            return True
        return False


























