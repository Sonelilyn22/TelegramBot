import pandas as pd
import datetime


#Проверка существования dataframe
def check_statistic():
    try:
        df = pd.read_csv('dataframes/statistic.csv')
    except:
        df = pd.DataFrame(columns=['chat_id','user_id','fullname','message','type','date'])
        df.to_csv('dataframes/statistic.csv',index=False)

#Получение dataframe
def get_statistic() -> pd.DataFrame:
    return pd.read_csv('dataframes/statistic.csv')

#Добавление новых записей в dataframe
def save_statistic(chat_id,user_id,fullname,message,type):
    date = datetime.date.today()#Генерация текущей даты
    new_message = {
        'chat_id':chat_id,
        'user_id':user_id,
        'fullname':fullname,
        'message':message,
        'type':type,
        'date':date
    }#Новая запись
    df = get_statistic()
    df.loc[len(df)] = new_message #Добавление новой записи в dataframe
    df.to_csv('dataframes/statistic.csv',index=False)


###### Функции статистики #######


#Получение кол-ва сообщений у конкретного пользователя
def get_user_messages_count(chat_id,user_id) -> str:
    df = get_statistic()
    df = df[(df['chat_id'] == chat_id) & (df['user_id'] == user_id)]
    fullname = df['fullname'][0]
    return f'{fullname} - {len(df)}'

#Получение средней длины сообщений конкретного пользователя
def get_user_messages_len(chat_id,user_id) -> str:
    df = get_statistic()
    df = df[(df['chat_id'] == chat_id) & (df['user_id'] == user_id)]
    fullname = df['fullname'][0]
    messages_len = sum(len(x) for x in df['message'].values)
    messages_count = len(df)
    average = messages_len / messages_count
    return f'{fullname} - {round(average,2)}'

#Получение кол-ва сообщений по пользователям в группе
def get_group_messages_count(chat_id) -> str:
    df = get_statistic()
    df = df[(df['chat_id'] == chat_id)]
    df = df.groupby(df['fullname'])
    result = 'Топ пользователей по кол-ву сообщений \n'
    for fullname,value in df:
        result += f'{fullname} - {len(value)} \n'
    return result 
#Получение средней длины сообщений по пользователям в группе
def get_group_messages_len(chat_id):
    df = get_statistic()
    df = df[(df['chat_id'] == chat_id)]
    df = df.groupby(df['fullname'])
    result = 'Топ пользователей по средней длине сообщений \n'
    for fullname,value in df:
        messages_len = sum(len(x) for x in value['message'].values)
        messages_count = len(value)
        average = messages_len / messages_count
        result += f'{fullname} - {round(average,2)}\n'
    return result

#Получение статистики по типам сообщений у пользователя
def get_user_messages_type(chat_id,user_id) -> str:
    df = get_statistic()
    df = df[(df['chat_id']==chat_id) & (df['user_id'] == user_id)]
    fullname = df['fullname'][0]
    result = f'Типы сообщений у пользователя {fullname}\n'
    for type,count in df['type'].value_counts().items():
        result+=f'Тип:{type} - {count}\n'
    return result

#Авто запуск при запуске бота
check_statistic()

