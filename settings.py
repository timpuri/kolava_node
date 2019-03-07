import ujson

class Settings():
    def __init__(self):
        try:
            with open("settings.json", "r") as entry:
                data = ujson.load(entry)
                for k, v in data.items():
                    setattr(self, k, v)
        except OSError as ex:
            print("Error({0}) when opening settings.json: {1}".format(ex.errno, ex.strerror))
        else:
            entry.close()
            