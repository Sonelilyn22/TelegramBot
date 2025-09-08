from telebot import TeleBot,types,util #Библиотека для работы с ботом
import os#Библиотека для работы с операционной системой
import dotenv #Библиотека для работы с файлами .env
import uuid #Библиотека для генерации уникальных названий
import random #Библиотека для добавления случайности
import dataframe #Наш файл для работы с dataframe

#Создание папки для хранения файлов
def create_chat_folder(chatId):
    os.makedirs(f'uploads/{chatId}',exist_ok=True)

dotenv.load_dotenv()
#Получение токена по ключу из файла .env
token = os.environ.get('Api_Token')
#Создание бота
bot = TeleBot(token)

#Обработка команды /start
@bot.message_handler(commands=['start'])
def start(message:types.Message):
    bot.send_message(message.chat.id,'Я тестовый бот')
#Обработка команды /random
@bot.message_handler(commands=['random'])
def message_random(message:types.Message):
    text = random.choice(['text1','text2','text3'])
    bot.send_message(message.chat.id,text)
#Обработка команды /reply_keyboard -> возвращает reply-клавиатуру
@bot.message_handler(commands=['reply_keyboard'])
def reply_keyboard(message:types.Message):
    keyboard = types.ReplyKeyboardMarkup(True,True)
    button = types.KeyboardButton('/random')
    keyboard.add(button)
    bot.send_message(message.chat.id,'Клавиатура:',reply_markup=keyboard)
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
#Обработка команды /location -> возвращает reply-клавиатуру с запросом геоданных !!!работает только для телефонов
@bot.message_handler(commands=['location'])
def reply_location(message:types.Message):
    keyboard = types.ReplyKeyboardMarkup()
    button = types.KeyboardButton('Поделится локацией',request_location=True)
    keyboard.add(button)
    bot.send_message(message.chat.id,'Дай локацию',reply_markup=keyboard)
#Обработка команды /messages_count -> возвращает статистику по кол-ву отправленных сообщений пользователем
@bot.message_handler(commands=['messages_count'])
def get_user_messages_count(message:types.Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    result = dataframe.get_user_messages_count(chat_id,user_id)
    bot.send_message(message.chat.id,result)
#Обработка команды /user_stats -> возвращает inline-клавиатуру с кнопками вызова статистик по пользователю
@bot.message_handler(commands=['user_stats'])
def create_user_stat(message:types.Message):
    keyboard = util.quick_markup({
        'Кол-во сообщений':{'callback_data':'user_messages_count'},
        'Средняя длина сообщений':{'callback_data':'user_messages_len'},
        'Типы сообщений':{'callback_data':'user_messages_type'}
    })
    bot.send_message(message.chat.id,'Кнопки вашей статстики',reply_markup=keyboard)
#Обработка команды /group_stats -> возвращает inline-клавиатуру с кнопками вызова статистик по чату
@bot.message_handler(commands=['group_stats'])
def create_group_stat(message:types.Message):
    keyboard = util.quick_markup({
        'Кол-во сообщений':{'callback_data':'group_messages_count'},
        'Средняя длина сообщений':{'callback_data':'group_messages_len'}
    })
    bot.send_message(message.chat.id,'Статистика группы',reply_markup=keyboard)
#Обработка отправки фото в чат -> сохраняет в папку проекта файл
@bot.message_handler(content_types=['photo'])
def OnSendImage(message:types.Message):
    create_chat_folder(str(message.chat.id))
    photo = message.photo[-1] #Указываем -1 элемент так как в message.photo хранится файл в разных разришениях
    filepath = bot.get_file(photo.file_id).file_path #Получаем путь к файлу по его id
    file = bot.download_file(filepath) #Загружаем этот файл по пути
    filename = uuid.uuid4()
    with open(f'uploads/{str(message.chat.id)}/{filename}.jpg','wb') as newfile:
        newfile.write(file)
    bot.reply_to(message,f'Вы отправили изображение:{filepath}')
#Обработка отправки аудио в чат -> сохраняет в папку проекта файл
@bot.message_handler(content_types=['audio'])
def OnSendAudio(message:types.Message):
    chatId = str(message.chat.id)
    create_chat_folder(chatId)
    audio = message.audio
    filepath = bot.get_file(audio.file_id).file_path
    file = bot.download_file(filepath)
    filename = uuid.uuid4()
    with open(f'uploads/{chatId}/{filename}.mp3','wb') as newfile:
        newfile.write(file)
    bot.reply_to(message,'Аудио сохранено')
#Обработка отправки видео в чат -> сохраняет в папку проекта файл
@bot.message_handler(content_types=['video'])
def OnSendVideo(message:types.Message):
    chatId = str(message.chat.id)
    create_chat_folder(chatId)
    video = message.video
    filepath = bot.get_file(video.file_id).file_path
    file = bot.download_file(filepath)
    filename = uuid.uuid4()
    with open(f'uploads/{chatId}/{filename}.mp4','wb') as newfile:
        newfile.write(file)
    bot.reply_to(message,'Видео сохранено')
#Обработка нажатий на inline-клавиатуры    
@bot.callback_query_handler(func=lambda call:True)
def callback_handler(call:types.CallbackQuery):
    if call.message:
        if call.data == 'test':
            bot.send_message(call.message.chat.id,'Вы нажали на inline кнопку')
            bot.edit_message_reply_markup(call.message.chat.id,call.message.id,reply_markup=None)
        if call.data == 'user_messages_count':
            chat_id = call.message.chat.id
            user_id = call.from_user.id
            result = dataframe.get_user_messages_count(chat_id,user_id)
            bot.send_message(chat_id,result)
        if call.data == 'user_messages_len':
            chat_id = call.message.chat.id
            user_id = call.from_user.id
            result = dataframe.get_user_messages_len(chat_id,user_id)
            bot.send_message(chat_id,result)
        if call.data == 'group_messages_count':
            chat_id = call.message.chat.id
            result = dataframe.get_group_messages_count(chat_id)
            bot.send_message(chat_id,result)
        if call.data == 'group_messages_len':
            chat_id = call.message.chat.id
            result = dataframe.get_group_messages_len(chat_id)
            bot.send_message(chat_id,result)
        if call.data == 'user_messages_type':
            chat_id = call.message.chat.id
            user_id = call.from_user.id
            result = dataframe.get_user_messages_type(chat_id,user_id)
            bot.send_message(chat_id,result)
#Обработка всех сообщений которые не проверятся другими обработчиками
@bot.message_handler(func=lambda message:True)
def all_messages(message:types.Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    fullname = message.from_user.full_name
    dataframe.save_statistic(chat_id,user_id,fullname,message.text,message.content_type)

bot.infinity_polling()