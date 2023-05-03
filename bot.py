import telegram
from telegram.ext import Updater
from telegram import Update , InlineKeyboardButton, InlineKeyboardMarkup, TelegramError
from telegram import InputMediaPhoto, InputMediaVideo
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler,MessageHandler,Filters, CallbackQueryHandler, ContextTypes, JobQueue
import logging
import json
from datetime import datetime
from hypebeast import Hypebeast
from db import getNonSendedToTGPosts, updatePost , getPostContentById , getImagesByPostId
from gpt import createPost

STAGE_CHANNEL = "@vaityagiwork"
PROD_CHANNEL = "@vaityagi"
ADMIN_USERID = 331392389

def parsePostsTask(context : CallbackContext) :
    parser.parse()
    
def checkPosts(context : CallbackContext) :
    posts = getNonSendedToTGPosts()
    for post in posts:
        message = f"""{post['info'][2]}
{post['info'][1]}"""
        #items = []
        #for img in post['images']:
        #    med = InputMediaPhoto(media=img[0])
        #    items.append(med)
        data = {
            "operation": "post",
            'info' : post['info'][0]
        }
        keyboard = [[InlineKeyboardButton("📩", callback_data=json.dumps(data))]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        #context.bot.send_media_group(chat_id='331392389',media = items)
        context.bot.send_message(chat_id=STAGE_CHANNEL, text=message, reply_markup=reply_markup)
        updatePost(operation='send_to_telegram', postId=post['info'][0])

def localStores(update: Update , context : CallbackContext) :
    pass

def start(update: Update , context : CallbackContext) :
    userId = update.message.from_user.id
    if userId == ADMIN_USERID:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Rabotaem')
        context.job_queue.run_repeating(checkPosts,40, context=update.message.chat_id)
        context.job_queue.run_repeating(parsePostsTask,100, context=update.message.chat_id)
    else:
        data = {
            'operation' : 'localStores'
        }
        text = """Привет! Я бот канала 'ВAI, что за тяги' и могу быть твоим проводником в мир кроссовок. Я умею:"""
        keyboard = [[InlineKeyboardButton("Покажи локальные магазины", callback_data=json.dumps(data))]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(chat_id=update.effective_chat.id, text=text,reply_markup=reply_markup)

def button(update: Update, context: ContextTypes) -> None:
    query = update.callback_query
    query.answer()
    data = json.loads(query.data)
    if data['operation'] == 'post' :
        postId = data['info']
        prompt = getPostContentById(postId=postId)
        message = createPost(prompt=prompt)
        images = getImagesByPostId(postId=postId)
        items = []
        counter = 1
        for img in images:
            if counter == 1:
                med = InputMediaPhoto(media=img[0], caption=message)
            else:
                med = InputMediaPhoto(media=img[0])
            items.append(med)
            counter = 0
        context.bot.send_media_group(chat_id=PROD_CHANNEL,media = items)
        updatePost(operation='send_to_openai', postId=postId)
    elif data['operation'] == 'localStores' :
        print(123123)

if __name__ == "__main__" :
    TOKEN = "6290678020:AAFy9CdpJhcavRMLJAJEj5_Vr6MUsoIgBBs"
    parser = Hypebeast()
    
    bot = telegram.Bot(token=TOKEN)
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    button_handler = CallbackQueryHandler(button)
    dispatcher.add_handler(button_handler)

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
    updater.start_polling()

    updater.idle() 