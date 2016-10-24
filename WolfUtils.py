# -*- coding: utf-8 -*-

from ChatExchange6 import chatexchange6 as chatexchange6
import json
import shlex
import sys
import requests
from urlparse import urlparse   
from urllib import urlopen
from datetime import datetime
import json

from WolfPrefs import PREFS

CMD_DELIM = PREFS.get("global", "command_delimiter", "!!/")
REPLY_DELIM = PREFS.get("global", "reply_delimiter", "%")

# Determine if a text is a command
#    Arg `message`: The text to check for commandiness
def isCommand(message):
    return message.startswith(CMD_DELIM)

def parseCommand(cmd):
    def newSplit(value):
        lex = shlex.shlex(value)
        lex.quotes = '"'
        lex.whitespace_split = True
        lex.commenters = ''
        return list(lex)

    txt_split = cmd.split()
    return txt_split[0].replace(CMD_DELIM, "", 1), shlex.split(" ".join(txt_split[1:]).encode('utf-8'))
    
def webPost(address, data):
    json = requests.post(address,data).json()
    return json
    
def getName(user_id):
    # Every user has a record in CSE, and it doesn't matter what room we get it from. So, Room1 is good.
    return webPost("https://chat.stackexchange.com/user/info", {"ids": user_id, "roomId": "1"})["users"][0]["name"]
    
def isRoomOwner(user_id, room_id):
    n = webPost("https://chat.stackexchange.com/user/info", {"ids": user_id, "roomId": room_id})["users"][0]["is_owner"]
    
    if n is None:
        return False
    else:
        return n

def isSEModerator(user_id):
    # SE Mods have SE admin status across the board. So we can query for Room1.
    n = webPost("https://chat.stackexchange.com/user/info", {"ids": user_id, "roomId": "1"})["users"][0]["is_moderator"]
    
    if n is None:
        return False
    else:
        return n
    
def isDeveloper(user_id):
    if (str(user_id) in PREFS.get("global", "devs", [])):
        return True
    else:
        return isSEModerator(user_id)
    
def isAdmin(user_id, room_id):
    if str(user_id) in PREFS.get(room_id, "admins", []):
        return True
    elif isDeveloper(user_id):
        return True
    else:
        return isRoomOwner(room_id, user_id)
        

