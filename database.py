import sqlite3
from telebot.types import Message
import datetime

#Подключение или создание бд
db = sqlite3.connect('databases/statistic.db',check_same_thread=False)

#Создание таблицы
def create_table():
    try:
        cursor = db.cursor()
        cursor.execute('CREATE TABLE messages(chat_id,user_id,fullname,text,type,date) ')
        cursor.close()
    except:
        pass

#Получение кол-ва сообщений по пользователю
def get_user_messages_count(chat_id,user_id):
    cursor = db.cursor()
    query = f'''select * from messages where (chat_id == {chat_id} and user_id == {user_id}) '''
    cursor.execute(query)
    messages = cursor.fetchall()
    if len(messages) > 0 or messages != None:
        fullname = messages[0][2]
        print(fullname,'-',len(messages))
        return f'{fullname} - {len(messages)}'
    else:
        return 'Вы ещё не отправляли сообщения'

#Получить среднюю длину сообщений по пользователю
def get_user_messages_average_len(chat_id,user_id):
    cursor = db.cursor()
    query = f'''select text,fullname from messages where (chat_id == {chat_id} and user_id == {user_id}) '''
    cursor.execute(query)
    messages = cursor.fetchall()
    if len(messages) > 0 or messages != None:
        messages_len = 0
        for text,name in messages:
            messages_len += len(text)
        messages_count = len(messages)
        average_len = messages_len/messages_count
        fullname = messages[0][1]
        print(fullname,'-',average_len)
        return f'{fullname} - {average_len}'
    else:
        return 'Вы ещё не отправляли сообщения'
    
#Получение кол-ва сообщений по чату
def get_group_messages_count(chat_id):
    cursor = db.cursor()
    query = f'select fullname,count(*) from messages where(chat_id == {chat_id}) group by (fullname) '
    cursor.execute(query)
    messages = cursor.fetchall()
    if len(messages) > 0 or messages != None: 
        result = 'Топ пользователей по кол-ву сообщений \n'
        for name,count in messages:
            result+= f'{name} - {count} сообщений \n'
        print(result)
        return result
    else:
        return 'В чате ещё не было сообщений'

#Сохранение статистики
def save_statistic(message:Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    fullname = message.from_user.full_name
    text = message.text
    type = message.content_type
    date = datetime.datetime.today()
    query = f''' insert into messages values(?,?,?,?,?,?)'''
    cursor = db.cursor()
    cursor.execute(query,(chat_id,user_id,fullname,text,type,date))
    cursor.close()
    db.commit()


create_table()
