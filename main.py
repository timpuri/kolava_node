import sys
from settings import Settings
import machine

# Basic module
class Module():
    def __init__(self, *args, **kwargs):
        self.parent = kwargs["parent"]
        self.settings = kwargs["settings"]

# Digital output
class DigitalOutput(Module):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_status = None
        if "default_state" in self.settings:
            default_state = int(self.settings["default_state"])
        else:
            default_state = 0
        self.output = machine.Pin(self.settings["pin"],machine.Pin.OUT,value=default_state)

    def set_status(self,status):
        self.output.value(int(status))
        self.current_status = status

    def get_status(self):
        self.current_status = self.output.value()
        return self.current_status

# PWM output
class Pwm(Module):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def wakeup(self):
        self.pin = machine.Pin(self.settings["pin"])
        self.pwm = machine.PWM(self.pin,freq=self.settings["frequency"])

    def sleep(self, timer=None):
        print("Setting pwm to sleep")
        self.pwm.deinit()

# Analog input
class Adc(Module):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.adc = machine.ADC(machine.Pin(self.settings["pin"]))
        
        if hasattr(self.settings["attenuatiossssssn"]):
            self.adc.atten(eval(self.settings["attenuation"]))

# Main program
class KolavaNode():
    def __init__(self):
        self.s = Settings()
        self.initialized_classes = []

        # Import and initialize modules defined in settings
        for module in self.s.modules:
            print("Initializing module {}".format(module))
            try:
                import_module_code = "from {} import {}".format(module["__module"],module["__class"])
                print(import_module_code)
                exec(import_module_code)
            except Exception as e:
                sys.print_exception(e)
                print("Failed to import module {}: {}".format(module["__module"],e))
                continue

            try:
                module["__class__"] = globals()[module["__class"]]
                setattr(self,module["__instance"],module["__class__"](parent=self,settings=module["settings"]))                        
            except Exception as e:
                sys.print_exception(e)
                print("Failed to initialize module {}: {}".format(module["__module"],e))
                if hasattr(self, module["__instance"]):
                    delattr(self, module["__instance"])
                continue

            self.initialized_classes.append(module["__instance"])
            print("Successfully initialized class {}".format(module["__class"]))

        self.call_callbacks("after_init_callback")

    def call_callbacks(self,callback_name, **kwargs):
        print("Calling callbacks: {}".format(callback_name))
        for instance in self.initialized_classes:
            if hasattr(getattr(self,instance),callback_name):
                cb = getattr(getattr(self,instance),callback_name)
                print("Calling callback {}.{}".format(instance,callback_name))
                print(kwargs)
                cb(**kwargs)

kolavanode = KolavaNode()