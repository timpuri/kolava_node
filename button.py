from __main__ import Module
import machine
from aswitch import Pushbutton

class Button(Module):
    def __init__(self, *args, **kwargs):
        print("Initializing button")
        super().__init__(*args, **kwargs)

        self.pin = machine.Pin(self.settings["pin"], machine.Pin.IN)
        self.pushbutton = Pushbutton(self.pin)
        self.pushbutton.press_func(self.button_pressed)

    def button_pressed(self, timer=None):
        print("Button pressed")
        self.parent.call_callbacks("button_on_pressed_callback")