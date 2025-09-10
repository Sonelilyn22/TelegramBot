#Пример обработчика команд 

from main import bot # В файле main.py создаётся объект бота
from telebot.types import Message

@bot.message_handler(commands=['команда']) #Для создания обработчика команд в message_handler необходимо указать аргумент commands в виде списка со строками
def command_handler(message:Message):#Аргументом функции обработчика всегда является объект типа Message
    #Здесь какая то логика обработки
    #например отправка сообщений
    bot.send_message(message.chat.id,'какой то текст')
