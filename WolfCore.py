# -*- encoding: utf-8 -*-

import ChatExchange6.chatexchange6 as chatexchange6
import time
import HTMLParser
import getpass
import random
import traceback

import WolfUtils

from WolfPrefs import PREFS
from WolfPrefs import SESSION_STORAGE
from WolfPlugin import COMMANDS
from WolfPlugin import TASKS
from WolfPlugin import LISTENERS

from plugins import *

def on_message(message, client):

    LISTENERS.execListeners(message)

    if not isinstance(message, chatexchange6.events.MessagePosted):
        return

    content = HTMLParser.HTMLParser().unescape(message.content)
    user = message.user

    if WolfUtils.isCommand(content):
        cmd = WolfUtils.parseCommand(content)[0]
        args = WolfUtils.parseCommand(content)[1]
        print("Got command " + cmd + " with args " + str(args))
        try:
            COMMANDS.execute(message, cmd, args)
        except Exception:
            print("Ow! Ran into a problem. Log follows:")
            traceback.print_exc()
            message.message.reply("Uh oh! I ran into a problem :(. See the console for more details.")
        #message.message.reply("User " + user.name + " sent command " + command + " with args " + " ".join(args))

print("WolfBot loading... please wait.")

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
    
if PREFS.get("devs", []) == []:
    ckey = "%06x" % random.randint(0, 0xFFFFFF)
    PREFS.set("captain_key", ckey)
    print("Please run this command to gain superuser privileges (single-use!):\n\n /iamthecaptainnow " + ckey.upper() + "\n\n")
    

# Register the Client to be used
client = chatexchange6.Client('stackexchange.com')
client.login(__USER__, __PASS__)

# Get the Bot itself
me = client.get_me()

SESSION_STORAGE.set("bot_username", me.name.replace(" ", ""))
SESSION_STORAGE.set("bot_id", client._br.user_id)

# Bind the user to the chat room
room = client.get_room(__CHATID__)
room.join()

roomWatcher = room.watch(on_message)
print("WolfBot online.")

while True:
    time.sleep(1)
    TASKS.runTasks(room)

PREFS.save()
client.logout()
