from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import logging
import settings
import ephem
import datetime
import re
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='logbot.log'
                    )



def greet_user(bot, update):
    text = ("Привет, я умею определять в каком созвездии находится планета на сегодняшний день!\n" 
        "Введи команду /planet и через пробел название планеты на английском языке, согласно реестру IAU")
    print (update.message.text)


    logging.info(text)
    update.message.reply_text(text)

def talk_to_me(bot, update):
    user_message = "Привет {}! Ты написал: {}".format(update.message.chat.first_name, update.message.text)
    logging.info("User: %s, Chat id: %s, Message: %s", update.message.chat.username, update.message.chat.id, update.message.text)
    print(update.message)

    update.message.reply_text(user_message)

def input_planet(bot, update):
    try:
        text_about_planet = "Trying input planetname..."
        separate_name =  update.message.text.split(" ")
        name_planet = separate_name[1].lower()
        name_planet = name_planet.capitalize()
        if name_planet != 'Earth':
            date = datetime.datetime.now()
            date_for_ephem = date.strftime('%Y/%m/%d')
            set_planet_and_time = getattr(ephem, name_planet)(date_for_ephem)
            planet_position = ephem.constellation(set_planet_and_time)
            logging.info(text_about_planet)
            update.message.reply_text("Планета {} находится в созвездии: {}".format(name_planet, planet_position[1]))
        else:
            logging.info("Trying to put Earth in name_panet")
            update.message.reply_text("Названия созвездий определены относительно Земли, делайте выводы!")

    except (AttributeError, IndexError):
        warning_log_message = "Incorrect planet name"
        warning_message = "Ввделите корректное название планеты на английском языке согласно реестру IAU"
        update.message.reply_text(warning_message)
        logging.info(warning_log_message)

def word_count(bot, update):
    phrase = update.message.text
    signs = [",", ".", "!", "?", "(", ")", "-", "_"]
    for letter in signs:
        phrase = phrase.replace(letter, " ")
 
    print (phrase)
    new_phrase = phrase.split()
    lenght_phrase = len(new_phrase)-1
    update.message.reply_text("Вы ввели: {} слова".format(lenght_phrase))
    logging.info("Input some text")




def main():
    my_bot = Updater(settings.API_KEY, request_kwargs = settings.PROXY)
    
    logging.info("Starting...")

    dp = my_bot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('planet', input_planet))
    dp.add_handler(CommandHandler('wordcount', word_count))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    


    my_bot.start_polling()
    my_bot.idle()


main()