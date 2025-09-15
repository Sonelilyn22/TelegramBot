from telebot import TeleBot,types,util
import pandas
import os
import dotenv
import json

def get_or_create_df(name:str,columns:list):
    try:
        df = pandas.read_csv(f'dataframes/{name}.csv')
    except:
        df = pandas.DataFrame(columns=columns)
        df.to_csv(f'dataframes/{name}.csv',index=False)
    return df

def get_or_create_food():
    try:
        df = pandas.read_csv(f'dataframes/food.csv')
    except:
        df = pandas.DataFrame(columns=['name','image_url','category','ingredients','cost'])
        df.loc[len(df)] = {
            'name':'Маргарита',
            'image_url':'images/margarita.jpg',
            'category':'Пицца',
            'ingredients':['Моцарелла','Помидоры'],
            'cost':550
        }
        df.loc[len(df)] = {
            'name':'филадельфия',
            'image_url':'images/roll.jpg',
            'category':'роллы',
            'ingredients':['Сёмга','Рис','Нори'],
            'cost':450
        }
        df.to_csv(f'dataframes/food.csv',index=False)
    return df

def check_user(chat_id):#Проверка на существование пользователей
    user = users[users['chat_id'] == chat_id]
    if len(user) > 0:
        return True
    return False

def save_user(message:types.Message):#Сохранение пользователя
    if message.contact != None:
        chat_id = message.chat.id
        user = message.from_user
        phone = message.contact.phone_number
        new_user = {
            'chat_id':chat_id,
            'user_id':user.id,
            'first_name':user.first_name,
            'last_name':user.last_name,
            'username':user.username,
            'phone':phone
        }
        users.loc[len(users)] = new_user
        users.to_csv('dataframes/users.csv',index=False)
        bot.reply_to(message,'Успешно')
        user_keyboard(chat_id)
    else:
        bot.reply_to(message,'Произошла ошибка попробуйте снова')

def user_keyboard(chat_id,call = None):
    keyboard = util.quick_markup(
        {
            'Профиль':{'callback_data':'user_profile'},
            'Заказать':{'callback_data':'user_order'},
            'История':{'callback_data':'user_history'}
        }
    )
    if call == None:
        bot.send_message(chat_id,'Меню',reply_markup=keyboard)
    else:
        bot.edit_message_text('Меню',chat_id,call.message.id,reply_markup=keyboard)

def user_handler(call:types.CallbackQuery):#Вызов обработок нажатий пользователя
    if call.data == 'user_profile':
        user_profile(call)
    if call.data == 'user_order':
        user_order(call)
    if call.data == 'user_history':
        pass
    if call.data == 'user_delete':
        user_delete(call)
    if call.data == 'user_menu':
        user_keyboard(call.message.chat.id,call)
    if call.data == 'user_cart':
        user_cart(call)

def user_profile(call:types.CallbackQuery):#Профиль пользователя
    user = users[users['user_id'] == call.from_user.id]
    first_name = user['first_name'].values[0]
    last_name = user['last_name'].values[0]
    username = user['username'].values[0]
    phone = user['phone'].values[0]
    text = f'Фамилия:{last_name}\nИмя:{first_name}\nПользователь:@{username}\nТелефон:{phone}'
    keyboard = util.quick_markup(
        {
        'Удалить':{'callback_data':'user_delete'},
        'Назад':{'callback_data':'user_menu'}
        }
    )
    bot.edit_message_text(f'Профиль\n{text}',call.message.chat.id,call.message.id,reply_markup=keyboard)

def user_delete(call:types.CallbackQuery):#Нажатие на кнопку удалить в профиле
    user_id = call.from_user.id
    user_index = users[users['user_id'] == user_id].index
    users.drop(index=user_index,inplace=True)
    users.to_csv('dataframes/users.csv',index=False)
    bot.edit_message_text('Профиль удалён',call.message.chat.id,call.message.id,reply_markup=None)

def user_order(call:types.CallbackQuery):#Нажате на кнопку заказ 
    message = call.message
    buttons = {}
    for index,row in food.iterrows():
        name = row['name']
        buttons[name] = {'callback_data':f'order_{index}'}
    if check_cart(call.from_user.id):#Есть что-то в корзине
        buttons['Корзина'] = {'callback_data':'user_cart'}
    buttons['Назад'] = {'callback_data':'user_menu'}
    keyboard = util.quick_markup(buttons)
    if message.text:#Если обычные переходы
        bot.edit_message_text('Асортимент',call.message.chat.id,call.message.id,reply_markup=keyboard)
    else:#Если возвращаемся с заказа еды
        bot.delete_message(call.message.chat.id,message.id)#Удалим старое сообщение с фотографией
        bot.send_message(call.message.chat.id,'Асортимент',reply_markup=keyboard)

def user_cart(call:types.CallbackQuery):#Корзина пользователя #FIXME
    buttons = {}
    user_id = call.from_user.id
    row = cart[cart['user_id'] == user_id]
    index,usercart = next(row.iterrows())
    food_ids = json.loads(usercart['food_ids'])
    cart_food = {} #Будет хранится еда в корзине
    for index in food_ids.keys():
        local_food = food.loc[index]
        cart_food[index] = local_food['name']
    for index,name in cart_food.items():
        buttons['-'] = {'callback_data':f'order_{index}_minus'}
        buttons[{name}] = {'callback_data':''}
        buttons['+'] = {'callback_data':f'order_{index}_plus'}
    keyboard = util.quick_markup(buttons,3)
    bot.edit_message_text('Корзина',call.message.chat.id,call.message.id,reply_markup=keyboard)

def order_handler(call:types.CallbackQuery):#Вызов обработок при нажати в заказах
    data = call.data.split('_')
    if len(data) == 2:
        get_food(call)
    else:
        if data[2] == 'add':
            order_add(call)
        if data[2] == 'plus':#Увеличение кол-ва
            pass
        if data[2] == 'minus':#Уменьшение кол-ва
            pass
        if data[2] == 'delete':#Удаление еды из заказа
            pass

def get_food(call:types.CallbackQuery):
    index = int(call.data.split('_')[1])
    row = food.loc[index]
    desc,image_url = create_order_description(row) 
    image = types.InputMediaPhoto(types.InputFile(image_url),desc)
    keyboard = order_keyboard(index)
    bot.edit_message_media(image,call.message.chat.id,call.message.id,reply_markup=keyboard)

def order_add(call:types.CallbackQuery):#Добавление заказа ###FIXME
    user_id = call.from_user.id
    index = call.data.split('_')[1]
    if check_cart(user_id):
        cart_index,user_cart = get_cart(user_id)
    else:
        create_cart(user_id)
        cart_index,user_cart = get_cart(user_id)
    print(user_cart['food_ids'])
    food_ids = json.loads(user_cart['food_ids'])
    print(food_ids)
    if index not in food_ids:
        food_ids[index] = 1
    updated_cart = {
        'user_id':user_id,
        'food_ids':food_ids
    }
    cart.loc[cart_index] = updated_cart
    cart.to_csv('dataframes/cart.csv',index=False)
    #Возможно добавить переход в корзину

def check_cart(user_id:int):#Проверка на существование корзины
    user_cart = cart[cart['user_id']==user_id]
    if len(user_cart) > 0:
        return True #Существует
    return False   #Отсутствует

def create_cart(user_id:int):#Создание корзины
    new_cart = {
        'user_id':user_id,
        'food_ids':{}
    }
    cart.loc[len(cart)] = new_cart
    cart.to_csv('dataframes/cart.csv',index=False) #Сохраняем в файл

def get_cart(user_id:int):#Получение корзины ###
    row = cart[cart['user_id'] == user_id]
    index,user_cart = next(row.iterrows())
    return index,user_cart

def order_keyboard(index:int):
    keyboard = util.quick_markup({
        'Добавить':{'callback_data':f'order_{index}_add'},
        'Назад':{'callback_data':'user_order'}
    })
    return keyboard

def create_order_description(row:pandas.Series):
    name,image_url,category,ingridients,cost = row.values
    descrtipton = f'Название:{name}\nКатегория:{category}\nИнгридиенты:'
    for element in ingridients:#Добавление ингридиентов
        descrtipton += f'{element} '
    descrtipton += f'\nЦена:{cost} руб.'
    return descrtipton,image_url

dotenv.load_dotenv()

api_token = os.environ.get('Api_Token')
bot = TeleBot(api_token)

@bot.message_handler(commands=['start'])
def command_start(message:types.Message):
    chat_id = message.chat.id
    if message.from_user.id in admins_id:#Проверка на то что пользователь является администратором
        return
    if not check_user(chat_id):
        keyboard = types.ReplyKeyboardMarkup()
        contact_btn = types.KeyboardButton('Поделится контактом',True)
        keyboard.add(contact_btn)
        text = 'Для работы необходимо зарегистрироваться для продожения поделитсь контактом'
        bot.reply_to(message,text,reply_markup = keyboard)
        bot.register_next_step_handler(message,save_user) #позволяет отследить следующее сообщение
    else:
       user_keyboard(chat_id)

@bot.message_handler(commands=['dump_user']) #Команда которая будет очищать users.csv
def command_dump_user(message):
    global users
    users = pandas.DataFrame(columns=['chat_id','user_id','first_name','last_name','username','phone'])
    users.to_csv('dataframes/users.csv',index=False)

@bot.callback_query_handler(func=lambda call:True)#Обработка нажатий на клавиатуру
def callback_handler(call:types.CallbackQuery):
    if call.message:
        if call.data.startswith('user'):
            user_handler(call)
        if call.data.startswith('order'):
            order_handler(call)

if __name__ == '__main__':#Проверка на то что запустили этот файл
    users = get_or_create_df('users',['chat_id','user_id','first_name','last_name','username','phone']) #Пользователи
    food = get_or_create_food()#Пища
    cart = get_or_create_df('cart',['user_id','food_ids'])#Корзина
    orders = get_or_create_df('orders',['user_name','food_ids','total_cost','status'])#Заказы
    admins_id = []
    bot.infinity_polling()