# -*- coding: utf-8 -*-

# noinspection PyUnresolvedReferences
import WolfUtils
import feedparser
import time
import calendar
import urllib2
from datetime import datetime
from bs4 import BeautifulSoup

from WolfPlugin import register_command, register_task
from WolfPrefs import PREFS
from WolfPrefs import SESSION_STORAGE

LAST_PULL_TIME = int(time.time())


@register_command("s", "Get a shortcutted post", "", {})
def getshortcut(message, args):
    room = message.data['room']

    if len(args) != 1:
        message.message.reply("Hey, silly! I need a shortcut to check!")
        return None

    current_shortcuts = PREFS.get(room.id, "post-shortcuts", {})

    if args[0] not in current_shortcuts:
        message.message.reply(args[0] + " is not a shortcut. Go away.")
        return None

    soup = BeautifulSoup(urllib2.urlopen(current_shortcuts[args[0]]))

    message.message.reply(
        "Hey! I've got this link for you: [" + soup.title.string + "](" +
        current_shortcuts[args[0]] + ")")


@register_command("addshortcut", "Add a new Question Shortcut", "", {"adminNeeded": True})
def addshortcut(message, args):
    if len(args) != 2:
        message.message.reply("Two arguments (name, url) needed!")
        return None

    current_shortcuts = PREFS.get(message.data['room_id'], "post-shortcuts", {})

    if args[0] in current_shortcuts:
        message.message.reply(args[0] + " is already a shortcut! Can't add.")
        return None

    args[1] = args[1].decode('ascii', 'ignore')

    current_shortcuts[args[0]] = args[1]
    PREFS.set(message.data['room_id'], "post-shortcuts", current_shortcuts)

    message.message.reply(
        "From now on, the shortcut `" + args[0] + "` will return [this link](" + args[1] + ").")


@register_command("delshortcut", "Add a new Question Shortcut", "", {"adminNeeded": True})
def delshortcut(message, args):
    if len(args) != 1:
        message.message.reply("Two arguments (name) needed!")
        return None

    current_shortcuts = PREFS.get(message.data['room_id'], "post-shortcuts", {})

    if args[0] not in current_shortcuts:
        message.message.reply(args[0] + " is not a shortcut. Can't remove.")
        return None

    del current_shortcuts[args[0]]

    message.message.reply(
        "From now on, the shortcut `" + args[0] + "` will no longer resolve to anything.")


# noinspection PyUnusedLocal
@register_command("listshortcuts", "List all registered shortcuts", "", {})
def listshortcuts(message, args):
    current_shortcuts = PREFS.get(message.data['room_id'], "post-shortcuts", None)

    if current_shortcuts is None:
        message.message.reply("No shortcuts are present in the system.")
        return None

    q_message = "I have the following shortcuts in my registry: \n\n"
    for s in current_shortcuts:
        q_message += "`" + s + "`: " + current_shortcuts[s]

    message.message.reply(q_message)


@register_command("setfurl", "Set the filter URL", "", {"superuserNeeded": True})
def addfilter(message, args):
    if len(args) != 1:
        message.message.reply("One argument (url) needed!")
        return None

    filter_url = args[0]
    PREFS.set(message.data['room_id'], "word_filter_source", filter_url)
    message.message.reply("Filter Source URL set to " + args[0])


@register_command("addfilter", "Add something to the Filter list", "", {"adminNeeded": True})
def addfilter(message, args):
    if len(args) < 2:
        message.message.reply("Two arguments [bl|wl] (words) needed!")
        return None

    if args[0] == "bl":
        word_list = PREFS.get(message.data['room_id'], "word_filter_blacklist", [])
        list_name = "blacklist"
    elif args[0] == "wl":
        word_list = PREFS.get(message.data['room_id'], "word_filter_whitelist", [])
        list_name = "whitelist"
    else:
        message.message.reply("First argument must be either bl or wl!")
        return None

    if len(args) == 2:
        word = args[1]
        if word not in word_list:
            word_list.append(word)
            PREFS.set(message.data['room_id'], "word_filter_" + list_name, word_list)
            message.message.reply("`" + word + "` has been added to the filter " + list_name + ".")
        else:
            message.message.reply("`" + word + "` is already in the filter" + list_name + "!")
        return None
    else:
        merge_fail = []

        for word in args[1:]:
            if word not in word_list:
                word_list.append(word)
            else:
                merge_fail.append(word)
        PREFS.set(message.data['room_id'], "word_filter_" + list_name, word_list)

        if len(merge_fail) == 0:
            message.message.reply("All words were added to " + list_name + " successfully.")
        elif len(merge_fail) == len(args):
            message.message.reply(
                "No words could be added to the " + list_name + " (already there?).")
        else:
            message.message.reply(str(len(
                merge_fail)) + " words could not be added to the " + list_name +
                                  " (already there?):\n" + " ".join(merge_fail))


@register_command("delfilter", "Remove something from the Filter list", "", {"adminNeeded": True})
def remfilter(message, args):
    if len(args) < 2:
        message.message.reply("Two arguments [bl|wl] (words) needed!")
        return None

    if args[0] == "bl":
        word_list = PREFS.get(message.data['room_id'], "word_filter_blacklist", [])
        list_name = "blacklist"
    elif args[0] == "wl":
        word_list = PREFS.get(message.data['room_id'], "word_filter_whitelist", [])
        list_name = "whitelist"
    else:
        message.message.reply(
            "First argument must be either `bl` (modify blacklist) or `wl` (modify whitelist)!")
        return None

    if len(args) == 2:
        word = args[1]
        if word in word_list:
            word_list.remove(word)
            PREFS.set(message.data['room_id'], "word_filter_" + list_name, word_list)
            message.message.reply(
                "`" + word + "` has been removed from the filter " + list_name + ".")
        else:
            message.message.reply("`" + word + "` is not in the filter " + list_name + "!")
        return None
    else:
        merge_fail = []

        for word in args:
            if word in word_list:
                word_list.remove(word)
            else:
                merge_fail.append(word)
        PREFS.set(message.data['room_id'], "word_filter_" + list_name, word_list)

        if len(merge_fail) == 0:
            message.message.reply("All words were removed from the " + list_name + "successfully.")
        elif len(merge_fail) == len(args):
            message.message.reply(
                "No words could be removed from the " + list_name + " (not there?).")
        else:
            message.message.reply(str(len(
                merge_fail)) + " words could not be removed from the the " + list_name +
                                  " (not there?):\n" + " ".join(merge_fail))


# noinspection PyUnusedLocal
@register_command("clearfilter", "Clear the Filter List", "", {"adminNeeded": True})
def clearfilter(message, args):
    PREFS.set(message.data['room_id'], "word_filter_blacklist", [])
    PREFS.set(message.data['room_id'], "word_filter_whitelist", [])
    message.message.reply("The filter list has been cleared.")


# noinspection PyUnusedLocal
@register_command("getfilter", "Get all items on the Filter List", "", {})
def getfilter(message, args):
    message.message.reply("Words on the filter blacklist:\n" + ", ".join(
        PREFS.get(message.data['room_id'], "word_filter_blacklist", [])) +
                          "\n\nWords on the filter whitelist:\n" + ", ".join(
        PREFS.get(message.data['room_id'], "word_filter_whitelist", [])))


@register_task("GetNewEntries", 60)
def task_run_filter(room):
    global LAST_PULL_TIME

    filter_url = PREFS.get(room.id, "word_filter_source")
    word_blacklist = PREFS.get(room.id, "word_filter_blacklist", [])
    word_whitelist = PREFS.get(room.data, "word_filter_whitelist", [])

    if filter_url is None:
        print("[E] Unable to run task! Filter URL is empty.")
        return None

    results = []
    post_timestamps = []

    data = feedparser.parse(filter_url).entries

    for entry in data:
        post_timestamps.append(setime_to_unixtime(entry['published']))
        if setime_to_unixtime(entry['published']) > LAST_PULL_TIME:
            for word in word_blacklist:
                if word.lower() in entry['summary'].lower() and not any(
                                oword.lower() in entry['summary'].lower() for oword in
                                word_whitelist):
                    results.append({"trigger": word, "title": entry['title'], "url": entry['id']})

    try:
        LAST_PULL_TIME = max(post_timestamps)
    except ValueError:
        LAST_PULL_TIME = LAST_PULL_TIME

    if len(results) == 1:
        room.send_message("[**" + SESSION_STORAGE.get(
            "bot_username") + "**] Found filtered post, matches word `" + results[0]["trigger"] +
                          "`: [" + results[0]["title"] + "](" + results[0]["url"] + ")")
    elif len(results) > 1:
        s = ""
        for result in results:
            # noinspection PyTypeChecker
            s += "[" + result["title"] + "](" + result["url"] + "), matches word `" + \
                 result["trigger"] + "`\n"
        room.send_message("[**" + SESSION_STORAGE.get(
            "bot_username") + "**] Found multiple filtered posts:\n" + s)


def setime_to_unixtime(timestring):
    dt = datetime.strptime(timestring, "%Y-%m-%dT%H:%M:%SZ")
    return int(calendar.timegm(dt.utctimetuple()))
