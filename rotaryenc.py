from __main__ import Module
import machine
from rotary_irq_esp import RotaryIRQ
import uasyncio as asyncio

class RotaryEnc(Module):
    def __init__(self, *args, **kwargs):
        print("Initializing Rotary encoder")
        super().__init__(*args, **kwargs)

        self.r = RotaryIRQ(pin_num_clk=self.settings["clk_pin"],
              pin_num_dt=self.settings["dt_pin"],
              min_val=self.settings["min_val"],
              max_val=self.settings["max_val"],
              reverse=self.settings["reverse"],
              range_mode=eval(self.settings["range_mode"]))

        self.start()

    async def start(self):
        lastval = self.r.value()
        while True:
            val = self.r.value()
        
            if lastval != val:
                lastval = val
                self.parent.call_callbacks("display_add_row_callback",row=str(val))

            await asyncio.sleep_ms(50)

    def after_init_callback(self,*args,**kwargs):
        self.parent.loop.create_task(self.start())
