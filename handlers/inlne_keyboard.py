
#Обработка команды /inline_keyboard_url -> возвращает inline-клавиатуру с кнопкой переадрисации на ютуб
@bot.message_handler(commands=['inline_keyboard_url'])
def inline_keyboard_url(message:types.Message):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    button = types.InlineKeyboardButton('Ютуб','https://www.youtube.com/')
    keyboard.add(button)
    bot.send_message(message.chat.id,'Вот ссылки',reply_markup=keyboard)

#Обработка команды /inline_keyboard_data -> возвращает inline-клавиатуру с кнопками (Переадрисации,обработку callback_data)
@bot.message_handler(commands=['inline_keyboard_data'])
def inline_keyboard_url(message:types.Message):
    keyboard = util.quick_markup(
        {
            'Ютуб':{'url':'https://www.youtube.com/'},
            'Data':{'callback_data':'test'}
        }
    )
    bot.send_message(message.chat.id,'Вот ссылки',reply_markup=keyboard)