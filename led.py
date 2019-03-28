from __main__ import DigitalOutput
import utime
import machine

class Led(DigitalOutput):
    def __init__(self, *args, **kwargs):
        print("Initializing Led")
        super().__init__(*args, **kwargs)

        self.led = self.output
        
    def blink_led(self):
        print("Blinking led")
        for i in range(1,10):
            self.set_led(True,False)
            utime.sleep(0.1)
            self.set_led(False,False)
            utime.sleep(0.1)
            
        self.set_led(self.current_status,False)

    def set_led(self, value, call_callback = True):
        super().set_status(value)
        if call_callback:
            self.parent.call_callbacks("led_on_change_callback",value=value)

    def servo_on_change_callback(self,**kwargs):
        if kwargs["position"] > 1:
            self.set_led(True)
        else:
            self.set_led(False)

    def button_on_pressed_callback(self,**kwargs):
        if "toggle_from_button" in self.settings:
            if self.led.value() == 1:
                self.set_led(False)
            else:
                self.set_led(True)

    def mqtt_on_message_received(self,**kwargs):
        if kwargs["topic"] == "blink_led":
            self.blink_led()
            
    def mqtt_on_connect_callback(self,**kwargs):
        self.blink_led()
