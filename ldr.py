import machine

class Ldr():
    def __init__(self, parent, settings):
        print("Initializing LDR sensor")
        self.settings = settings
        self.parent = parent

        self.value_changed = True
        self.ldr = machine.ADC(machine.Pin(self.settings["pin"]))
        self.ldr.atten(eval(self.settings["attenuation"]))
        self.last_value = self.read_status()
        self.timer = machine.Timer(self.settings["timer_id"])
        self.timer_start()

    def read_status(self):
        value = self.ldr.read()
        #print("Ldr read status value: {}".format(value))
        return True if value > self.settings["thresold"] else False

    def timer_callback(self,timer):
        status_now = self.read_status()
        if status_now != self.last_value:
            if self.value_changed == True:
                self.on_value_changed(status_now)
                self.value_changed = False
                self.last_value = status_now
            else:
                print("Verifying light status change after time_buffer..")
                self.value_changed = True
        else:
            self.value_changed = False

        self.timer_start()

    def timer_start(self):
        self.timer.init(mode=machine.Timer.ONE_SHOT, period=self.settings["time_buffer"], callback=self.timer_callback)

    def on_value_changed(self, new_value):
        print("Ldr status changed to {}".format(new_value))
        if hasattr(self.parent, "mqtt"):
            self.parent.mqtt.publish("kolava/"+self.parent.mqtt.settings["client_name"]+"/light_status", new_value)

    def mqtt_on_connect_callback(self,**kwargs):
        self.on_value_changed(self.last_value)

    def __del__(self):
        self.timer.deinit()