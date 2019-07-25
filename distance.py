from __main__ import Module
import machine
from hcsr04 import HCSR04

class Distance(Module):
    def __init__(self, *args, **kwargs):
        print("Initializing distance")
        super().__init__(*args, **kwargs)
        self.sensor = HCSR04(trigger_pin=self.settings["trigger_pin"], echo_pin=self.settings["echo_pin"])

    def distance(self):
        return self.sensor.distance_cm()

    def publish_distance(self):
        distance = self.distance()
        print("Distance: {}".format(distance))

        if hasattr(self.parent, "mqtt"):
            self.parent.mqtt.publish("kolava/" + self.parent.mqtt.settings["client_name"] + "/distance", str(distance), True)

    def mqtt_on_message_received(self,**kwargs):
        if kwargs["topic"] == "get_distance":
            self.publish_distance()

    def period_on_period_callback(self, **kwargs):
        if kwargs["period_no"] % int(self.settings["period_time"]) == 0:
            self.publish_distance()
