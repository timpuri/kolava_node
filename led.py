import utime
import machine

class Led():
    def __init__(self, parent, settings):
        print("Initializing Led")
        self.settings = settings
        self.parent = parent

        self.led = machine.Pin(self.settings["pin"], machine.Pin.OUT)
        
        # Blinking led when initializing
        for i in range(1,10):
            self.set_led(True,False)
            utime.sleep(0.2)
            self.set_led(False,False)
            utime.sleep(0.05)

    def set_led(self, value, call_callback = True):
        self.led.value(int(value))
        if call_callback:
            self.parent.call_callbacks("led_on_change_callback")

    def servo_on_change_callback(self,**kwargs):
        if kwargs["position"] > 1:
            self.set_led(True)
        else:
            self.set_led(False)