#Обработка команды /location -> возвращает reply-клавиатуру с запросом геоданных !!!работает только для телефонов
@bot.message_handler(commands=['location'])
def reply_location(message:types.Message):
    keyboard = types.ReplyKeyboardMarkup()
    button = types.KeyboardButton('Поделится локацией',request_location=True)
    keyboard.add(button)
    bot.send_message(message.chat.id,'Дай локацию',reply_markup=keyboard)

#Обработка команды /reply_keyboard -> возвращает reply-клавиатуру
@bot.message_handler(commands=['reply_keyboard'])
def reply_keyboard(message:types.Message):
    keyboard = types.ReplyKeyboardMarkup(True,True)
    button = types.KeyboardButton('/random')
    keyboard.add(button)
    bot.send_message(message.chat.id,'Клавиатура:',reply_markup=keyboard)