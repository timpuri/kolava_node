from __main__ import DigitalOutput
import machine

class Relay(DigitalOutput):
    def __init__(self, *args, **kwargs):
        print("Initializing Relay")
        super().__init__(*args, **kwargs)

    def set_status(self,status):
        super().set_status(status)

    def mqtt_on_message_received(self,**kwargs):
        if kwargs["topic"] == "set_power":
            self.set_status(int(kwargs["msg"]))

    def led_on_change_callback(self,**kwargs):
        self.set_status(kwargs["value"])