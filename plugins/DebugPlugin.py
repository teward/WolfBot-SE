import WolfUtils
from WolfPlugin import registerCommand, registerTask

from WolfPrefs import PREFS

@registerCommand("start", "Get started with WolfBot!", "", {})
def start(message, args):
    message.message.reply("Hi there! Welcome to WolfBot!")
    
@registerCommand("whoami", "Get user information.", "", {})
def whoami(message, args):
    uid = message.data['user_id']
    username = message.data['user_name']
    
    isDev = WolfUtils.isDeveloper(uid)
    isMod = WolfUtils.isSEModerator(uid)
    isAdm = WolfUtils.isAdmin(uid)
    isRO  = WolfUtils.isRoomOwner(uid)
    
    message.message.reply("You are: " + username + " (ID: " + str(uid) + ")" + \
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
