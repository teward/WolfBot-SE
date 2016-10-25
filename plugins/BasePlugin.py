import os
import sys
import signal
# noinspection PyUnresolvedReferences
import time
# noinspection PyUnresolvedReferences
import json
# noinspection PyUnresolvedReferences
import urllib2
import WolfUtils

import ChatExchange6.chatexchange6 as chatexchange6

# noinspection PyUnresolvedReferences
from WolfPlugin import register_command, register_listener, register_task
from WolfPrefs import PREFS
from WolfPrefs import SESSION_STORAGE


# Privilege Escalation
@register_command("addadmin", "Add an Admin to the system.", "", {"superuserNeeded": True})
def addadmin(message, args):
    room = message.data['room']

    if len(args) == 0 or len(args) > 1:
        message.message.reply("One argument (user_id) needed!")
        return None

    current_admins = PREFS.get(room.id, "admins", [])
    if args[0] not in current_admins:
        current_admins.append(args[0])
        PREFS.set(room.id, "admins", current_admins)
        message.message.reply(WolfUtils.get_name(args[0]) + " (ID  " + args[0] +
                              ") added as bot admin for this room.")
        return None
    else:
        message.message.reply("User is already a declared admin!")
        return None


@register_command("deladmin", "Add an Admin to the system.", "", {"superuserNeeded": True})
def deladmin(message, args):
    room = message.data['room']

    if len(args) == 0 or len(args) > 1:
        message.message.reply("One argument (user_id) needed!")
        return None

    current_admins = PREFS.get(room.id, "admins", [])
    if args[0] in current_admins:
        current_admins.remove(args[0])
        PREFS.set(room.id, "admins", current_admins)
        message.message.reply(WolfUtils.get_name(args[0]) +
                              " removed from bot admin role for this room.")
        return None
    else:
        message.message.reply("User is not a declared admin! "
                              "(This command may not be used to remove inherited rights)")
        return None


@register_command("setprefix", "Change the bot prefix", "", {"superuserNeeded": True})
def setprefix(message, args):
    if len(args) > 1:
        message.message.reply("One argument (prefix) needed!")
        return None

    if len(args) == 0:
        PREFS.set("global", "command_delimiter", "!!/")
        WolfUtils.CMD_DELIM = "!!/"
        message.message.reply("Prefix globally reset to default of `!!/`.")

        for room in SESSION_STORAGE.get("in_rooms"):
            if room.id != message.data['room_id']:
                room.send_message("The bot prefix has been set to `!!/` by " +
                                  WolfUtils.get_name(message.data['user_id']) + ".")
    else:
        PREFS.set("global", "command_delimiter", args[0])
        WolfUtils.CMD_DELIM = args[0]
        message.message.reply("Prefix globally set to `" + args[0] + "`.")

        for room in SESSION_STORAGE.get("in_rooms"):
            if room.id != message.data['room_id']:
                room.send_message("The bot prefix has been set to `" + args[0] + "` by " +
                                  WolfUtils.get_name(message.data['user_id']) + ".")


@register_command("setrprefix", "Change the bot reply prefix", "", {"superuserNeeded": True})
def setprefix(message, args):
    if len(args) > 1:
        message.message.reply("One argument (prefix) needed!")
        return None

    if len(args) == 0:
        PREFS.set("global", "reply_delimiter", "%")
        WolfUtils.REPLY_DELIM = "%"
        message.message.reply("Prefix reset to default of `%`.")

        for room in SESSION_STORAGE.get("in_rooms"):
            if room.id != message.data['room_id']:
                room.send_message("The reply prefix has been set to `%` by " + WolfUtils.get_name(
                    message.data['user_id']) + ".")
    else:
        PREFS.set("global", "reply_delimiter", args[0])
        WolfUtils.REPLY_DELIM = args[0]
        message.message.reply("Prefix set to `" + args[0] + "`.")

        for room in SESSION_STORAGE.get("in_rooms"):
            if room.id != message.data['room_id']:
                room.send_message(
                    "The reply prefix has been set to `" + args[0] + "` by " + WolfUtils.get_name(
                        message.data['user_id']) + ".")


# noinspection PyShadowingBuiltins
@register_command("reload", "Reload the bot", "<prefs>", {"superuserNeeded": True})
def reload(message, args):
    if len(args) > 1:
        message.message.reply("Zero or one argument (reloadtype (prefs)) needed!")
        return None

    if len(args) == 0:
        reload_type = "all"
    else:
        reload_type = args[0]

    if reload_type == "prefs":
        PREFS.load()
        message.message.reply("**Preference reload complete.**")


# noinspection PyUnusedLocal
@register_command("restart", "Restart the bot", "", {"superuserNeeded": True})
def restart(message=None, args=None):
    os.execl(sys.executable, sys.executable, *sys.argv)


# noinspection PyUnusedLocal
@register_command("stop", "Stop the bot", "", {"superuserNeeded": True})
def stop(message=None, args=None):
    os.kill(os.getpid(), signal.SIGTERM)


@register_command("iamthecaptainnow", "Become a Developer", "", {})
def take_root(message, args):
    if len(args) != 1:
        message.message.reply("Needs one argument (captain_key)")
        return None

    current_devs = PREFS.get("global", "devs", [])

    if not current_devs:
        if args[0].lower() == PREFS.get("global", "captain_key").lower():
            current_devs.append(str(message.data['user_id']))
            PREFS.set("global", "devs", current_devs)
            message.message.reply("https://i.imgur.com/2oNMYD3.jpg")
            PREFS.delete("global", "captain_key")
            PREFS.save()
        else:
            message.message.reply("You are by far the worst captain I've ever heard of.")
    else:
        message.message.reply("You are by far the worst captain I've ever heard of.")


@register_command("blacklist", "Block a user from using commands", "", {"adminNeeded": True})
def blacklist_user(message, args):
    if len(args) != 1:
        message.message.reply("Needs one argument (user_id)")
        return None

    room = message.data['room']

    user_to_bl = args[0]

    current_blacklist = PREFS.get(room.id, "user_blacklist", [])
    if user_to_bl not in current_blacklist:
        if not WolfUtils.is_admin(user_to_bl, room.id):
            current_blacklist.append(user_to_bl)
            PREFS.set(room.id, "user_blacklist", current_blacklist)
            message.message.reply(WolfUtils.get_name(
                user_to_bl) + " (ID  " + user_to_bl + ") is no longer permitted "
                                                      "to use WolfBot commands.")
        else:
            message.message.reply("Admins and Superusers may not be blacklisted.")
    else:
        message.message.reply("User is already blacklisted!")


@register_command("unblacklist", "Allow a user to use commands", "", {"adminNeeded": True})
def unblacklist_user(message, args):
    if len(args) != 1:
        message.message.reply("Needs one argument (user_id)")
        return None

    room = message.data['room']

    user_to_unbl = args[0]

    current_blacklist = PREFS.get(room.id, "user_blacklist", [])
    if user_to_unbl in current_blacklist:
        current_blacklist.remove(user_to_unbl)
        PREFS.set(room.id, "user_blacklist", current_blacklist)
        message.message.reply(WolfUtils.get_name(
            user_to_unbl) + " (ID  " + user_to_unbl + ") is now permitted to use WolfBot commands.")
    else:
        message.message.reply("User is already blacklisted!")


@register_command("joinroom", "Send the bot to join a new room.", "", {"superuserNeeded": True})
def join_room(message, args):
    if len(args) == 0:
        message.message.reply("Needs one argument: room_id")
        return

    rid = args[0]

    if PREFS.get(rid, "banned", False):
        message.message.reply("The bot has been banned from joining that room!")
        return

    PREFS.set(rid, "active", True)
    message.message.reply("The bot has joined the given room.")
    restart("1", "1")


@register_command("leaveroom", "Have the bot leave the current room.", "",
                  {"superuserNeeded": True})
def leave_room(message, args):
    if len(args) == 0:
        mode = "normal"
    else:
        mode = args[0]

    if mode == "purge":
        PREFS.purge_chat(message.data['room_id'])
        restart("1", "1")
    elif mode == "ban":
        PREFS.purge_chat(message.data['room_id'])
        PREFS.set(message.data['room_id'], "banned", True)
        restart("1", "1")
    elif mode == "normal":
        PREFS.set(message.data['room_id'], "active", False)
        restart("1", "1")
    else:
        message.message.reply(
            "Command expects a mode: normal, purge, ban (No argument implies normal)")


@register_command("lockdown", "Lock down the bot and prevent it from taking actions from "
                              "non-admins", "", {"adminNeeded": True})
def lockdown(message, args):
    room = message.data['room_id']

    lockdown_state = PREFS.get(room, "lockdown", False)

    if len(args) == 1:
        if args(0) == "false" or args(0) == "off":
            if not lockdown_state:
                message.message.reply("Lockdown mode is already disabled.")
            else:
                PREFS.set(room, "lockdown", False)
                message.message.reply(
                    "Room no longer lockdown. Commands may be freely given, and tasks will"
                    " run once again.")
        elif args(0) == "true" or args(0) == "on":
            if lockdown_state:
                message.message.reply("Lockdown mode is already enabled.")
            else:
                PREFS.set(room, "lockdown", True)
                message.message.reply(
                    "Room under lockdown. Only admins may give commands to the bot, and tasks"
                    " will not run.")
        return

    if not lockdown_state:
        PREFS.set(room, "lockdown", True)
        message.message.reply(
            "Room under lockdown. Only admins may give commands to the bot, and tasks will "
            "not run.")
    else:
        PREFS.set(room, "lockdown", False)
        message.message.reply(
            "Room no longer under lockdown. Commands may be freely given, and tasks will "
            "run once again.")


@register_command("addtask", "Add a task to the list of tasks executable by the bot.", "",
                  {"adminNeeded": True})
def deltask(message, args):
    current_tasks = PREFS.get(message.data['room_id'], "enabled_tasks", [])

    if len(args) == 0:
        message.message.reply("Expected one argument: task_name")
        return

    if args(0) in current_tasks:
        message.message.reply("This task is already listed as enabled!")
    else:
        current_tasks.append(args(0))
        message.message.reply("The task `" + args(
            0) + "` is now enabled for this room. Note that it may still need configuration.")


@register_command("deltask", "Remove a task from the list of tasks executable by the bot.", "",
                  {"adminNeeded": True})
def deltask(message, args):
    current_tasks = PREFS.get(message.data['room_id'], "enabled_tasks", [])

    if len(args) == 0:
        message.message.reply("Expected one argument: task_name")
        return

    if args(0) not in current_tasks:
        message.message.reply("This task is not listed as enabled!")
    else:
        current_tasks.remove(args(0))
        message.message.reply("The task `" + args(
            0) + "` is now disabled for this room. Note that it may still need configuration.")


@register_listener("modtool-deletemsg", 18)
def listener_delete_message(message):
    if message.data["content"] == "@" + SESSION_STORAGE.get(
            "bot_username") + " " + WolfUtils.REPLY_DELIM + "d":
        if WolfUtils.is_admin(message.data["user_id"], message.data['room_id']):
            chatexchange6.messages.Message(message.data["parent_id"], message.client).delete()
