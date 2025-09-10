#Примеры обработчиков текстовых сообщений !!!Важно такие обработчики должны быть ниже обработчиков команд ибо команда тоже текст
from main import bot
from telebot.types import Message

@bot.message_handler(func=lambda message:True) #Обрабатываются вообще все сообщения которые не обработались другими обработчиками в тч файлы и команды
def message_handler(message:Message):
    #Какая то логика обработки
    #Например отправка сообщения
    bot.send_message(message.chat.id,'какой то текст')

@bot.message_handler(content_types=['text']) #для обработки только текстовых команд можно задать тип как text
def message_text_handler(message:Message):
    #Какая то логика обработки
    #Например отправка сообщения
    bot.send_message(message.chat.id,'какой то текст')
