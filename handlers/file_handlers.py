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
    chat_id = message.chat.id
    user_id = message.from_user.id
    fullname = message.from_user.full_name
    message_text = message.caption
    content_type = message.content_type
    dataframe.save_statistic(chat_id,user_id,fullname,message_text,content_type)

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
    chat_id = message.chat.id
    user_id = message.from_user.id
    fullname = message.from_user.full_name
    message_text = message.caption
    content_type = message.content_type
    dataframe.save_statistic(chat_id,user_id,fullname,message_text,content_type)

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
    chat_id = message.chat.id
    user_id = message.from_user.id
    fullname = message.from_user.full_name
    message_text = message.caption
    content_type = message.content_type
    dataframe.save_statistic(chat_id,user_id,fullname,message_text,content_type)