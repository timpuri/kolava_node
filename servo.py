from __main__ import Pwm
import machine

class Servo(Pwm):
    def __init__(self, *args, **kwargs):
        print("Initializing servo")
        super().__init__(*args, **kwargs)

        self.current_position = self.settings["default_position"]
        self.timer = machine.Timer(self.settings["timer_id"])
        self.wakeup()
        self.set_position(self.current_position)

    def set_position(self,position):
        print("Setting servo position to {}".format(position))
        
        if position not in range(0,101):
            print("Value error, position should be betweet 0 and 100")
            return False

        self.wakeup()
        duty = int(self.settings["closed_duty"]+(((self.settings["open_duty"]-self.settings["closed_duty"])/100)*position))
        self.pwm.duty(duty)
        self.current_position = position

        self.timer.init(period=self.settings["idle_time"], mode=machine.Timer.ONE_SHOT, callback=self.sleep)
        
        self.on_change(self.current_position)

    def on_change(self,position):
        self.parent.call_callbacks("servo_on_change_callback",position=position)
        if hasattr(self.parent, "mqtt"):
            self.parent.mqtt.publish("kolava/"+self.parent.mqtt.settings["client_name"]+"/valve_position", position, True)

    def mqtt_on_connect_callback(self,**kwargs):
        self.parent.call_callbacks("servo_on_change_callback",position=self.current_position)

    def mqtt_on_message_received(self,**kwargs):
        if kwargs["topic"] == "set_valve":
            self.set_position(int(kwargs["msg"]))

    def button_on_pressed_callback(self,**kwargs):
        if self.current_position > 1:
            self.set_position(0)
        else:
            self.set_position(100)

    def button_period_on_change_callback(self,**kwargs):
        if kwargs["state"] == 1 and self.current_position == 0:
            self.set_position(100)
        elif self.current_position > 0:
            self.set_position(0)

    def __del__(self):
        self.timer.deinit()