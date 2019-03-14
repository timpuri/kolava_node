import machine
import utime

class Ldr():
    def __init__(self, parent, settings):
        print("Initializing LDR sensor")
        self.settings = settings
        self.parent = parent

        self.value_changed = True
        self.ldr = machine.ADC(machine.Pin(self.settings["pin"]))
        self.ldr.atten(eval(self.settings["attenuation"]))
        self.last_value = self.read_status()

    def read_status(self):
        value = self.ldr.read()
        #print("Ldr read status value: {}".format(value))
        return True if value > self.settings["thresold"] else False

    def check_if_changed(self):
        status_now = self.read_status()
        if status_now != self.last_value:
            if self.value_changed == True:
                self.on_value_changed(status_now)
                self.value_changed = False
                self.last_value = status_now
            else:
                print("Verifying light status change after recheck_time..")
                self.value_changed = True
                utime.sleep_ms(self.settings["recheck_time"])
                self.check_if_changed()
        else:
            self.value_changed = False

    def on_value_changed(self, new_value):
        print("Ldr status changed to {}".format(new_value))
        if hasattr(self.parent, "mqtt"):
            self.parent.mqtt.publish("kolava/"+self.parent.mqtt.settings["client_name"]+"/light_status", new_value, True)

    def mqtt_on_connect_callback(self,**kwargs):
        self.on_value_changed(self.last_value)

    def period_on_period_callback(self,**kwargs):
        if divmod(kwargs["period_no"],int(self.settings["period_time"]))[1] == 0:
            self.check_if_changed()