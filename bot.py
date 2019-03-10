# -*- coding: utf-8 -*-
from glob import glob
import logging
from random import choice

from emoji import emojize
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, RegexHandler, Filters
 
import settings
# Updater подключается к Telegram, представляется ботом и проверяет входящие сообщения
# CommandHandler - обработчик команд
# MessageHandler - обработчик текстовых сообщений
# Filters - с каким типом сообщений мы хотим взаимодействовать (текст, картинки и т.д.)
# logging - отчет о работе с ботом 
# dlob - указывает путь к файлам и ограничивает список определенными критериями
# emojize - берет текстовое обозначение смайла и превращает его в смаил
# ReplyKeyboardMarkup - для создания клавиатуры
# RegexHandler - хендлер основаный на регулярных выражениях (для сложного поиска или замены в строке)
# KeyboardButton - класс для получ. геоолокации и контактных данных пользователя
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO, # уровни логирования
                    handlers=[logging.FileHandler('bot.log', 'w', 'utf-8')]
                    )

def greet_user(bot, update, user_data):
    # bot -экземпляр нашего бота
    # update - данные о прешедшем сообщении
    # user_date - данные о пользователе (словарь)
    '''text ='Вызван /start'
    print(text) # Вывод текста в консоль
    logging.info(text) # Сооб. в bot.log '''
    smile = get_user_emo(user_data)
    user_data ['emo'] = smile
    text = 'Привет {}'.format(smile)
    update.message.reply_text(text, reply_markup=get_keyboard()) # ответ пользователю

def send_cat_picture(bot, update, user_data):
    cat_list = glob('images/cat*.jp*g') # Выводим список картинок
    cat_pic = choice(cat_list) # рандомно выбираем одну картинку из списка
    bot.send_photo(chat_id=update.message.chat.id, photo=open(cat_pic, 'rb'), reply_markup=get_keyboard())
    # ф-ция send_photo(chat_id, photo)- умеет правильно отправлять фото в telegram 

def talk_to_me (bot, update, user_data):
    user_text ='Привет {}{}! Ты написал {}'.format(update.message.chat.first_name, user_data['emo'],
                                update.message.text)
    print(user_text) # печать вх. сообщен в консоль
    # Сохраним в bot.log данные о вх. сообщ.
    logging.info('Users: %s, Chat id: %s, Message: %s', update.message.chat.username,
                update.message.chat.id, update.message.text)
    update.message.reply_text(user_text, reply_markup=get_keyboard()) # ответ пользователю
 
# Функция зименения аватара (смайла)
def change_avatar(bot, update, user_data):
    if 'emo' in user_data:
        del user_data['emo']
    smile = get_user_emo(user_data)
    update.message.reply_text('Готово: {}'.format(smile), reply_markup=get_keyboard())    

# Функция обработки контактов
def get_contact(bot, update, user_data):
    print(update.message.contact)
    update.message.reply_text('Готово: {}'.format(get_user_emo(user_data)), reply_markup=get_keyboard())

# Функция обработки локации
def get_location(bot, update, user_data):
    print(update.message.location)
    update.message.reply_text('Готово: {}'.format(get_user_emo(user_data)), reply_markup=get_keyboard())


# Функция проверки на наличие смайла у пользователя
def get_user_emo(user_data):
    if 'emo' in user_data:
        return user_data['emo']
    else:
        user_data['emo'] = emojize(choice(settings.USER_EMOJI), use_aliases=True)
        return user_data['emo']

# функция обновления клавиатуры (на привязана к команде /start)
def get_keyboard():
    contact_button = KeyboardButton('Прислать контакты', request_contact=True)
    location_button = KeyboardButton('Прислать кооринаты', request_location=True)
    my_keyboard = ReplyKeyboardMarkup([
                                        ['Прислать котика', 'Сменить аватарку'],
                                        [contact_button, location_button]
                                      ], resize_keyboard=True
                                     ) # Добавляем кнопки
    return my_keyboard

def main():
    # mybot - объект класса Updater
    mybot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)
    
    # Добавим в тело нашего бота обработчик команд
    # dispatcher - перераспределяет вх. сообщения по "адресатам"
    dp = mybot.dispatcher
   
    # Если в telegram придет команда start мы на нее среагируем
    # командой greet_user
    dp.add_handler(CommandHandler('start', greet_user,pass_user_data=True))
    #pass_user_data=True - разрешить работу с user_data
    
    # Добавим в тело нашего бота обработчик картинок
    dp.add_handler(CommandHandler('cat', send_cat_picture, pass_user_data=True))

    # Добавим хендлер RegexHandler
    dp.add_handler(RegexHandler('^(Прислать котика)$', send_cat_picture, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Сменить аватарку)$', change_avatar, pass_user_data=True))

    # Добавим хендлеры обработки контактов и геолокации пользователя
    dp.add_handler(MessageHandler(Filters.contact, get_contact, pass_user_data= True))
    dp.add_handler(MessageHandler(Filters.location, get_location, pass_user_data= True))

    # Добавим в тело нашего бота обработчик сообщений
    # Если поступило сообщение, то вызывается ф-ия talk_to_me
    # Filters.text означает что MessageHandler будет реагировать только
    # на текстовые сообщения
    dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True))
    
    logging.info('Бот запускается')
    # Бот постоянно проверяет Telegramm на поступление сообщений
    mybot.start_polling()
    # Бот работает до принудительной остановки
    mybot.idle()

# Вызов функции
main()