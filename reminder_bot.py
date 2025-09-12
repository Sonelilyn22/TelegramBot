from telebot import TeleBot,types #Библиотека для работы с ботом
import os #Работа с операционной системой
import dotenv #работа с окружением
import threading #модуль многопоточности
import datetime #работа с датами
import time #работа со временем
import pandas #работа с dataframe
import random

#Сохранение в файл .csv
def save_dataframe():
    df.to_csv('dataframes/reminder.csv',index=False)

#Попытка прочтения dataframe
try:
    df = pandas.read_csv('dataframes/reminder.csv')
except:
    df = pandas.DataFrame(columns=['chat_id','date','message'])
    save_dataframe()


dotenv.load_dotenv()
#Получение токена по ключу из файла .env
token = os.environ.get('Api_Token')
#Создание бота
bot = TeleBot(token)

reminder = {} #user_id:{'date':'дата оповещения','message':'что напомнить'}

@bot.message_handler(commands=['start'])
def start(message:types.Message):
    text = 'Этот бот может напомнить вам о ваших делах для этого используйте команду /remind'
    bot.send_message(message.chat.id,text)

@bot.message_handler(commands=['remind'])
def create_remind(message:types.Message):
    text = message.text.split(' ')[1] #/remind 17:40 text -> получим 17:40
    if len(text) != 5 and text.find(':') != -1:
        bot.send_message(message.chat.id,'Введите строку /remind время в формате 00:00')
        return
    now = datetime.datetime.now()
    hours = text[0:2]
    if hours[0] == '0':
        hours = int(hours[1])
    else:
        hours = int(hours)
    minutes = text[3::]
    if minutes[0] == '0':
        minutes = int(minutes[1])
    else:
        minutes = int(minutes)
    date = datetime.datetime(now.year,now.month,now.day,hours,minutes) #Генерация даты для оповещения
    if now >= date:
        date = datetime.datetime(now.year,now.month,now.day+1,hours,minutes) #Если время уже прошло записываем на следующий день
    text = ''
    for element in message.text.split(' ')[2::]:
        text += f'{element} '
    #Записб в словарь
    reminder[message.chat.id] = {
        'date':date,
        'message':text
    }
    #Запись в dataframe
    df.loc[len(df)] = {
        'chat_id':message.chat.id,
        'date':date,
        'message':text
    }
    save_dataframe()
    bot.send_message(message.chat.id,f'Напоминание установлено на {date}')

#Функция оповещений через словарь
def check():
    while True:
        now = datetime.datetime.now()
        chat_ids = []
        for chat_id,value in reminder.items():
            target_date = value['date']
            if now >= target_date:
                bot.send_message(chat_id,value['message'])
                chat_ids.append(chat_id)
        for x in chat_ids:
            reminder.pop(x)
        time.sleep(1)

#Функция оповещний через dataframe
def check_pandas():
    while True:
        now = datetime.datetime.now()
        chat_ids = []
        for index,row in df.iterrows():
            target_date = pandas.to_datetime(row['date'])
            if now >= target_date:
                bot.send_message(row['chat_id'],row['message'])
                chat_ids.append(index)
        for x in chat_ids:
            print(x)
            df.drop(index=x,inplace=True)
        save_dataframe()
        time.sleep(60)


#Создание проверки для оповещения отдельным потоком
t = threading.Thread(target=check_pandas,daemon=True)
t.start()


@bot.message_handler(commands=['8ball'])
def ball_handler(message:types.Message):
    #1 способ
    text = random.choice(['Да','Нет','Спроси позже'])
    bot.send_message(message.chat.id,text)
    #2 способ
    num = random.randint(0,2)
    if num == 0:
        text = 'Да'
    if num == 1:
        text = 'Нет'
    else:
        text = 'Спроси позже'
    bot.send_message(message.chat.id,text)

#Обработка бота
bot.infinity_polling()