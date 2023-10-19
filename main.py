
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ContentType
from classes.user import User, dad_admin, cityes, son_admin
from classes.event import Event
from data.base_file import userbase, eventbase, sort_eventbase,sort_after_delete
import pathlib
from pathlib import Path
dir_path = pathlib.Path.cwd()

#МАШИНА СОСТОЯНИЙ
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
storage=MemoryStorage()

class StepsForm(StatesGroup):
    get_fio=State()
    get_phone=State()
    get_date=State()

class AddEvent(StatesGroup):
    get_name=State()
    get_date=State()
    get_time=State()
    get_location = State()
    get_url = State()
    get_description = State()
    get_vzletbusiness = State()
    get_photo = State()


bot = Bot(token = "6100104762:AAEJWgdFyucF-6cUgyrzlzazLMZccxoZYB8",
          parse_mode="HTML")
dp = Dispatcher(bot,storage=MemoryStorage())

statisticbot = Bot(token = "6681358573:AAEDPtrd3jNn82es9LS69eDOicI0ih9FSxk",
                   parse_mode="HTML")



eventbase["0"] = Event(name="Встреча клуба Росмолодежь.Бизнес",
                       url_to_tgchat="https://t.me/+9PY3bcf3ZH01MDZi",
                       photo_path=Path(dir_path, "files", "photo", "rosmol.jpg"),
                       description="Тут будет описание",
                       date = "16.03.2024",
                       time = "12:00",
                       creator="5965231899",
                       location = "Культурная станция Гагарин. Маерчака 17",
                       vzletbusiness=True)

eventbase["1"] = Event(name="Я в деле",
                       url_to_tgchat="https://t.me/+9PY3bcf3ZH01MDZi",
                       photo_path=Path(dir_path, "files", "photo", "yavdele.jpg"),
                       description="Предпринимательский кейс-чемпионат. Создай свой бизнес-проект с помощью наставников",
                       date = "15.03.2024",
                       time = "12:00",
                       creator="5965231899",
                       location = "Культурная станция Гагарин. Маерчака 17",
                       vzletbusiness=True)

eventbase["2"] = Event(name="Битва Креаторов",
                       url_to_tgchat="https://t.me/+9PY3bcf3ZH01MDZi",
                       photo_path=Path(dir_path, "files", "photo", "institut.jpg"),
                       description="приходите пж",
                       date = "11.03.2024",
                       time = "12:00",
                       creator="5965231899",
                       location = "Культурная станция Гагарин. Маерчака 17",
                       vzletbusiness=True)


#Старт
@dp.message_handler(commands=["start"])
async def start(message: types.Message):

    #удаляем сообщение
    await message.delete()

    #добавляем пользователя в базу данных
    if str(message.from_user.id) not in userbase:
        userbase[str(message.from_user.id)] = User(username=message.from_user.username,
                                                   id = message.from_user.id)

    #получаем объект класса юзер. Чисто для укорачивания кода
    user = userbase[str(message.from_user.id)]

    #добавляем действие
    await user.AddAction("start")

    #создаем клавиатуру
    ikb = InlineKeyboardMarkup()
    for city in cityes:
        ikb.add(InlineKeyboardButton(text=f"📍 {city}",callback_data=city))
    ikb.add(InlineKeyboardButton(text="Скоро новые города!", callback_data="Krasnoyarsk"))

    #получаем фото
    png = open(Path(dir_path,"files", "photo", "start.png"),"rb")

    #отправляем сообщение
    msg = await bot.send_photo(caption="Привет, я креативный стартап Взлёт! Выбери свой город",
                               reply_markup = ikb,
                               chat_id = user.id,
                               photo = png)
    png.close()

    #оповещаем админов о новых пользователях
    for adm in dad_admin:
        await statisticbot.send_message(chat_id=adm,
                                        text=f"Новый пользователь\n\n"
                                             f"{await user.GetInfo()}")

    #сохраняем последнее сообщение
    user.last_message = msg.message_id


#Главное меню
@dp.callback_query_handler(text = cityes)
async def city(message: types.CallbackQuery):

    # получаем объект класса юзер. Чисто для укорачивания кода
    user = userbase[str(message.from_user.id)]

    # Обнуляем карусель
    user.location = None

    #Добавляем юзеру город
    user.city = message.data

    # добавляем действие
    await user.AddAction(f"Выбрал {message.data}")

    #клавиатура
    ikb = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(text = "Мероприятия", callback_data="eventsnext")
    btn2 = InlineKeyboardButton(text = "Обучение", callback_data = "learning")
    btn3 = InlineKeyboardButton(text = "Стажировки", callback_data = "work")
    btn4 = InlineKeyboardButton(text="Взлёт.Бизнес", callback_data="business")
    ikb.add(btn1).add(btn2).add(btn3).add(btn4)

    #Получаем фото
    png = open(Path(dir_path,"files", "photo", "cityes.png"),"rb")
    photo = types.InputMediaPhoto(png, caption="Здесь собраны все самые классные возможности твоего города")

    #Редактируем сообщения
    await bot.edit_message_media(chat_id=user.id,
                                 message_id = user.last_message,
                                 media = photo,
                                 reply_markup=ikb)

    png.close()



callback_location = [f"event_registration_{index}" for index in range(0,1000)]
callback_delete_event = [f"delete_event_{index}" for index in range(0,1000)]

#Движение по карусели эвентам
@dp.callback_query_handler(text=["eventsnext","eventsback"])
async def events1(message: types.CallbackQuery):

    # получаем объект класса юзер. Чисто для укорачивания кода
    user = userbase[str(message.from_user.id)]

    # добавляем действие
    await user.AddAction(f"листнул на эвент")

    #Движение по карусели
    if user.location == None:
        user.location = "0"

    elif message.data == "eventsnext":
        if int(user.location) < len(eventbase)-1:
            user.location = str(int(user.location) + 1)
        else:
            user.location = "0"
    else:
        if int(user.location) > 0:
            user.location = str(int(user.location) - 1)
        else:
            user.location = str(len(eventbase)-1)

    #получаем из базы событие
    event = eventbase[user.location]

    # клавиатура
    ikb = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(text="Назад", callback_data="eventsback")
    btn2 = InlineKeyboardButton(text="Далее", callback_data="eventsnext")
    btn3 = InlineKeyboardButton(text="🕹 Зарегистрироваться", callback_data=f"event_registration_{user.location}")
    btn5 = InlineKeyboardButton(text="🗂 Главное меню", callback_data=user.city)
    ikb.row(btn1,btn2).add(btn3).add(btn5)

    if str(user.id) in son_admin:
        ikb.add(InlineKeyboardButton(text="Добавить мероприятие {admin}", callback_data="add_event"))
        ikb.add(InlineKeyboardButton(text="Удалить мероприятие {admin}", callback_data=f"delete_event_{user.location}"))


    png = open(event.photo_path, "rb")
    photo = types.InputMediaPhoto(png, caption=f"<b>{event.name}</b>\n\n"
                                               f"{event.description}\n\n"
                                               f"<b>Дата:</b> {event.date}\n"
                                               f"<b>Время:</b> {event.time}")

    # Редактируем сообщения
    await bot.edit_message_media(chat_id=user.id,
                                 message_id=user.last_message,
                                 media=photo,
                                 reply_markup=ikb)

    png.close()



#Регистрация
@dp.callback_query_handler(text = callback_location)
async def registration1(message: types.CallbackQuery):

    # получаем объект класса юзер. Чисто для укорачивания кода
    user = userbase[str(message.from_user.id)]

    user.registration_hub = eventbase[message.data[-1]]

    #добавляем картинку и текст
    png = open(user.registration_hub.photo_path,"rb")
    photo = types.InputMediaPhoto(png, caption=f"<i>🕹 Регистрация</i>\n\n"
                                               f"<b>🎟 Событие:</b>\n<code>{user.registration_hub.name}</code>\n\n"
                                               f"<b>🗓 Дата:</b>\n<code>{user.registration_hub.date} {user.registration_hub.time}</code>\n\n"
                                               f"<b>📍 Место:</b>\n<code>{user.registration_hub.location}</code>\n\n"
                                               f"<b>⚠️ Введи ФИО</b>")

    # Редактируем сообщения
    await bot.edit_message_media(chat_id=user.id,
                                 message_id=user.last_message,
                                 media=photo)

    await StepsForm.get_fio.set()

@dp.message_handler(state=StepsForm.get_fio)
async def registration2(message: types.Message, state: FSMContext):

    # получаем объект класса юзер. Чисто для укорачивания кода
    user = userbase[str(message.from_user.id)]

    #удаляем сообщение пользователя
    await message.delete()

    #Добавляем ФИО в базу
    user.fio = message.text

    # добавляем действие
    await user.AddAction(f"Имя: {user.fio}")

    # добавляем картинку и текст
    png = open(user.registration_hub.photo_path, "rb")
    photo = types.InputMediaPhoto(png, caption=f"<i>🕹 Регистрация</i>\n\n"
                                               f"<b>🎟 Событие:</b>\n<code>{user.registration_hub.name}</code>\n\n"
                                               f"<b>🗓 Дата:</b>\n<code>{user.registration_hub.date} {user.registration_hub.time}</code>\n\n"
                                               f"<b>📍 Место:</b>\n<code>{user.registration_hub.location}</code>\n\n"
                                               f"<b>🙎‍♂️ ФИО:</b>\n<code>{user.fio}</code>\n\n"
                                               f"<b>⚠️Введи номер телефона</b>")

    # Редактируем сообщения
    await bot.edit_message_media(chat_id=user.id,
                                 message_id=user.last_message,
                                 media=photo)

    await StepsForm.get_phone.set()

@dp.message_handler(state=StepsForm.get_phone)
async def registration3(message: types.Message, state: FSMContext):

    # получаем объект класса юзер. Чисто для укорачивания кода
    user = userbase[str(message.from_user.id)]

    #удаляем сообщение пользователя
    await message.delete()

    #Добавляем ФИО в базу
    user.phone = message.text

    # добавляем действие
    await user.AddAction(f"Номер: {user.phone}")

    #Регистрируем пользователя на мероприятие
    user.registration_hub.registrations.append(user)
    user.registrations.append(user.registration_hub)

    ikb = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(text="🔗 Общий чат мероприятия", url=user.registration_hub.url_to_tgchat)
    btn2 = InlineKeyboardButton(text="🗂 Главное меню", callback_data=user.city)
    ikb.row(btn1).add(btn2)

    # добавляем картинку и текст
    png = open(user.registration_hub.photo_path, "rb")
    photo = types.InputMediaPhoto(png, caption=f"<i>🕹 Регистрация</i>\n\n"
                                               f"<b>🎟 Событие:</b>\n<code>{user.registration_hub.name}</code>\n\n"
                                               f"<b>🗓 Дата:</b>\n<code>{user.registration_hub.date} {user.registration_hub.time}</code>\n\n"
                                               f"<b>📍 Место:</b>\n<code>{user.registration_hub.location}</code>\n\n"
                                               f"<b>🙎‍♂️ ФИО:</b>\n<code>{user.fio}</code>\n\n"
                                               f"<b>️📱 Номер:</b>\n<code>{user.phone}</code>\n\n"
                                               f"<b>️--------------------------</b>\n"
                                               f"<b>🎉 Ты успешно зарегистрирован!</b> <i>Перешли это сообщение в избранное, "
                                               f"чтобы ничего не забыть</i>\n\n")
    # Редактируем сообщения
    await bot.edit_message_media(chat_id=user.id,
                                 message_id=user.last_message,
                                 media=photo,
                                 reply_markup=ikb)
    await state.finish()

    allregs = ''
    for event in user.registrations:
        allregs+= '📍' + event.name + '\n'

         # Оповещаем админов
    for ad in list(set(dad_admin+[user.registration_hub.creator])):
        await statisticbot.send_message(chat_id=ad,
                                        text=f"<b>Регистрация на мероприятие</b>\n\n"
                                             f"<b>🎟 Мероприятие:</b>\n<code>{user.registration_hub.name}</code>\n\n"
                                             f"<b> 👤 Пользователь:</b>\n@{user.username} (<code>{user.id}</code>)\n\n"
                                             f"<b>Номер:</b> \n{user.phone}\n\n"
                                             f"<b>ФИО:</b> \n{user.fio}\n\n"
                                             f"<b>🗂 Все реги:</b> \n<code>{allregs}</code>")


    user.registration_hub = None



#Добавить мероприятие
@dp.callback_query_handler(text = "add_event")
async def add_event(message: types.CallbackQuery):

    # получаем объект класса юзер. Чисто для укорачивания кода
    user = userbase[str(message.from_user.id)]

    # добавляем действие
    await user.AddAction(f"Добавить мероприятие")

    # добавляем картинку и текст
    png = open(Path(dir_path,"files", "photo", "createevent.png"), "rb")
    photo = types.InputMediaPhoto(png, caption=f"<b>⚠️Введи название мероприятия</b>")

    # Редактируем сообщения
    await bot.edit_message_media(chat_id=user.id,
                                 message_id=user.last_message,
                                 media=photo)

    await AddEvent.get_name.set()

@dp.message_handler(state = AddEvent.get_name)
async def add_event(message: types.Message, state: FSMContext):

    await message.delete()
    # получаем объект класса юзер. Чисто для укорачивания кода
    user = userbase[str(message.from_user.id)]

    # добавляем действие
    await user.AddAction(f"Добавить мероприятие")

    #Складируем инфу во временной памяти
    await state.update_data(name=message.text)
    data = await state.get_data()

    # добавляем картинку и текст
    png = open(Path(dir_path,"files", "photo", "createevent.png"), "rb")
    photo = types.InputMediaPhoto(png, caption=f"<b> Название мероприятия:</b>\n<code>{data['name']}</code>\n\n"
                                               f"<b>⚠️Введи дату</b>\nФормат: дд.мм.гггг\nПример: 16.03.2024")

    # Редактируем сообщения
    await bot.edit_message_media(chat_id=user.id,
                                 message_id=user.last_message,
                                 media=photo)

    await AddEvent.get_date.set()

@dp.message_handler(state=AddEvent.get_date)
async def add_event(message: types.Message, state: FSMContext):

    #удаляем сообщение пользователя
    await message.delete()

    # получаем объект класса юзер. Чисто для укорачивания кода
    user = userbase[str(message.from_user.id)]

    # добавляем действие
    await user.AddAction(f"Добавить мероприятие")

    # Складируем инфу во временной памяти
    await state.update_data(date=message.text)
    data = await state.get_data()

    # добавляем картинку и текст
    png = open(Path(dir_path, "files", "photo", "createevent.png"), "rb")
    photo = types.InputMediaPhoto(png, caption=f"<b>Название мероприятия:</b>\n<code>{data['name']}</code>\n\n"
                                               f"<b>Дата:</b>\n<code>{data['date']}</code>\n\n"
                                               f"<b>⚠️Введи время</b>\nФормат: чч:мм\nПример: 12:00")

    # Редактируем сообщения
    await bot.edit_message_media(chat_id=user.id,
                                 message_id=user.last_message,
                                 media=photo)

    await AddEvent.get_time.set()

@dp.message_handler(state=AddEvent.get_time)
async def add_event(message: types.Message, state: FSMContext):

    #удаляем сообщение пользователя
    await message.delete()

    # получаем объект класса юзер. Чисто для укорачивания кода
    user = userbase[str(message.from_user.id)]

    # добавляем действие
    await user.AddAction(f"Добавить мероприятие")

    # Складируем инфу во временной памяти
    await state.update_data(time=message.text)
    data = await state.get_data()

    # добавляем картинку и текст
    png = open(Path(dir_path, "files", "photo", "createevent.png"), "rb")
    photo = types.InputMediaPhoto(png, caption=f"<b>Название мероприятия:</b>\n<code>{data['name']}</code>\n\n"
                                               f"<b>Дата:</b>\n<code>{data['date']}</code>\n\n"
                                               f"<b>Время:</b>\n<code>{data['time']}</code>\n\n"
                                               f"<b>⚠️Введи место</b>")

    # Редактируем сообщения
    await bot.edit_message_media(chat_id=user.id,
                                 message_id=user.last_message,
                                 media=photo)

    await AddEvent.get_location.set()

@dp.message_handler(state=AddEvent.get_location)
async def add_event(message: types.Message, state: FSMContext):

    #удаляем сообщение пользователя
    await message.delete()

    # получаем объект класса юзер. Чисто для укорачивания кода
    user = userbase[str(message.from_user.id)]

    # добавляем действие
    await user.AddAction(f"Добавить мероприятие")

    # Складируем инфу во временной памяти
    await state.update_data(location=message.text)
    data = await state.get_data()

    # добавляем картинку и текст
    png = open(Path(dir_path, "files", "photo", "createevent.png"), "rb")
    photo = types.InputMediaPhoto(png, caption=f"<b>Название мероприятия:</b>\n<code>{data['name']}</code>\n\n"
                                               f"<b>Дата:</b>\n<code>{data['date']}</code>\n\n"
                                               f"<b>Время:</b>\n<code>{data['time']}</code>\n\n"
                                               f"<b>Место:</b>\n<code>{data['location']}</code>\n\n"
                                               f"<b>⚠️Создайте пригласительную ссылку на общий чат мероприятия и отправьте</b>")

    # Редактируем сообщения
    await bot.edit_message_media(chat_id=user.id,
                                 message_id=user.last_message,
                                 media=photo)

    await AddEvent.get_url.set()

@dp.message_handler(state=AddEvent.get_url)
async def add_event(message: types.Message, state: FSMContext):

    #удаляем сообщение пользователя
    await message.delete()

    # получаем объект класса юзер. Чисто для укорачивания кода
    user = userbase[str(message.from_user.id)]

    # добавляем действие
    await user.AddAction(f"Добавить мероприятие")

    # Складируем инфу во временной памяти
    await state.update_data(url=message.text)
    data = await state.get_data()

    # добавляем картинку и текст
    png = open(Path(dir_path, "files", "photo", "createevent.png"), "rb")
    photo = types.InputMediaPhoto(png, caption=f"<b>Название мероприятия:</b>\n<code>{data['name']}</code>\n\n"
                                               f"<b>Дата:</b>\n<code>{data['date']}</code>\n\n"
                                               f"<b>Время:</b>\n<code>{data['time']}</code>\n\n"
                                               f"<b>Место:</b>\n<code>{data['location']}</code>\n\n"
                                               f"<b>Ссылка:</b>\n{data['url']}\n\n"
                                               f"<b>⚠️Введите описание мероприятия. Максимум 90 знаков</b>")

    # Редактируем сообщения
    await bot.edit_message_media(chat_id=user.id,
                                 message_id=user.last_message,
                                 media=photo)

    await AddEvent.get_description.set()

@dp.message_handler(state=AddEvent.get_description)
async def add_event(message: types.Message, state: FSMContext):

    #удаляем сообщение пользователя
    await message.delete()

    # получаем объект класса юзер. Чисто для укорачивания кода
    user = userbase[str(message.from_user.id)]

    # добавляем действие
    await user.AddAction(f"Добавить мероприятие")

    # Складируем инфу во временной памяти
    await state.update_data(description=message.text)
    data = await state.get_data()

    # добавляем картинку и текст
    png = open(Path(dir_path, "files", "photo", "createevent.png"), "rb")
    photo = types.InputMediaPhoto(png, caption=f"<b>Название мероприятия:</b>\n<code>{data['name']}</code>\n\n"
                                               f"<b>Дата:</b>\n<code>{data['date']}</code>\n\n"
                                               f"<b>Время:</b>\n<code>{data['time']}</code>\n\n"
                                               f"<b>Место:</b>\n<code>{data['location']}</code>\n\n"
                                               f"<b>Ссылка:</b>\n{data['url']}\n\n"
                                               f"<b>Описание:</b>\n<code>{data['description']}</code>\n\n"
                                               f"<b>⚠️Отправьте фото. Обязательно в виде файла. Затем немного подождите</b>")

    # Редактируем сообщения
    await bot.edit_message_media(chat_id=user.id,
                                 message_id=user.last_message,
                                 media=photo)

    await AddEvent.get_photo.set()

@dp.message_handler(state=AddEvent.get_photo, content_types=ContentType.DOCUMENT)
async def add_event(message: types.Message, state: FSMContext):

    #удаляем сообщение пользователя
    await message.delete()

    # получаем объект класса юзер. Чисто для укорачивания кода
    user = userbase[str(message.from_user.id)]

    # добавляем действие
    await user.AddAction(f"Добавить мероприятие")

    #Сохраняем фото
    data = await state.get_data()
    photo_name = (data['date']+data['time']+str(user.id)).replace('.','').replace(':','')
    await message.document.download(destination_file=Path(dir_path,'files','photo','events',f"{photo_name}.png"))

    # Складируем инфу во временной памяти
    await state.update_data(photo_path=Path(dir_path,'files','photo','events',f"{photo_name}.png"))
    data = await state.get_data()

    # добавляем картинку и текст
    png = open(Path(dir_path, "files", "photo", "createevent.png"), "rb")
    photo = types.InputMediaPhoto(png, caption=f"<b>Название мероприятия:</b>\n<code>{data['name']}</code>\n\n"
                                               f"<b>Дата:</b>\n<code>{data['date']}</code>\n\n"
                                               f"<b>Время:</b>\n<code>{data['time']}</code>\n\n"
                                               f"<b>Место:</b>\n<code>{data['location']}</code>\n\n"
                                               f"<b>Ссылка:</b>\n{data['url']}\n\n"
                                               f"<b>Описание:</b>\n<code>{data['description']}</code>\n\n"
                                               f"<b>Фото загружено:</b>\n<code>{data['photo_path']}</code>\n\n"
                                               f"<b>⚠️Подходит ли это мероприятие под бизнес-тематику?</b>\nФормат: True/False")

    # Редактируем сообщения
    await bot.edit_message_media(chat_id=user.id,
                                 message_id=user.last_message,
                                 media=photo)

    await AddEvent.get_vzletbusiness.set()

@dp.message_handler(state=AddEvent.get_vzletbusiness)
async def add_event(message: types.Message, state: FSMContext):

    #удаляем сообщение пользователя
    await message.delete()

    # получаем объект класса юзер. Чисто для укорачивания кода
    user = userbase[str(message.from_user.id)]

    ikb = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(text="Опубликовать", callback_data="publicevent")
    btn2 = InlineKeyboardButton(text="Заполнить заново", callback_data="add_event")
    btn3 = InlineKeyboardButton(text="Главное меню", callback_data=user.city)
    ikb.add(btn1).add(btn2).add(btn3)

    # добавляем действие
    await user.AddAction(f"Добавить мероприятие")

    # Складируем инфу во временной памяти
    await state.update_data(vzletbusiness=message.text)
    data = await state.get_data()

    # добавляем картинку и текст
    png = open(Path(dir_path, "files", "photo", f"{data['photo_path']}"), "rb")
    photo = types.InputMediaPhoto(png, caption=f"<b>Название мероприятия:</b>\n<code>{data['name']}</code>\n\n"
                                               f"<b>Дата:</b>\n<code>{data['date']}</code>\n\n"
                                               f"<b>Время:</b>\n<code>{data['time']}</code>\n\n"
                                               f"<b>Место:</b>\n<code>{data['location']}</code>\n\n"
                                               f"<b>Ссылка:</b>\n{data['url']}\n\n"
                                               f"<b>Описание:</b>\n<code>{data['description']}</code>\n\n"
                                               f"<b>Фото загружено:</b>\n<code>{data['photo_path']}</code>\n\n"
                                               f"<b>Взлёт.Бизнес: </b>\n<code>{data['vzletbusiness']}</code>\n\n")

    # Редактируем сообщения
    await bot.edit_message_media(chat_id=user.id,
                                 message_id=user.last_message,
                                 media=photo,
                                 reply_markup=ikb)

    user.create_hub = Event(name = data['name'],
                            url_to_tgchat = data['url'],
                            photo_path = data['photo_path'],
                            description = data['description'],
                            creator = str(user.id),
                            vzletbusiness = data['vzletbusiness'],
                            date = data['date'],
                            location = data['location'],
                            time = data['time'])

    await state.finish()

@dp.callback_query_handler(text = "publicevent")
async def publicevent(message: types.CallbackQuery):

    # получаем объект класса юзер. Чисто для укорачивания кода
    user = userbase[str(message.from_user.id)]

    # добавляем действие
    await user.AddAction(f"Добавить мероприятие")

    #Оповещаем админов
    for ad in dad_admin:
        await statisticbot.send_message(chat_id=ad,
                                        text = f"@{user.username} добавил мероприятие.\n\n"
                                               f"{user.create_hub.GetInfo()}")

    global eventbase
    #Добавляем в базу эвентов новый эвент и обнуляем креатехаб
    eventbase[str(int(list(eventbase.keys())[-1])+ 1)] = user.create_hub
    user.create_hub = None

    # Сортируем эвенты по датам

    eventbase = await sort_eventbase(eventbase)

    #добавляем клавиатуру
    ikb = InlineKeyboardMarkup()
    btn3 = InlineKeyboardButton(text="🗂Главное меню", callback_data=user.city)
    ikb.add(btn3)

    # добавляем картинку и текст
    png = open(Path(dir_path, "files", "photo", "fio.png"), "rb")
    photo = types.InputMediaPhoto(png, caption=f"<b>Мероприятие добавлено</b>\n\n")

    # Редактируем сообщения
    await bot.edit_message_media(chat_id=user.id,
                                 message_id=user.last_message,
                                 media=photo,
                                 reply_markup=ikb)



#Удалить мероприятие
@dp.callback_query_handler(text = callback_delete_event)
async def delete_event(message: types.CallbackQuery):

    # получаем объект класса юзер. Чисто для укорачивания кода
    user = userbase[str(message.from_user.id)]

    # добавляем действие
    await user.AddAction(f"Добавить мероприятие")

    global eventbase
    # Оповещаем админов
    for ad in dad_admin:
        await statisticbot.send_message(chat_id=ad,
                                        text=f"@{user.username} удалил мероприятие\n\n"
                                             f"<b>Название: </b>{eventbase[message.data[-1]].name}")

    eventbase = await sort_after_delete(eventbase, message.data[-1])

    ikb = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(text = "🗂Главное меню", callback_data=user.city)
    ikb.add(btn1)

    # добавляем картинку и текст
    png = open(Path(dir_path, "files", "photo", "fio.png"), "rb")
    photo = types.InputMediaPhoto(png, caption=f"Мероприятие удалено\n\n")

    # Редактируем сообщения
    await bot.edit_message_media(chat_id=user.id,
                                 message_id=user.last_message,
                                 media=photo,
                                 reply_markup=ikb)













if __name__ == "__main__":
    executor.start_polling(dp,
                           skip_updates=True)




