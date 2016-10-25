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
    if not PREFS.get(message.data['room_id'], "active", False):
        return

    try:
        LISTENERS.execListeners(message)

        if not isinstance(message, chatexchange6.events.MessagePosted):
            return

        content = HTMLParser.HTMLParser().unescape(message.content)
        user = message.user

        if WolfUtils.isCommand(content):
            cmd = WolfUtils.parseCommand(content)[0]
            args = WolfUtils.parseCommand(content)[1]
            print("Got command " + cmd + " with args " + str(args))
            COMMANDS.execute(message, cmd, args)
            #message.message.reply("User " + user.name + " sent command " + command + " with args " + " ".join(args))

    except Exception:
        print("Ow! Ran into a problem. Log follows:")
        traceback.print_exc()
        message.message.reply("Uh oh! I ran into a problem :(. See the console for more details.")

print("WolfBot loading... please wait.")

try:
    input = raw_input
except NameError:
    pass

# Handle setup first.
__USER__ = PREFS.get("global", "username", None)
__PASS__ = PREFS.get("global", "password", None)

if __USER__ is None:
    __USER__ = input("Please enter the e-mail to use: ")
    PREFS.set("global", "username", __USER__)
    __PASS__ = getpass.getpass("Please enter the password to use: ")
    PREFS.set("global", "password", __PASS__)
    PREFS.save()

if PREFS.get("global", "devs", []) == []:
    ckey = "%06x" % random.randint(0, 0xFFFFFF)
    PREFS.set("global", "captain_key", ckey)
    print("Please run this command to gain superuser privileges (single-use!):\n\n " + WolfUtils.CMD_DELIM + "iamthecaptainnow " + ckey.upper() + "\n\n")
    

# Register the Client to be used
client = chatexchange6.Client('stackexchange.com')
client.login(__USER__, __PASS__)

# Get the Bot itself
me = client.get_me()

SESSION_STORAGE.set("bot_username", me.name.replace(" ", ""))
SESSION_STORAGE.set("bot_id", client._br.user_id)

allRooms = PREFS.all()

if len(allRooms) == 1:
    PREFS.set("1", "active", True)

for room in allRooms:
    if room == "global":
        continue

    if PREFS.get(room, "active", True) and not PREFS.get(room, "banned", False):
        PREFS.set(room, "active", True)
        print("Updated room ID " + str(room) + " to new prefs format. It is now Active.")
    else:
        continue

    # Bind the user to the chat room
    roomObject = client.get_room(room)
    roomObject.join()
    print("Joined room " + str(roomObject.id))
    roomWatcher = roomObject.watch(on_message)

    oldRoomlist = SESSION_STORAGE.get("in_rooms", [])
    oldRoomlist.append(roomObject)
    SESSION_STORAGE.set("in_rooms", oldRoomlist)

print("WolfBot (named " + SESSION_STORAGE.get("bot_username") + ") online.")

while True:
    time.sleep(1)
    TASKS.runTasks()

PREFS.save()
client.logout()
