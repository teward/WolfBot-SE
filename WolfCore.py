import ChatExchange6.chatexchange6 as chatexchange6
import time
import HTMLParser
import getpass

import WolfUtils

from WolfPrefs import PREFS
from WolfPlugin import COMMANDS
from WolfPlugin import TASKS

from plugins import *

def on_message(message, client):
    if not isinstance(message, chatexchange6.events.MessagePosted):
        return

    content = HTMLParser.HTMLParser().unescape(message.content)
    user = message.user
    
    #print("Got message:\n" + str(message.data))

    if WolfUtils.isCommand(content):
        cmd = WolfUtils.parseCommand(content)[0]
        args = WolfUtils.parseCommand(content)[1]
        print("Got command " + cmd + " with args " + " ".join(args))
        COMMANDS.execute(message, cmd, args)
        #message.message.reply("User " + user.name + " sent command " + command + " with args " + " ".join(args))

try:
    input = raw_input
except NameError:
    pass

# Handle setup first.
__USER__ = PREFS.get("username", None)
__PASS__ = PREFS.get("password", None)
__CHATID__ = PREFS.get("chat_id", None)

if __USER__ is None:
    __USER__ = input("Please enter the e-mail to use: ")
    PREFS.set("username", __USER__)
    __PASS__ = getpass.getpass("Please enter the password to use: ")
    PREFS.set("password", __PASS__)
    PREFS.save()

if __CHATID__ is None:
    __CHATID__ = input("Please enter the Chat to join: ")
    PREFS.set("chat_id", __CHATID__)
    PREFS.save()

# Register the Client to be used
client = chatexchange6.Client('stackexchange.com')
client.login(__USER__, __PASS__)

# Get the Bot itself
me = client.get_me()

# Bind the user to the chat room
room = client.get_room(__CHATID__)
room.join()
room.watch(on_message)
print("Ready for commands")

while True:
    time.sleep(1)
    TASKS.runTasks(room)

PREFS.save()
client.logout()
