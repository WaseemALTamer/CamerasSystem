from Controller import Controller

x = Controller()

while True:
    input("Press enter to detect and run cameras: ")
    x.initCaptureDevice()