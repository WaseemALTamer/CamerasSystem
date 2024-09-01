from Controller import Controller
import threading

x = Controller()


x.initCaptureDevice()

threading.Thread(target=x.RecordPhotoageForAllCameras).start()


while True:
    input("")
    x.initCaptureDevice()