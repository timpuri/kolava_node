from __main__ import Module
import machine

class Period(Module):
    def __init__(self, *args, **kwargs):
        print("Initializing Periodical")
        super().__init__(*args, **kwargs)

        self.period_no = 0
        self.timer = machine.Timer(self.settings["timer_id"])

    def run_period(self,timer=None):
        if self.period_no > 86400:
            self.period_no = 0

        self.period_no += 1
        self.parent.call_callbacks("period_on_period_callback",period_no=self.period_no)

    def mqtt_on_connect_callback(self,**kwargs):
        self.timer.init(period=1000, mode=machine.Timer.PERIODIC, callback=self.run_period)

    def __del__(self):
        print("Cleaning Period class instance")
        self.timer.init(callback=None)
        self.timer.deinit()