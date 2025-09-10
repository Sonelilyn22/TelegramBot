#Пример обработки нажатий на inline-клавиатуру

from main import bot
from telebot.types import CallbackQuery

@bot.callback_query_handler(func=lambda call:True)#Обработка нажатия на inline-клавиатуру
def callback_handler(call:CallbackQuery):#Аргументом вызова callback_query_handler всегда является объект типа CallbackQuery
    if call.message:#Проверка на нажатие inline кнопок
        if call.data == 'текст':#Значение свойства callback_data у inline кнопки
            #Какое то действие например отправка сообщения
            bot.send_message(call.message.chat.id,'какой то текст')
