# -*- coding: utf-8 -*-

# noinspection PyUnresolvedReferences
from ChatExchange6 import chatexchange6 as chatexchange6
# noinspection PyUnresolvedReferences
import json
import shlex
# noinspection PyUnresolvedReferences
import sys
import requests
# noinspection PyUnresolvedReferences
from urlparse import urlparse
# noinspection PyUnresolvedReferences
from urllib import urlopen
# noinspection PyUnresolvedReferences
from datetime import datetime

from WolfPrefs import PREFS

CMD_DELIM = PREFS.get("global", "command_delimiter", "!!/")
REPLY_DELIM = PREFS.get("global", "reply_delimiter", "%")


# Determine if a text is a command
#    Arg `message`: The text to check for commandiness
def is_command(message):
    return message.startswith(CMD_DELIM)


def parse_command(cmd):
    # noinspection PyUnusedLocal
    def new_split(value):
        lex = shlex.shlex(value)
        lex.quotes = '"'
        lex.whitespace_split = True
        lex.commenters = ''
        return list(lex)

    txt_split = cmd.split()
    return txt_split[0].replace(CMD_DELIM, "", 1), shlex.split(
        " ".join(txt_split[1:]).encode('utf-8'))


def web_post(address, data):
    json_data = requests.post(address, data).json()
    return json_data


def get_name(user_id):
    # Every user has a record in CSE, and it doesn't matter what room we get it from.
    # So, Room1 is good.
    return web_post("https://chat.stackexchange.com/user/info",
                    {"ids": user_id, "roomId": "1"})["users"][0]["name"]


def is_room_owner(user_id, room_id):
    n = web_post("https://chat.stackexchange.com/user/info",
                 {"ids": user_id, "roomId": room_id})["users"][0]["is_owner"]

    if n is None:
        return False
    else:
        return n


def is_se_moderator(user_id):
    # SE Mods have SE admin status across the board. So we can query for Room1.
    n = web_post("https://chat.stackexchange.com/user/info",
                 {"ids": user_id, "roomId": "1"})["users"][0]["is_moderator"]

    if n is None:
        return False
    else:
        return n


def is_developer(user_id):
    if str(user_id) in PREFS.get("global", "devs", []):
        return True
    # else:
        # return is_se_moderator(user_id)


def is_admin(user_id, room_id):
    if str(user_id) in PREFS.get(room_id, "admins", []):
        return True
    elif is_developer(user_id):
        return True
    else:
        return is_room_owner(room_id, user_id)
