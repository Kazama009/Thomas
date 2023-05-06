import time
import importlib

from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import ContextTypes, CommandHandler
from telegram.helpers import escape_markdown
from telegram.constants import ParseMode

from thomas import application, LOGGER, SUPPORT_CHAT, START_TIME
from thomas.modules import ALL_MODULES


START_TEXT = '''
Hᴇʟʟᴏ *{}*
I ᴀᴍ *Thomas*
A Tᴇʟᴇɢʀᴀᴍ ʙᴏᴛ ɪɴᴛᴇɢʀᴀᴛᴇᴅ ᴡɪᴛʜ OᴘᴇɴAI's GPT-3.5 ʙᴀsᴇᴅ ʟᴀɴᴜᴀɢᴇ ᴍᴏᴅᴇʟ.
× Uᴘᴛɪᴍᴇ: `{}`
× Pᴏᴡᴇʀᴇᴅ Bʏ [Retrogini](t.me/retroginibotz)
'''

buttons = [
    [
        InlineKeyboardButton(
            text="Updates",
            url="t.me/retroginibotz"
        ),

        InlineKeyboardButton(
            text="Source Code",
            url="https://github.com/Kazama009/Thomas"
        )
    ]
]

IMPORTED = {}

for module_name in ALL_MODULES:
    imported_module = importlib.import_module("thomas.modules." + module_name)
    if not hasattr(imported_module, "__mod_name__"):
        imported_module.__mod_name__ = imported_module.__name__

    if imported_module.__mod_name__.lower() not in IMPORTED:
        IMPORTED[imported_module.__mod_name__.lower()] = imported_module
    else:
        raise Exception("Can't have two modules with the same name! Please change one")

def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uptime = get_readable_time((time.time() - START_TIME))
    fname = update.effective_user.first_name

    await update.effective_message.reply_text(
        text=START_TEXT.format(
            escape_markdown(fname), escape_markdown(uptime)
        ),
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True   
    )

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    HELP_TEXT = "I am an AI but in telegram.\nAsk me any query and I will answer.\nIts that simple 😅"
    
    await update.effective_message.reply_text(HELP_TEXT)

def main():
    start_handler = CommandHandler("start", start, block=False)
    help_handler = CommandHandler("help", help, block=False)

    application.add_handler(start_handler)
    application.add_handler(help_handler)

    application.run_polling(timeout=15, drop_pending_updates=False)

if __name__ == "__main__":
    main()