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

    def get(self, chat, key, default=None):
        """
        Retrieve the value for the provided key in chat. Return None if the
        key or chat does not exist.
        """
        try:
            return self._prefs[str(chat)][key]
        except KeyError:
            return default

    def exists(self, chat, key):
        if (self.get(chat, key) is None):
            return False

        return True

    def set(self, chat, key, value):
        """
        Set the value for the provided key in chat, creating objects as needed.
        """
        c = self._prefs.get(str(chat), {})
        c[key] = value
        self._prefs[str(chat)] = c
        self.save()

    def delete(self, chat, key):
        c = self._prefs.get(str(chat), {})
        c.pop(key, None)
        self.save()

    def purgeChat(self, chat):
        self._prefs.pop(str(chat), None)
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
                    # Init default prefs
                    self.set("global", "command_delimiter", "!!/")
                    self.set("global", "reply_delimiter", "%")
        except IOError:
            self._prefs = {}
            # Init default prefs
            self.set("global", "command_delimiter", "!!/")
            self.set("global", "reply_delimiter", "%")

    def save(self):
        """
        Save preferences from the file.
        """
        with open('config/prefs.json', 'w') as f:
            f.write(json.dumps(self._prefs, sort_keys=True))

    def all(self):
        return self._prefs

class SessionStorage:
    """
    Object used for storing preferences.
    """

    def __init__(self):
        self._prefs = {}

    def __len__(self):
        return len(self._prefs)

    def __getitem__(self, chat):
        return self._prefs.get(str(chat), {})

    def get(self, key, default=None):
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
        
    def delete(self, key):
        c = self._prefs
        c.pop(key, None)
        
    def all(self):
        return self._prefs


SESSION_STORAGE = SessionStorage()
PREFS = Prefs()
PREFS.load()
