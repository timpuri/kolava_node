import sys
from settings import Settings


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
                setattr(self,module["__instance"],module["__class__"](self,module["settings"]))                        
            except Exception as e:
                sys.print_exception(e)
                print("Failed to initialize module {}: {}".format(module["__module"],e))
                if hasattr(self, module["__instance"]):
                    delattr(self, module["__instance"])
                    pass
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