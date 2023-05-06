import json
import openai 

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import MessageHandler, ContextTypes, filters, CallbackQueryHandler

from thomas import application, OPENAI_API_TOKEN


openai.api_key = OPENAI_API_TOKEN

def _textcompletion(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002", 
        prompt=prompt, 
        max_tokens=2048,
        temperature=0.5
    )

    return response

async def textcompletion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = update.effective_message.text
    response = _textcompletion(prompt=prompt)

    text = response["choices"][0]["text"]
    cb = str(update.effective_message.text)

    await update.effective_message.reply_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Regenerate",
                        callback_data=f"chatbot_=textcompletion={cb}"
                    )
                ]
            ]
        )
    )

async def chatbot_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    message = update.effective_message

    splitter = query.data.replace("chatbot_", "").split("=")

    if splitter[1] == "textcompletion":
        prompt = splitter[2]
        response = _textcompletion(prompt=prompt)

        text = response["choices"][0]["text"]
        cb = str(update.effective_message.text)

        await message.edit_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Regenerate",
                            callback_data=f"chatbot_=textcompletion={cb}"
                        )
                    ]
                ]
            )
        )

textcompletion_handler = MessageHandler(filters.TEXT, textcompletion, block=False)

chatbot_callback_handler = CallbackQueryHandler(chatbot_callback, block=False, pattern=r"chatbot_")

application.add_handler(textcompletion_handler)    
application.add_handler(chatbot_callback_handler)