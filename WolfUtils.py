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

CMD_DELIM = PREFS.get("command_delimiter")
ROOM_ID = PREFS.get("chat_id")

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
    return txt_split[0].replace(CMD_DELIM, "", 1), shlex.split(" ".join(txt_split[1:]))
    
def webPost(address, data):
    json = requests.post(address,data).json()
    return json
    
def isRoomOwner(user_id):
    n = webPost("https://chat.stackexchange.com/user/info", {"ids": user_id, "roomId": ROOM_ID})["users"][0]["is_owner"]
    
    if n is None:
        return False
    else:
        return n

def isSEModerator(user_id):
    n = webPost("https://chat.stackexchange.com/user/info", {"ids": user_id, "roomId": ROOM_ID})["users"][0]["is_moderator"]
    
    if n is None:
        return False
    else:
        return n
    
def isDeveloper(user_id):
    if (str(user_id) in PREFS.get("devs", [])):
        return True
    else:
        return isSEModerator(user_id)
    
def isAdmin(user_id):
    if str(user_id) in PREFS.get("admins", []):
        return True
    elif isDeveloper(user_id):
        return True
    else:
        return isRoomOwner(user_id)
        

