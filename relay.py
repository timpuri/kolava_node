from __main__ import DigitalOutput
import machine

class Relay(DigitalOutput):
    def __init__(self, *args, **kwargs):
        print("Initializing Relay")
        super().__init__(*args, **kwargs)

    def set_status(self,status):
        super().change_status(status)
        if hasattr(self.parent, "mqtt"):
            self.parent.mqtt.publish("kolava/"+self.parent.mqtt.settings["client_name"]+"/power_status", str(bool(status)), True)

    def mqtt_on_message_received(self,**kwargs):
        if kwargs["topic"] == "set_power_off":
            self.change_status(False)
        elif kwargs["topic"] == "set_power_on":
            self.change_status(True)

    def led_on_change_callback(self,**kwargs):
        self.set_status(kwargs["value"])