# this file is responsable for the slider which tells 
# you where in the video you  are and lets you change
# the time you are at








from VideoGraper import Graper
import pygame







class Slider:
    def __init__(self,PygameWindow,
                 VideoGraper:Graper=None,
                 WindowResloution:list[int,int]=[1280,720],
                 relheight:float=1, # one being the whole width of the paerent weiget
                 relwidth:float=1,  # one being the whole width of the paerent weiget
                 relx:float=0,
                 rely:float=0,
                 anchor:str="NW",
                 MasterPos:list[int,int]=[0,0], # this is used if the Weigit was a Child weigit
                 ) -> None:
        
        self.PygameWindow = PygameWindow

        self.VideoGraper:Graper = VideoGraper
        self.WindowResloution:list[int,int] = WindowResloution
        self.relwidth:float = relwidth
        self.relheight:float = relheight
        self.relx:float = relx
        self.rely:float = rely
        self.anchor:str = anchor
        self.MasterPos = MasterPos

        self.Resloution:list[int,int] = [0,0]





        self.UpdateScheduled:bool = False # this will tell the main loop that we need new update
                                          # so the loop can update whenever  everything is ready

        # this is where all the surfaces and the Objects for the silder are going to be intiated  and  made
        # all that is left is dispalying them at the right place and keeping track on when they are clicked 
        # and draged good luck to you cuz you fucking need it

        self.Alpha = 255 # this will be generalised for all the weigets in the slider


        
        self.SliderFrameSurface = None
        self.ProgressBarFrame = None
        self.ProgressOnBar = None

        self.InitiateSurfaces()






    @property
    def SliderColor(self) -> list[int,int,int,int]:
        _alpha = self.Alpha//2
        if _alpha <= 0:
            _alpha = 0
            
        return [50, 50, 50, _alpha]



        












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
            "S": (-(self.Width//2),-self.Heigth),
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




    def InitiateSurfaces(self):
        self.SliderFrameSurface = pygame.Surface((self.Width, self.Heigth), pygame.SRCALPHA)
        self.ProgressBarFrame = pygame.Rect(0,self.Heigth//2 , self.Width , 5)





    def EventHandeler(self, Event:pygame.event) -> bool: # this function should be ran when there is an event
                                                         # the main point of this function is to  process the
                                                         # event and pass them to the children Weigit

        if Event.type == pygame.VIDEORESIZE:
            self.InitiateSurfaces()

        if Event.type == pygame.MOUSEMOTION:
            return self.CursorInWeigit(Event.pos)
            
        elif Event.type == pygame.MOUSEBUTTONUP:
            return self.CursorInWeigit(Event.pos)

        return False # we return false to tell the main loop that this event is not for us
                     # or this weigit children



    def Update(self) -> None: # for the slider we just want to update the postion of the 
                              # knob every second the event Handeler is responsable  for
                              # the interaction with it the Update sohuld only blit them
                              # you should not always schedul an update because most  of
                              # the time you dont need it


        
        self.SliderFrameSurface.fill(self.SliderColor)


        

        pygame.draw.rect(self.SliderFrameSurface, [255,255,255,255], pygame.Rect(0,self.Heigth//2 , self.Width , 5))

        self.PygameWindow.blit(self.SliderFrameSurface, (self.Postion[0], self.Postion[1]))

        print(self.Postion)

        self.UpdateScheduled = True
        pass


    def CursorInWeigit(self, CursorPos:tuple[int,int]) -> bool:
        CurrentPos = self.Postion
        if (CursorPos[0] >= CurrentPos[0]) and (CursorPos[1] >= CurrentPos[1]) and  (CursorPos[0] <= CurrentPos[0] + self.Width) and (CursorPos[1] <= CurrentPos[1] + self.Heigth):
            return True
        return False
