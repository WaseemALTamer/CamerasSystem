# this file is responsable for the slider which tells 
# you where in the video you  are and lets you change
# the time you are at








from VideoGraper import Graper
import pygame
import time







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

        self.MaxAlpha = 170
        self.Alpha = 170 # this will be generalised for all the  weigets in the slider
        
        self.BeforeFadingTime = 1 # this timer will be responsable for telling the functions
                                  # how many seconds it will take until the slider  start to
                                  # disappear

        self.AlphaTranstionTime = 0.2 # this timer will be responsable for the Alpha going
                                      # from what it is to 0

        self.CurosorNotMovedTime = 3



        self.BeforeFadingTimer = time.time() + self.BeforeFadingTime
        self.AlphaTranstionTimer = time.time() + self.AlphaTranstionTime
        self.CurosorNotMovedTimer = time.time() + self.CurosorNotMovedTime

        self.CurosrDidNotMovedForTime = False
        


        self.CursorOnSliderFrame = False
        
        
        self.SliderFrameSurface = None


        self.ProgressBarFrame = None
        self.ProgressOnBar = None
        self.ProgressBarWidth = None
        self.ProgressPressed = False

        self.InitiateSurfaces()








    @property
    def ProgressBarFrameDimentions(self) -> list[int,int,int,int]:
        _width = (self.Width - 20)
        Dimention = [(self.Width//2)-(_width//2), self.Heigth//2 , _width, 5]
        return Dimention


    @property
    def SliderColor(self) -> list[int,int,int,int]:
        _alpha = self.Alpha//2
        if _alpha <= 0:
            _alpha = 0
        return [50, 50, 50, _alpha]

    @property
    def ProgressBarFrameColor(self) -> list[int,int,int,int]:
        return [80, 80, 80, self.Alpha]
    
    @property
    def ProgressBarColor(self) -> list[int,int,int,int]:
        return [255, 0, 0, self.Alpha]











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
        self.ProgressBarFrame = pygame.Rect(self.ProgressBarFrameColor)





    def EventHandeler(self, Event:pygame.event) -> bool: # this function should be ran when there is an event
                                                         # the main point of this function is to  process the
                                                         # event and pass them to the children Weigit

        if Event.type == pygame.VIDEORESIZE:
            self.InitiateSurfaces()

        elif Event.type == pygame.MOUSEMOTION:

            if self.CursorInWeigit(Event.pos):
                if not self.CursorOnSliderFrame:
                    self.CursorOnSliderFrame = True
                    self.AlphaTranstionTimer = time.time() + self.AlphaTranstionTime

                if self.CurosrDidNotMovedForTime: 
                    self.CurosorNotMovedTimer = time.time() + self.CurosorNotMovedTime
                    self.CurosrDidNotMovedForTime = False
                    self.AlphaTranstionTimer = time.time() + self.AlphaTranstionTime
            else:
                if self.CursorOnSliderFrame:
                    self.CursorOnSliderFrame = False
                    self.BeforeFadingTimer = time.time() + self.BeforeFadingTime
                    self.AlphaTranstionTimer = time.time() + self.AlphaTranstionTime + self.BeforeFadingTime
                    

            if self.ProgressPressed:
                _Dimentions =  self.ProgressBarFrameDimentions
                self.VideoGraper._time_stamp = self.VideoGraper._duration * ((Event.pos[0] - _Dimentions[0])/ (_Dimentions[2]))
                self.UpdateScheduled = True
            return self.CursorInWeigit(Event.pos)
                  
        elif Event.type == pygame.MOUSEBUTTONDOWN:
            if not self.ProgressPressed and self.CursorInProgreessFrame(Event.pos):
                _Dimentions =  self.ProgressBarFrameDimentions
                self.VideoGraper._time_stamp = self.VideoGraper._duration * ((Event.pos[0] - _Dimentions[0])/ (_Dimentions[2]))
                self.UpdateScheduled = True

                self.VideoGraper.pause()
                self.ProgressPressed = True

        elif Event.type == pygame.MOUSEBUTTONUP:
            if self.ProgressPressed:
                _Dimentions =  self.ProgressBarFrameDimentions
                _Sec = self.VideoGraper._duration * ((Event.pos[0] - _Dimentions[0])/ (_Dimentions[2]))
                if _Sec <= 0:
                    _Sec = 0

                self.VideoGraper.seek(int(_Sec))
                self.ProgressPressed = False

                self.VideoGraper.play()
            return self.CursorInWeigit(Event.pos)

        
        return False # we return false to tell the main loop that this event is not for us
                     # or this weigit children



    def Update(self) -> None: # for the slider we just want to update the postion of the 
                              # knob every second the event Handeler is responsable  for
                              # the interaction with it the Update sohuld only blit them
                              # you should not always schedul an update because most  of
                              # the time you dont need it


        # those if statemnts are responsable for disapearing the slider and reapearing the slider when you hover over it
        if (self.BeforeFadingTimer < time.time() and not self.CursorOnSliderFrame) or self.CurosorNotMovedTimer <= time.time():
            if not self.CurosrDidNotMovedForTime:
                self.CurosrDidNotMovedForTime = True
                self.AlphaTranstionTimer = time.time() + self.AlphaTranstionTime
            if self.AlphaTranstionTimer >= time.time():

                _diff = self.AlphaTranstionTimer - time.time()
                _diff = (_diff / self.AlphaTranstionTime)
                _alpha = self.MaxAlpha * _diff

                if self.Alpha >= _alpha:
                    self.Alpha = self.MaxAlpha * _diff
                    self.UpdateScheduled = True

        if self.CursorOnSliderFrame and not self.CurosrDidNotMovedForTime:
            if self.AlphaTranstionTimer >= time.time():

                _diff = self.AlphaTranstionTimer - time.time()
                _diff = 1 - (_diff / self.AlphaTranstionTime)
                _alpha = self.MaxAlpha * _diff

                if self.Alpha <= _alpha:
                    self.Alpha = self.MaxAlpha * _diff
                    self.UpdateScheduled = True
        #=============================================


        self.SliderFrameSurface.fill(self.SliderColor)
        _ProgressFrameDimentions = self.ProgressBarFrameDimentions
        pygame.draw.rect(self.SliderFrameSurface, self.ProgressBarFrameColor, _ProgressFrameDimentions) #Draw the frame of the progress bar
        # we now draw the Porgress on the frame
        if self.VideoGraper._time_stamp and self.VideoGraper._duration:
            _ProgressFrameDimentions[2] *= (self.VideoGraper._time_stamp/self.VideoGraper._duration) # we access the width of the progress frame 
                                                                                                     # and  change  it to the presentange of the
                                                                                                     # progress that we have but  only  if  they
                                                                                                     # ready to access the duration and stamp
        pygame.draw.rect(self.SliderFrameSurface, self.ProgressBarColor, _ProgressFrameDimentions)
        _pos = self.Postion
        self.PygameWindow.blit(self.SliderFrameSurface, (_pos[0], _pos[1])) # draw the main frame of the slider



    def CursorInWeigit(self, CursorPos:tuple[int,int]) -> bool:
        CurrentPos = self.Postion
        if (CursorPos[0] >= CurrentPos[0]) and (CursorPos[1] >= CurrentPos[1]) and  (CursorPos[0] <= CurrentPos[0] + self.Width) and (CursorPos[1] <= CurrentPos[1] + self.Heigth):
            return True
        return False
    
    def CursorInProgreessFrame(self, CursorPos):
        _WeigitPos = self.Postion
        _Dimention = self.ProgressBarFrameDimentions
        _Dimention[0] = _WeigitPos[0] + _Dimention[0] # this gets the absolute width relitive to the weiget
        _Dimention[1] = _WeigitPos[1] + _Dimention[1] # this gets the absolute height relitive to the weiget
        if (CursorPos[0] >= _Dimention[0]) and (CursorPos[1] >= _Dimention[1]) and  (CursorPos[0] <= _Dimention[0] + _Dimention[2]) and (CursorPos[1] <= _Dimention[1] + _Dimention[3]):
            return True
        

    def Transtion(self, Durtaion):
        pass