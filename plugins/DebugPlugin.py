import WolfUtils
from WolfPlugin import registerCommand, registerTask

from WolfPrefs import PREFS
from WolfPrefs import SESSION_STORAGE


@registerCommand("start", "Get started with WolfBot!", "", {})
def start(message, args):
    message.message.reply("Hi there! Welcome to " + SESSION_STORAGE.get("bot_username") + "!")
    
@registerCommand("whoami", "Get user information.", "", {})
def whoami(message, args):
    uid = message.data['user_id']
    username = message.data['user_name']
    room = message.data['room_id']
    
    isDev = WolfUtils.isDeveloper(uid)
    isMod = WolfUtils.isSEModerator(uid)
    isAdm = WolfUtils.isAdmin(uid, room)
    isRO  = WolfUtils.isRoomOwner(uid,room)
    
    message.message.reply("You are: " + username + " (ID " + str(uid) + ")" + \
    "\nIs Bot Superuser (Grants Bot Admin): " + str(isDev) + \
    "\nIs Bot Admin: " + str(isAdm) + \
    "\nIs SE Mod (Grants Superuser): " + str(isMod) + \
    "\nIs Room Owner (Grants Bot Admin): " + str(isRO))

# Privilege Test Commands
@registerCommand("regusertest", "Check for user powers.", "", {})
def regUserTest(message, args):
    message.message.reply("User command executed successfully.")
    
@registerCommand("admintest", "Check for admin powers.", "", {"adminNeeded": True})
def adminTest(message, args):
    message.message.reply("Awooooo!")
    
@registerCommand("superusertest", "Check for superuser powers.", "", {"superuserNeeded": True})
def superuserTest(message, args):
    message.message.reply("Superuser command executed successfully.")

@registerCommand("throwex", "Force an exception.", "", {"superuserNeeded": True})
def throwex(message, args):
    if len(args) == 0:
        msg = "The exception you requested..."
    else:
        msg = " ".join(args)

    raise RuntimeError(msg)
