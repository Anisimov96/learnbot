# -*- coding: utf-8 -*-
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import settings
# Updater подключается к Telegram, представляется ботом и проверяет входящие сообщения
# CommandHandler - обработчик команд
# MessageHandler - обработчик текстовых сообщений
# Filters - с каким типом сообщений мы хотим взаимодействовать (текст, картинки и т.д.)
# logging - отчет о работе с ботом 

# Настроим прокси


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO, # уровни логирования
                    handlers=[logging.FileHandler('bot.log', 'w', 'utf-8')]
                    )

def greet_user(bot, update):
    # bot -экземпляр нашего бота
    # update - данные о прешедшем сообщении
    text ='Вызван /start'
    print(text) # Вывод текста в консоль
    logging.info(text) # Сооб. в bot.log 
    update.message.reply_text(text) # ответ пользователю

def talk_to_me (bot, update):
    user_text ='Привет {}! Ты написал {}'.format(update.message.chat.first_name, update.message.text)
    print(user_text) # печать вх. сообщен в консоль
    # Сохраним в bot.log данные о вх. сообщ.
    logging.info('Users: %s, Chat id: %s, Message: %s', update.message.chat.username,
                update.message.chat.id, update.message.text)
    update.message.reply_text(user_text) # ответ пользователю
 
def main():
    # mybot - объект класса Updater
    mybot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)
    
    # Добавим в тело нашего бота обработчик команд
    # dispatcher - перераспределяет вх. сообщения по "адресатам"
    dp = mybot.dispatcher
   
    # Если в telegram придет команда start мы на нее среагируем
    # командой greet_user
    dp.add_handler(CommandHandler('start', greet_user))
    
    # Добавим в тело нашего бота обработчик сообщений
    # Если поступило сообщение, то вызывается ф-ия talk_to_me
    # Filters.text означает что MessageHandler будет реагировать только
    # на текстовые сообщения
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    
    logging.info('Бот запускается')
    # Бот постоянно проверяет Telegramm на поступление сообщений
    mybot.start_polling()
    # Бот работает до принудительной остановки
    mybot.idle()

# Вызов функции
main()
