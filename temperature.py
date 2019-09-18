from __main__ import Module
import machine
from time import sleep
import onewire, ds18x20

class Temperature(Module):
    def __init__(self, *args, **kwargs):
        print("Initializing DS18x20 temperature sensor")
        super().__init__(*args, **kwargs)

        self.dallas = ds18x20.DS18X20(onewire.OneWire(machine.Pin(self.settings["pin"])))
        self.sensors = self.dallas.scan()
        print('Found temperature sensors: ', self.sensors)

    def temperature(self):
        self.dallas.convert_temp()
        sleep(0.75)
        return self.dallas.read_temp(self.sensors[0])

    def publish_temperature(self):
        temperature = self.temperature()
        print("Temperature: {}".format(temperature))

        if hasattr(self.parent, "mqtt"):
            self.parent.mqtt.publish("kolava/" + self.parent.mqtt.settings["client_name"] + "/temperature", str(temperature), True)

    def publish_period_time(self):
        if hasattr(self.parent, "mqtt"):
            self.parent.mqtt.publish("kolava/" + self.parent.mqtt.settings["client_name"] + "/period_time", str(self.settings["period_time"]), False)

    def mqtt_on_message_received(self,**kwargs):
        if kwargs["topic"] == "get_temperature":
            self.publish_temperature()
        if kwargs["topic"] == "set_period_time":
            try:
                new_period_time = int(kwargs["msg"])
                self.settings["period_time"] = new_period_time
            except:
                print("Invalid new period time {}, needs to be integer.".format(kwargs["msg"]))
            self.publish_period_time()
        if kwargs["topic"] == "get_period_time":
            self.publish_period_time()

    def period_on_period_callback(self, **kwargs):
        if kwargs["period_no"] % int(self.settings["period_time"]) == 0:
            self.publish_temperature()
