import time
import calendar

from WolfPrefs import PREFS
import WolfUtils

class CommandManager:
    def __init__(self):
        self._commands = {}

    def register(self, function, commandName, helptext, helpargs, permset):
        self._commands[commandName] = {"function": function, "helptext": helptext, "helpargs": helpargs, "permset": permset}

    def deregister(self, commandName):
        del self._commands[commandName]

    def gethelp(self):
        return None
        # ToDo: Real help!

    def execute(self, message, commandName, args):
        room = str(message.data['room_id'])

        # Make sure the user isn't blacklisted from executing commands in that room
        if str(message.data['user_id']) in PREFS.get(room, "user_blacklist", []):
            return None

        # Make sure the user isn't blacklisted from executing commands globally
        if str(message.data['user_id']) in PREFS.get("global", "user_blacklist", []):
            return None
            
        # Verify that the command exists.
        try:
            command= self._commands[commandName.lower()]
        except KeyError:
            message.message.reply("The command " + WolfUtils.CMD_DELIM + commandName + " does not exist.")
            return None

        # Make sure the command isn't disabled in the room at hand.
        if commandName in PREFS.get(room, "disabled_commands", []):
            return None

        # Make sure the user is a superuser for superuser commands
        if command["permset"].get("superuserNeeded", False):
            if not WolfUtils.isDeveloper(message.data['user_id']):
                message.message.reply("This command needs to be run by a Superuser.")
                return None

        # Make sure the user is privileged enough to run this command
        if command["permset"].get("adminNeeded", False):
            if not WolfUtils.isAdmin(message.data['user_id'], room):
                message.message.reply("This command needs to be run by a Bot Admin.")
                return None

        # Make sure the room isn't on admin lockdown
        if (PREFS.get(room, "lockdown") and (not WolfUtils.isAdmin(message.data['user_id'], room))):
            return None

        command["function"](message, args)

    def all(self):
        return self._commands
        
class ScheduledTaskManager:
    def __init__(self):
        self._tasks = {}
    
    def register(self, function, name, runDelay):
        self._tasks[name] = {"function": function, "runDelay": runDelay, "lastRun": 0}
        
    def deregister(self, name):
        del self._tasks[name]
        
    def runTasks(self):
        for room in PREFS.all():
            if room == "global":
                continue

            # Skip room if we're in lockdown mode.
            if PREFS.get(room, "lockdown", False):
                continue

            for task in self._tasks:
                if str(task) in PREFS.get(room, "enabled_tasks", []):
                    taskEntry = self._tasks[task]
                    if (int(time.time()) - taskEntry["lastRun"]) >= taskEntry["runDelay"]:
                        # print("Running task " + task)
                        taskEntry["function"](room)
                        taskEntry["lastRun"] = calendar.timegm(time.gmtime())
                        # print("Finished task " + task)
                
class ListenerManager:
    def __init__(self):
        self._listeners = {}
    
    def register(self, function, name, eventId):
        self._listeners[name] = {"function": function, "eventId": eventId}
        
    def deregister(self, name):
        del self._listeners[name]
        
    def execListeners(self, message):
        eventId = int(message.data['event_type'])
        room = message.data['room_id']

        # Handle potential lockdown
        if (PREFS.get(room, "lockdown") and (not WolfUtils.isAdmin(message.data['user_id'], room))):
            return None

        for listenerName in self._listeners:
            listener = self._listeners[listenerName]
            if listener["eventId"] == eventId:
                listener["function"](message)
                
        
COMMANDS = CommandManager()
TASKS = ScheduledTaskManager()
LISTENERS = ListenerManager()

def registerCommand(name, helptext, helpargs, permset):
    def wrap(fn):
        # perform registration here
        # fn points to the function itself
        # fn.__name__ is the name of the function
        COMMANDS.register(fn, name, helptext, helpargs, permset)
        #print "Registered command " + WolfUtils.CMD_DELIM + name
    return wrap
    
def registerTask(name, runDelay):
    def wrap(fn):
        # perform registration here
        # fn points to the function itself
        # fn.__name__ is the name of the function
        TASKS.register(fn, name, runDelay)
        #print "Registered scheduled task " + name + ", to be run every " + str(runDelay) + " seconds."
    return wrap
    
def registerListener(name, eventId):
    def wrap(fn):
        # perform registration here
        # fn points to the function itself
        # fn.__name__ is the name of the function
        LISTENERS.register(fn, name, eventId)
        #print "Registered listener " + name
    return wrap
