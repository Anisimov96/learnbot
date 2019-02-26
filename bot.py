# -*- coding: utf-8 -*-
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
# Updater подключается к Telegram, представляется ботом и проверяет входящие сообщения
# CommandHandler - обработчик команд
# MessageHandler - обработчик текстовых сообщений
# Filters - с каким типом сообщений мы хотим взаимодействовать
# logging - отчет о работе с ботом

# Настроим прокси
PROXY = {'proxy_url': 'socks5://t1.learn.python.ru:1080',
    'urllib3_proxy_kwargs': {'username': 'learn', 'password': 'python'}}

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    handlers=[logging.FileHandler('bot.log', 'w', 'utf-8')]
                    )
def greet_user(bot, update):
    text ='Вызван /start'
    print(text)
    logging.info(text)
    #  ответа пользователю
    update.message.reply_text(text)

def talk_to_me (bot, update):
    user_text = update.message.text 
    print(user_text)
    # ответ пользователю
    update.message.reply_text(user_text)
 
def main():
    mybot = Updater("629476291:AAHapHDKGqjtE9Y4UbzHNDGFQo-X6dXD1KI", request_kwargs=PROXY)
    
    # Добавим в тело нашего бота обработчик команд
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    
    # Добавим в тело нашего бота обработчик сообщений
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    
    logging.info('Бот запускается')
    # Бот постоянно проверяет Telegramm на поступление сообщений
    mybot.start_polling()
    # Бот работает до принудительной остановки
    mybot.idle()

# Вызов функции
main()
