from telebot import TeleBot,types,util #Библиотека для работы с ботом
import os#Библиотека для работы с операционной системой
import dotenv #Библиотека для работы с файлами .env
import uuid #Библиотека для генерации уникальных названий
import random #Библиотека для добавления случайности
import dataframe #Наш файл для работы с dataframe
import database #Наш файл для работы с базой данных

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

#Обработка команды /user_stats -> возвращает inline-клавиатуру с кнопками вызова статистик по пользователю
@bot.message_handler(commands=['user_stats'])
def create_user_stat(message:types.Message):
    keyboard = util.quick_markup({
        'Кол-во сообщений':{'callback_data':'user_messages_count'},
        'Средняя длина сообщений':{'callback_data':'user_messages_len'},
        'Типы сообщений':{'callback_data':'user_messages_type'}
    })
    bot.send_message(message.chat.id,'Кнопки вашей статстики',reply_markup=keyboard)

#Обработка команды /user_stats_sql -> возвращает inline-клавиатуру с кнопками вызова статистик по пользователю через database
@bot.message_handler(commands=['user_stats_sql'])
def create_user_stat_sql(message:types.Message):
    keyboard = util.quick_markup({
        'Кол-во сообщений':{'callback_data':'user_messages_count_sql'},
        'Средняя длина сообщений':{'callback_data':'user_messages_len_sql'},
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

#Обработка команды /group_stats -> возвращает inline-клавиатуру с кнопками вызова статистик по чату
@bot.message_handler(commands=['group_stats_sql'])
def create_group_stat_sql(message:types.Message):
    keyboard = util.quick_markup({
        'Кол-во сообщений':{'callback_data':'group_messages_count_sql'},
        'Средняя длина сообщений':{'callback_data':'group_messages_len_sql'}
    })
    bot.send_message(message.chat.id,'Статистика группы',reply_markup=keyboard)

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
        if call.data == 'user_messages_count_sql':
            chat_id = call.message.chat.id
            user_id = call.from_user.id
            result = database.get_user_messages_count(chat_id,user_id)
            bot.send_message(chat_id,result)
        if call.data == 'user_messages_len_sql':
            chat_id = call.message.chat.id
            user_id = call.from_user.id
            result = database.get_user_messages_average_len(chat_id,user_id)
            bot.send_message(chat_id,result)
        if call.data == 'group_messages_count_sql':
            chat_id = call.message.chat.id
            result = database.get_group_messages_count(chat_id)
            bot.send_message(chat_id,result)
#Обработка всех сообщений которые не проверятся другими обработчиками
@bot.message_handler(func=lambda message:True)
def all_messages(message:types.Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    fullname = message.from_user.full_name
    dataframe.save_statistic(chat_id,user_id,fullname,message.text,message.content_type)
    database.save_statistic(message)

bot.infinity_polling()