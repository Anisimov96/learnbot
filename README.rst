CatBot
======

CatBot - это бот для Telegram, созданный с целью сделать
вашу жизнь лучше, присылая вам фотографии котиков

Установка
---------
Создайте виртуальное окружение и активируйте его.
Потом в виртуальном окружении выполните.
.. code-block:: text
    pip install -r requirements.txt

Полжите картинки с котиками в папку images.
Название файлов должно начинаться с cat, а заканчиваться с .jpg
Например cat12234555.jpg

Настройка
---------
Создайте файл settings.py добавте туда следующие настройки
.. code-block:: python
    PROXY = {'proxy_url': 'socks5h://Ваш_SOCKS5H_Прокси:1080',
        'urllib3_proxy_kwargs': {'username': 'ЛОГИН', 'password': 'ПАРОЛЬ'}}

    API_KEY = "API ключ, полученный от BotFather "

    USER_EMOJI = [':poop:',':smiley_cat:', ':smiling_imp:', ':panda_face:', ':dog:']

Запуск
------
В активированном виртуальном окружении выполните:
.. code-block:: text
    python bot.py