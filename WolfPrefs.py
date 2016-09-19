from shutil import copyfile
import json

class Prefs:
    """
    Object used for storing preferences.
    """

    def __init__(self):
        self._prefs = {}

    def __len__(self):
        return len(self._prefs)

    def __getitem__(self, chat):
        return self._prefs.get(str(chat), {})

    def get(self, key, default = None):
        """
        Retrieve the value for the provided key in chat. Return None if the
        key or chat does not exist.
        """
        try:
            return self._prefs[key]
        except KeyError:
            return default

    def exists(self, key):
        if (self.get(key) is None):
            return False

        return True

    def set(self, key, value):
        """
        Set the value for the provided key in chat, creating objects as needed.
        """
        c = self._prefs
        c[key] = value
        self._prefs = c
        self.save()
        
    def delete(self, key):
        c = self._prefs
        c.pop(key, None)
        self.save()
        
    def load(self):
        """
        Load preferences from the file.
        """
        try:
            with open('config/prefs.json', 'r') as f:
                try:
                    self._prefs = json.loads(f.read())
                except ValueError:
                    self._prefs = {}
        except IOError:
            print("No prefs file found, making default!")
            self._prefs = {}
            self.set("command_delimiter", "!!/")
            print("[Prefs] Set Command String to !!/")
            self.set("reply_delimiter", "%")
            print("[Prefs] Set Reply String to %")
            self.save()
            print("[Prefs] Default preferences saved.")

    def save(self):
        """
        Save preferences from the file.
        """
        with open('config/prefs.json', 'w') as f:
            f.write(json.dumps(self._prefs, sort_keys=True))

    def all(self):
        return self._prefs


PREFS = Prefs()
PREFS.load()
