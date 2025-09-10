from telebot import TeleBot,types #Библиотека для работы с ботом
from random import randint
import os
import dotenv

dotenv.load_dotenv()
#Получение токена по ключу из файла .env
token = os.environ.get('Api_Token')
#Создание бота
bot = TeleBot(token)

games = {} #user_id:число которое мы загадали

@bot.message_handler(commands=['start_game']) #Команда начала игры
def start_game(message:types.Message):
    user_id = message.from_user.id
    num = randint(1,20)
    games[user_id] = {'target':num,'count':0}
    print(games)

@bot.message_handler(func=lambda message:True)
def message_handler(message:types.Message):
    user_id = message.from_user.id
    if user_id not in games:#Проверка на то что пользователь начал игру
        bot.send_message(message.chat.id,'Вы ещё игру используйте команду /start_game')
        return
    text = message.text
    if not text.isdigit():#Проверка на то что пользователь отправил число
        bot.send_message(message.chat.id,'Введите число от 1 до 20')
        return
    game = games[user_id]['target']
    if int(text)>game:
        bot.send_message(message.chat.id,'Загаданое мной число меньше')
        games[user_id]['count'] += 1
        return
    if int(text)<game:
        bot.send_message(message.chat.id,'Загаданое мной число больше')
        games[user_id]['count'] += 1
        return
    if int(text) == game:
        count = games[user_id]['count']
        games.pop(user_id)
        bot.send_message(message.chat.id,f'Вы успешно отгадали число с {count} попытки')


bot.infinity_polling()
    
    
