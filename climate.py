from __main__ import Module
import machine
import dht

class Climate(Module):
    def __init__(self, *args, **kwargs):
        print("Initializing DHT22 sensor sensor")
        super().__init__(*args, **kwargs)

        self.dht = dht.DHT22(machine.Pin(self.settings["pin"]))

    def mqtt_on_connect_callback(self, **kwargs):
        self.publish()

    def period_on_period_callback(self, **kwargs):
        if kwargs["period_no"] % int(self.settings["period_time"]) == 0:
            self.publish()

    def publish(self):
        self.dht.measure()
        temp = self.dht.temperature()
        humid = self.dht.humidity()

        print("Temperature: {} Humidity: {}".format(temp, humid))

        if hasattr(self.parent, "mqtt"):
            self.parent.mqtt.publish("kolava/" + self.parent.mqtt.settings["client_name"] + "/temperature", str(temp), True)
            self.parent.mqtt.publish("kolava/" + self.parent.mqtt.settings["client_name"] + "/humidity", str(humid), True)
