from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import logging
import settings
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='logbot.log'
                    )



def greet_user(bot, update):
    text = 'I am working!'
    logging.info(text)
    update.message.reply_text(text)

def talk_to_me(bot, update):
    user_message = "Привет {}! Ты написал: {}".format(update.message.chat.first_name, update.message.text)
    logging.info("User: %s, Chat id: %s, Message: %s", update.message.chat.username, update.message.chat.id, update.message.text)
    print(update.message)

    update.message.reply_text(user_message)
    


def main():
    my_bot = Updater(settings.API_KEY)
    
    logging.info("Starting...")

    dp = my_bot.dispatcher
    dp.add_handler(CommandHandler('mayhem', greet_user))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    my_bot.start_polling()
    my_bot.idle()


main()