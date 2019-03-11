import machine

class Button():
    def __init__(self, parent, settings):
        print("Initializing button")
        self.settings = settings
        self.parent = parent

        self.debounce_timer = machine.Timer(self.settings["timer_id"])
        self.button = machine.Pin(self.settings["pin"], machine.Pin.IN, machine.Pin.PULL_UP)
        self.button.irq(trigger=machine.Pin.IRQ_FALLING, handler=self.button_debounce)

    def button_debounce(self, pin):
            self.debounce_timer.init(mode=machine.Timer.ONE_SHOT, period=self.settings["debounce_time"], callback=self.button_pressed)

    def button_pressed(self, timer=None):
        print("Button pressed")
        self.parent.call_callbacks("button_on_pressed_callback")

    def __del__(self):
        self.debounce_timer.deinit()