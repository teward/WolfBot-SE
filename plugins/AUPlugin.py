import WolfUtils
import feedparser
import time
import calendar
from datetime import datetime
from WolfPlugin import registerCommand, registerTask

from WolfPrefs import PREFS

WORD_LIST = PREFS.get("word_filter_list", [])
FILTER_URL = PREFS.get("word_filter_source")
LAST_PULL_TIME = int(time.time())

@registerCommand("setfurl", "Set the filter URL", "", {"superuserNeeded": True})
def addfilter(message, args):
    if len(args) != 1:
        message.message.reply("One argument (url) needed!")
        return None
        
    FILTER_URL = args[0]
    PREFS.set("word_filter_source", FILTER_URL)
    message.message.reply("Filter Source URL set to " + args[0])

@registerCommand("addfilter", "Add something to the Filter list", "", {"adminNeeded": True})
def addfilter(message, args):
    if len(args) == 0:
        message.message.reply("One argument (word) needed!")
        return None    
    elif len(args) == 1:
        word = args[0]
        if word not in WORD_LIST:
            WORD_LIST.append(word)
            PREFS.set("word_filter_list", WORD_LIST)
            message.message.reply("`" + word + "` has been added to the filter list.")
        else:
            message.message.reply("`" + word + "` is already in the filter list!")
        return None
    else:
        merge_fail = []
        
        for word in args:
            if word not in WORD_LIST:
                WORD_LIST.append(word)
            else:
                merge_fail.append(word)
        PREFS.set("word_filter_list", WORD_LIST)
        
        if len(merge_fail) == 0:
            message.message.reply("All words were added to list successfully.")
        elif len(merge_fail) == len(args):
            message.message.reply("No words could be added to the list (already there?).")
        else:
            message.message.reply(str(len(merge_fail)) + " words could not be added to the list (already there?):\n" + " ".join(merge_fail)) 
    
@registerCommand("delfilter", "Remove something from the Filter list", "", {"adminNeeded": True})
def remfilter(message, args):
    if len(args) == 0:
        message.message.reply("One argument (word) needed!")
        return None    
    elif len(args) == 1:
        word = args[0]
        if word in WORD_LIST:
            WORD_LIST.remove(word)
            PREFS.set("word_filter_list", WORD_LIST)
            message.message.reply("`" + word + "` has been removed from filter list.")
        else:
            message.message.reply("`" + word + "` is not in the filter list!")
        return None
    else:
        merge_fail = []
        
        for word in args:
            if word in WORD_LIST:
                WORD_LIST.remove(word)
            else:
                merge_fail.append(word)
        PREFS.set("word_filter_list", WORD_LIST)
        
        if len(merge_fail) == 0:
            message.message.reply("All words were removed from the list successfully.")
        elif len(merge_fail) == len(args):
            message.message.reply("No words could be removed from the list (not there?).")
        else:
            message.message.reply(str(len(merge_fail)) + " words could not be removed from the list (not there?):\n" + " ".join(merge_fail))
        
@registerCommand("clearfilter", "Clear the Filter List", "", {"adminNeeded": True})
def clearfilter(message, args):
    WORD_LIST = {}
    PREFS.set("word_filter_list", WORD_LIST)
    message.message.reply("The filter list has been cleared.")
    
@registerCommand("getfilter", "Get all items on the Filter List", "", {})
def getfilter(message, args):
    message.message.reply("Words on the filter list:\n" + ", ".join(WORD_LIST))
    
    
@registerTask("GetNewEntries", 60)
def taskRunFilter(room):
    global LAST_PULL_TIME

    if FILTER_URL is None:
        print("[E] Unable to run task! Filter URL is empty.")
        return None
        
    results = []
    post_timestamps = []
    
    data = feedparser.parse(FILTER_URL).entries
    
    for word in WORD_LIST:
        for entry in data:
            if word.lower() in entry['summary'].lower():
                post_timestamps.append(seTimeToUnixTime(entry['published']))
                if seTimeToUnixTime(entry['published']) > LAST_PULL_TIME:
                    results.append({"trigger": word, "title": entry['title'], "url": entry['id']})
    
    try:                
        LAST_PULL_TIME = max(post_timestamps)
    except ValueError:
        LAST_PULL_TIME = LAST_PULL_TIME
    
    if len(results) == 1:
        room.send_message("[**WolfBot**] Found filtered post, matches word `" + results[0]["trigger"] + \
        "`: [" + results[0]["title"] + "](" + results[0]["url"] + ")")
    elif len(results) > 1:
        s = ""
        for result in results:
            s += "[" + result["title"]  + "](" + result["url"] + "), matches word `" + result["trigger"] + "`\n"     
        room.send_message("[**WolfBot**] Found multiple filtered posts:\n" + s)
        
def seTimeToUnixTime(timestring):
    dt = datetime.strptime(timestring, "%Y-%m-%dT%H:%M:%SZ")
    return int(calendar.timegm(dt.utctimetuple()))
