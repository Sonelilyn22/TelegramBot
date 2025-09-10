#Пример обработчика файлов 

from main import bot
from telebot.types import Message

@bot.message_handler(content_types=['photo'])
    #content_types=['audio', 'photo', 'voice', 'video', 'document','text', 'location', 'contact', 'sticker']
    # В зависимости от типа контента для обработки этого контента надо вызывать message.тип -> message.photo
def file_handler(message:Message):
    #Какая то логика
    #например отправка сообщений об id файла
    #так как content_types=['photo'] то для обработки используем свойстов .photo 
    file_id = message.photo[-1].file_id
    bot.send_message(message.chat.id,f'Вот id вашего файла:{file_id}')



