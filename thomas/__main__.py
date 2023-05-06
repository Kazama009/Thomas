import time

from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import ContextTypes, CommandHandler
from telegram.helpers import escape_markdown
from telegram.constants import ParseMode

from thomas import application, LOGGER, SUPPORT_CHAT, START_TIME

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

def main():
    start_handler = CommandHandler("start", start, block=False)

    application.add_handler(start_handler)

    application.run_polling(timeout=15, drop_pending_updates=False)

if __name__ == "__main__":
    main()