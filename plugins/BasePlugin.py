import os
import sys
import signal

import WolfUtils
from WolfPlugin import registerCommand, registerTask

from WolfPrefs import PREFS

from plugins import __init__ as PluginInit


# Privilege Escalation
@registerCommand("addadmin", "Add an Admin to the system.", "", {"superuserNeeded": True})
def addadmin(message, args):
    if len(args) == 0 or len(args) > 1:
        message.message.reply("One argument (user_id) needed!")
        return None

    currentAdmins = PREFS.get("admins", [])
    if args[0] not in currentAdmins:
        currentAdmins.append(args[0])
        PREFS.set("admins", currentAdmins)
        message.message.reply("User ID " + args[0] + " added as bot admin.")
        return None
    else:
        message.message.reply("User is already a declared admin!")
        return None
    
@registerCommand("deladmin", "Add an Admin to the system.", "", {"superuserNeeded": True})
def addadmin(message, args):
    if len(args) == 0 or len(args) > 1:
        message.message.reply("One argument (user_id) needed!")
        return None

    currentAdmins = PREFS.get("admins", [])
    if args[0] in currentAdmins:
        currentAdmins.remove(args[0])
        PREFS.set("admins", currentAdmins)
        message.message.reply("User ID " + args[0] + " removed from bot admin.")
        return None
    else:
        message.message.reply("User is not a declared admin! (This command may not be used to remove inherited rights)")
        return None
        
@registerCommand("setprefix", "Change the bot prefix", "", {"superuserNeeded": True})
def setprefix(message, args):
    if len(args) > 1:
        message.message.reply("One argument (prefix) needed!")
        return None

    if len(args) == 0:
        PREFS.set("command_delimiter", "!!/")
        WolfUtils.CMD_DELIM = "!!/"
        message.message.reply("Prefix reset to default of `!!/`.")
    else:
        PREFS.set("command_delimiter", args[0])
        WolfUtils.CMD_DELIM = args[0]
        message.message.reply("Prefix set to `" + args[0] + "`.")
        
@registerCommand("reload", "Reload the bot", "<prefs|commands|all>", {"superuserNeeded": True})
def reload(message, args):
    if len(args) > 1:
        message.message.reply("Zero or one argument (reloadtype (prefs, commands, all)) needed!")
    
    if len(args) == 0:
        reloadType = "all"
    else:
        reloadType = args[0]
        
    if reloadType == "prefs":
        PREFS.load()
        message.message.reply("**Preference reload complete.**")
    elif reloadType == "plugins":
        reload(WolfCore)
        message.message.reply("**Plugin reload complete.**")
    elif reloadType == "all":
        PREFS.load()
        os.execl(sys.executable, sys.executable, *sys.argv)
        message.message.reply("**Full reload complete.**")
        
@registerCommand("restart", "Restart the bot", "", {"superuserNeeded": True})
def restart(message = None, args = None):
    os.execl(sys.executable, sys.executable, *sys.argv)
    
@registerCommand("stop", "Stop the bot", "", {"superuserNeeded": True})
def stop(message = None, args = None):
    os.kill(os.getpid(), signal.SIGTERM)
    
    
@registerCommand("iamthecaptainnow", "Become a Developer", "", {})
def takeRoot(message, args):
    if len(args) != 1:
        message.message.reply("Needs one argument (captain_key)")

    currentDevs = PREFS.get("devs", [])
    
    if currentDevs == []:
        if args[0].lower() == PREFS.get("captain_key").lower():
            currentDevs.append(str(message.data['user_id']))
            PREFS.set("devs", currentDevs)
            message.message.reply("https://i.imgur.com/2oNMYD3.jpg")
            PREFS.delete("captain_key")
            PREFS.save()
        else:
            message.message.reply("You are by far the worst captain I've ever heard of.")
    else:
        message.message.reply("You are by far the worst captain I've ever heard of.")
