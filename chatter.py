#!/usr/bin/python
import aiml
import time
import signal
import sys
import telegram
from datetime import date
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from gtts import gTTS
import logging
import os

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    chat_id = update.message.chat_id
    message = update.message.text    
    #bot.sendPhoto(chat_id=chat_id, photo='https://media.giphy.com/media/uooHb19hRELeM/giphy.gif')
    bot.sendMessage(update.message.chat_id, text='Hola, soy Sara! :D')



def help(bot, update):
    bot.sendMessage(update.message.chat_id, text='Help!')

def chatter(bot,update):

    chat_id = update.message.chat_id
    message = update.message.text
    if message == 'foto':
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
        bot.sendPhoto(chat_id=chat_id, photo='https://unsplash.it/600?random')
    else:
        k = aiml.Kernel()
        k.learn("std-startup.xml")
        k.respond("sara")
        k.setBotPredicate("name", "Sara")
        k.setBotPredicate("anyo_nacimiento", "2015")
        k.setBotPredicate("edad", str(date.today().year-2015) )
        k.setBotPredicate("botmaster", 'Alexander' )
        k.setBotPredicate("nombre_bot", 'Sara' )
        k.setBotPredicate("birthday", '17/12/2015' )
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        response = k.respond(message)    
        #bot.sendMessage(chat_id, text=response)
        tts = gTTS(text=response, lang='es') 

        file = str(chat_id) + str(time.time()) + '.ogg'
        tts.save(file)
        bot.sendVoice(chat_id=chat_id, voice=open(file, 'rb'))
        os.remove(file)



def main():
    # Create the EventHandler and pass it your bot's token.
    # sara
    #updater = Updater("223436029:AAEgihik3KXielXe7lBuP9H7o4M-eUdL_LU")
    #testbot
    updater = Updater("223436029:AAH9iIhGXP8EAB4qxXx4wJ0-YpYtplYVOkY")
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    #dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler([Filters.text], chatter))

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()