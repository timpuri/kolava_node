from __main__ import Module
import machine
from aswitch import Switch
import uasyncio as asyncio

class OnOffSwitch(Module):
    def __init__(self, *args, **kwargs):
        print("Initializing switch")
        super().__init__(*args, **kwargs)

        self.switch_state = None
        self.pin = machine.Pin(self.settings["pin"], machine.Pin.IN)
        self.switch_state = int(not self.pin.value())
        self.switch = Switch(self.pin)
        
        if self.settings["invert_switch"] == False:
            self.switch_off_func = self.switch_off
            self.switch_on_func = self.switch_on
        else:
            self.switch_off_func = self.switch_on
            self.switch_on_func = self.switch_off
        
        self.switch.close_func(self.switch_on_func)
        self.switch.open_func(self.switch_off_func)

    def switch_on(self):
        self.switch_state = 1
        self.parent.call_callbacks("switch_on_callback")

    def switch_off(self):
        self.switch_state = 0
        self.parent.call_callbacks("switch_off_callback")

    def after_init_callback(self,*args,**kwargs):
        if self.switch_state == 1:
            self.parent.call_callbacks("switch_on_callback")
        else:
            self.parent.call_callbacks("switch_off_callback")