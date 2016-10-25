import WolfUtils
# noinspection PyUnresolvedReferences
from WolfPlugin import register_command, register_task

# noinspection PyUnresolvedReferences
from WolfPrefs import PREFS
from WolfPrefs import SESSION_STORAGE


# noinspection PyUnusedLocal
@register_command("start", "Get started with WolfBot!", "", {})
def start(message, args):
    message.message.reply("Hi there! Welcome to " + SESSION_STORAGE.get("bot_username") + "!")


# noinspection PyUnusedLocal
@register_command("whoami", "Get user information.", "", {})
def whoami(message, args):
    uid = message.data['user_id']
    username = message.data['user_name']
    room = message.data['room_id']

    is_dev = WolfUtils.is_developer(uid)
    is_mod = WolfUtils.is_se_moderator(uid)
    is_adm = WolfUtils.is_admin(uid, room)
    is_room_owner = WolfUtils.is_room_owner(uid, room)

    message.message.reply("You are: " + username + " (ID " + str(uid) + ")" +
                          "\nIs Bot Superuser (Grants Bot Admin): " + str(is_dev) +
                          "\nIs Bot Admin: " + str(is_adm) +
                          "\nIs SE Mod (Grants Superuser): " + str(is_mod) +
                          "\nIs Room Owner (Grants Bot Admin): " + str(is_room_owner))


# Privilege Test Commands
# noinspection PyUnusedLocal
@register_command("regusertest", "Check for user powers.", "", {})
def reg_user_test(message, args):
    message.message.reply("User command executed successfully.")


# noinspection PyUnusedLocal
@register_command("admintest", "Check for admin powers.", "", {"adminNeeded": True})
def admin_test(message, args):
    message.message.reply("Awooooo!")


# noinspection PyUnusedLocal
@register_command("superusertest", "Check for superuser powers.", "", {"superuserNeeded": True})
def superuser_test(message, args):
    message.message.reply("Superuser command executed successfully.")


# noinspection PyUnusedLocal
@register_command("throwex", "Force an exception.", "", {"superuserNeeded": True})
def throwex(message, args):
    if len(args) == 0:
        msg = "The exception you requested..."
    else:
        msg = " ".join(args)

    raise RuntimeError(msg)
