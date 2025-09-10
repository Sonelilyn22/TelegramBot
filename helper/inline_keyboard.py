#Пример создания inline_keyboard

from main import bot # В файле main.py создаётся объект бота
from telebot.types import Message,InlineKeyboardMarkup,InlineKeyboardButton #Сообщение,клавиатура,кнопки

@bot.message_handler(commands=['inline_keyboard']) #Проще всего вызвать клавиатуры с помощью команд
def create_inline_keyboard(message:Message):
    keyboard = InlineKeyboardMarkup()
    #Класс для создания встроенной (inline) клавиатуры, которая появляется прямо под сообщением и возвращает данные боту без отправки нового сообщения в чат
    #Аргуметы
    #inline_keyboard - Список строк, каждая из которых — список объектов InlineKeyboardButton.
    #row_width - Если вы используете метод .add(), кнопки будут автоматически разбиты на строки по этому числу.
    button = InlineKeyboardButton(text='какой то текст',callback_data='какой то текст') #InlineKeyboardButton — кнопка встроенной клавиатуры (InlineKeyboardButton)
    #text - Текст на кнопке, который видит пользователь.
    #callback_data: - данные, которые Telegram вернет боту в обновлении callback_query при нажатии кнопки.
    #url - URL для открытия в браузере Telegram-клиента при нажатии кнопки.
    #switch_inline_query - переключение в режим inline search прямо из чата.
    #switch_inline_query_current_chat - аналогично, но поиск будет выполняться в текущем чате.
    #pay - товара/услуги через Telegram Pay (доступно не во всех сценариях).
    #login_url - URL для аутентификации через встроенный логин-URL (для некоторых кейсов авторизации).
    #game - запуск игры (если кнопка связана с игрой Telegram).
    #need_user_info - запрос информации о пользователе (де-факто редко используется в клиентской части; поддержка зависит от версии API).
    #poll - создание опроса напрямую через кнопку (ограничено поддержкой клиента).
    keyboard.add(button) #Добавление кнопки на клавиатуру
    #для того чтобы показать клавиатуру её необходимо отправить сообщением с аргументом reply_markup
    #Примеры
    bot.send_message(message.chat.id,'какой то текст',reply_markup=keyboard)#отправка новым сообщением

    bot.reply_to(message,'какой то текст',reply_markup=keyboard)#отправка ответом на сообщение
