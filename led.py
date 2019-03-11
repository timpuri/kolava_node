import utime
import machine

class Led():
    def __init__(self, parent, settings):
        print("Initializing Led")
        self.settings = settings
        self.parent = parent
        self.current_status = False
        
        self.led = machine.Pin(self.settings["pin"], machine.Pin.OUT)
        
    def blink_led(self):
        print("Blinking led")
        for i in range(1,10):
            self.set_led(True,False)
            utime.sleep(0.1)
            self.set_led(False,False)
            utime.sleep(0.1)
            
        self.set_led(self.current_status,False)

    def set_led(self, value, call_callback = True):
        self.led.value(int(value))
        self.current_status = value
        if call_callback:
            self.parent.call_callbacks("led_on_change_callback",value=value)

    def servo_on_change_callback(self,**kwargs):
        if kwargs["position"] > 1:
            self.set_led(True)
        else:
            self.set_led(False)

    def mqtt_on_message_received(self,**kwargs):
        if kwargs["topic"] == "blink_led":
            self.blink_led()
            
    def mqtt_on_connect_callback(self,**kwargs):
        self.blink_led()
