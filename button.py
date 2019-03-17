from __main__ import Module
import machine
import utime

class Button(Module):
    def __init__(self, *args, **kwargs):
        print("Initializing button")
        super().__init__(*args, **kwargs)

        self.button = machine.Pin(self.settings["pin"], machine.Pin.IN)
        self.button.irq(trigger=eval(self.settings["trigger"]), handler=self.button_debounce)

    def button_debounce(self, pin):
        pin.irq(handler=None)
        self.button_pressed()
        utime.sleep_ms(self.settings["debounce_time"])
        pin.irq(trigger=eval(self.settings["trigger"]), handler=self.button_debounce)

    def button_pressed(self, timer=None):
        print("Button pressed")
        self.parent.call_callbacks("button_on_pressed_callback")