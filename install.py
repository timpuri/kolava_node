import sys
from settings import Settings

class Module():
    def __init__(self, *args, **kwargs):
        self.parent = kwargs["parent"]
        self.settings = kwargs["settings"]


class Installer():
    def __init__(self, *args, **kwargs):
        print("Starting installer...")
        settings = Settings()

        from wifi import Wifi
        w=Wifi(parent=self,settings=settings.modules[0]["settings"])
        w.connect()

    def wifi_on_connect_callback(self):
        try:
            import uasyncio
        except ImportError:
            print("asyncio package not installed, installing")
            import upip
            upip.install(['micropython-uasyncio'])

    def call_callbacks(self, callback_name, **kwargs):
        if hasattr(self,callback_name):
            cb = getattr(self,callback_name)
            cb(**kwargs)

i=Installer()
