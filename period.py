import machine

class Period():
    def __init__(self, parent, settings):
        print("Initializing Periodical")
        self.parent = parent
        self.settings = settings
        self.period_no = 0

        self.timer = machine.Timer(self.settings["timer_id"])

    def run_period(self,timer=None):
        if self.period_no > 999:
            self.period_no = 0

        self.period_no += 1
        self.parent.call_callbacks("period_on_period_callback",period_no=self.period_no)

    def mqtt_on_connect_callback(self,**kwargs):
        self.timer.init(period=1000, mode=machine.Timer.PERIODIC, callback=self.run_period)