import network
import machine

class Wifi():
    def __init__(self, parent, settings):
        print("Initializing WiFi")
        self.parent = parent
        self.settings = settings

        self.nic = network.WLAN(network.STA_IF)

        self.timer = machine.Timer(self.settings["timer_id"])

    def start_connection_checker(self):
        self.timer.init(mode=machine.Timer.ONE_SHOT, period=self.settings["timer_interval"], callback=self.check_connection)

    def check_connection(self, timer):
        if not self.nic.isconnected():
            self.start_connection_checker()
        else:
            self.parent.call_callbacks("wifi_on_connect_callback")

    def connect(self):
        self.nic.active(True)
        self.nic.connect(self.settings["ssid"], self.settings["psk"])
        self.start_connection_checker()

    def after_init_callback(self,*args,**kwargs):
        self.connect()