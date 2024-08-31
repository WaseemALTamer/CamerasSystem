class Device:
    def turn_on(self):
        print("Device is now on.")

class CameraDevice(Device):
    def take_picture(self):
        print("Picture taken.")



device = Device()
device.take_picture()  # This will raise an error