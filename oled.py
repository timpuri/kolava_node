from __main__ import Module
import machine
import ssd1306
import utime

class Oled(Module):
    def __init__(self, *args, **kwargs):
        print("Initializing SSD1306 OLED Display")
        super().__init__(*args, **kwargs)
        self.text_buffer=self.empty_text_buffer()
        i2c = machine.I2C(-1, machine.Pin(self.settings["scl_pin"]), machine.Pin(self.settings["sda_pin"]))
        self.oled = ssd1306.SSD1306_I2C(self.settings["width"], self.settings["height"], i2c)
        self.startup_screen()
        

    def empty_text_buffer(self):
        if self.settings["height"] > 63:
            return ["","","","","",""]
        else:
            return ["","",""]

    def startup_screen(self):
        if hasattr(self.parent, "mqtt"):
            nodename=self.parent.mqtt.settings["client_name"]
        else:
            nodename=""

        self.oled.fill(1)
        self.oled.show()
        utime.sleep(0.7)

        self.add_text_row("Kolava Node")
        self.add_text_row(nodename)
        self.add_text_row("is starting up")

    def clear_buffer(self):
        self.text_buffer = self.empty_text_buffer()

    def add_text_row(self, row="", clear_buffer=False):
        if clear_buffer:
            self.clear_buffer()
            self.text_buffer[len(self.text_buffer)-1] = row
        else:
            for i,r in enumerate(self.text_buffer):
                if i < len(self.text_buffer)-1:
                    self.text_buffer[i] = self.text_buffer[i+1]
                else:
                    self.text_buffer[i] = row

        self.text()

    def text(self,rows=None):
        if rows == None:
            rows = self.text_buffer
        
        self.oled.fill(0)
        y=0
        for row in self.text_buffer:
            self.oled.text(row, 0, y)
            y=y+10
        self.oled.show()

    def display_add_row_callback(self,row=""):
        self.add_text_row(row)

    def after_init_callback(self,*args,**kwargs):
        self.add_text_row("Modules loaded")

    def wifi_on_connect_callback(self,**kwargs):
        self.add_text_row("WiFi connected")

    def mqtt_on_connect_callback(self,**kwargs):
        self.add_text_row("MQTT connected")

    def mqtt_on_message_received(self,**kwargs):
        if kwargs["topic"] == "set_screen_row":
            self.add_text_row(str(kwargs["msg"]))

        if kwargs["topic"] == "set_screen_text":
            self.clear_buffer()
            for row in str(kwargs["msg"]).split(";"):
                self.add_text_row(row)