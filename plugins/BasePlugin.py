import os
import sys
import signal
import WolfUtils

import ChatExchange6.chatexchange6 as chatexchange6

from WolfPlugin import registerCommand, registerTask, registerListener
from WolfPrefs import PREFS
from WolfPrefs import SESSION_STORAGE

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
        message.message.reply(WolfUtils.getName(args[0]) + " (ID  "+ args[0] + ") added as bot admin.")
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
        message.message.reply(WolfUtils.getName(args[0]) + " removed from bot admin.")
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
        
@registerCommand("setrprefix", "Change the bot reply prefix", "", {"superuserNeeded": True})
def setprefix(message, args):
    if len(args) > 1:
        message.message.reply("One argument (prefix) needed!")
        return None

    if len(args) == 0:
        PREFS.set("reply_delimiter", "%")
        WolfUtils.REPLY_DELIM = "%"
        message.message.reply("Prefix reset to default of `%`.")
    else:
        PREFS.set("reply_delimiter", args[0])
        WolfUtils.REPLY_DELIM = args[0]
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
        
@registerCommand("blacklist", "Block a user from using commands", "", {"adminNeeded": True})
def blacklistUser(message, args):
    if len(args) != 1:
        message.message.reply("Needs one argument (user_id)")
        
    user_to_bl = args[0]
    
    current_blacklist = PREFS.get("blacklist", [])
    if user_to_bl not in current_blacklist:
        if not WolfUtils.isAdmin(user_to_bl):
            current_blacklist.append(user_to_bl)
            PREFS.set("blacklist", current_blacklist)
            message.message.reply(WolfUtils.getName(user_to_bl) + " (ID  "+ user_to_bl + ") is no longer permitted to use WolfBot commands.")
        else:
            message.message.reply("Admins and Superusers may not be blacklisted.")
    else:
        message.message.reply("User is already blacklisted!")
        
@registerCommand("unblacklist", "Allow a user to use commands", "", {"adminNeeded": True})
def unblacklistUser(message, args):
    if len(args) != 1:
        message.message.reply("Needs one argument (user_id)")
        
    user_to_unbl = args[0]
    
    current_blacklist = PREFS.get("blacklist", [])
    if user_to_unbl in current_blacklist:
        current_blacklist.remove(user_to_unbl)
        PREFS.set("blacklist", current_blacklist)
        message.message.reply(WolfUtils.getName(user_to_unbl) + " (ID  "+ user_to_unbl + ") is now permitted to use WolfBot commands.")
    else:
        message.message.reply("User is already blacklisted!")
        
@registerListener("modtool-deletemsg", 18)
def listenerDeleteMessage(message):
    if message.data["content"] == "@" + SESSION_STORAGE.get("bot_username") + " " + WolfUtils.REPLY_DELIM + "d":
        if WolfUtils.isAdmin(message.data["user_id"]):
            chatexchange6.messages.Message(message.data["parent_id"], message.client).delete()
