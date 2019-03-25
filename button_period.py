from __main__ import Module
import machine

class ButtonPeriod(Module):
    def __init__(self, *args, **kwargs):
        print("Initializing button")
        super().__init__(*args, **kwargs)

        self.button_state = None
        self.button = machine.Pin(self.settings["pin"], machine.Pin.IN)

    def get_value(self):
        return int(not self.button.value())

    def check_if_changed(self):
        state_now = self.get_value()
        if self.get_value() != self.button_state:
            print("Button state changed to {}".format(state_now))
            self.button_state = state_now
            self.parent.call_callbacks("button_period_on_change_callback",state=state_now)

    def period_on_period_callback(self,**kwargs):
        if divmod(kwargs["period_no"],int(self.settings["period_time"]))[1] == 0:
            self.check_if_changed()