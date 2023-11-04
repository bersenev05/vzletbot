import datetime
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ContentType
from classes.user import User, dad_admin, cityes, son_admin
from classes.event import Event
from classes.work import Work
from classes.grant import Grant
from classes.learning import Learning
from data.base_file import userbase, eventbase, sort_eventbase, sort_after_delete, learningbase, workbase, grantbase,date,sort_user_regs
import pathlib
from pathlib import Path

dir_path = pathlib.Path.cwd()
from classes import information_body

# МАШИНА СОСТОЯНИЙ
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()


class StepsForm(StatesGroup):
    get_fio = State()
    get_phone = State()
    get_date = State()
class AddEvent(StatesGroup):
    get_name = State()
    get_date = State()
    get_time = State()
    get_location = State()
    get_url = State()
    get_description = State()
    get_photo = State()
class AddCity(StatesGroup):
    get_city = State()


bot = Bot(token="6100104762:AAErbAZGLc6uHLUDhgnKJYfyvlDJMt1x01g",
          parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())

statisticbot = Bot(token="6681358573:AAEDPtrd3jNn82es9LS69eDOicI0ih9FSxk",
                   parse_mode="HTML")


# Старт
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    # удаляем сообщение
    await message.delete()

    # добавляем пользователя в базу данных
    if str(message.from_user.id) not in userbase:

        userbase[str(message.from_user.id)] = User(username=message.from_user.username,
                                                   id=message.from_user.id)
        # оповещаем админов о новых пользователях
        for adm in dad_admin:
            await statisticbot.send_message(chat_id=adm,
                                            text=f"Новый пользователь\n\n"
                                                 f"{await userbase[str(message.from_user.id)].GetInfo()}")

    # получаем объект класса юзер. Чисто для укорачивания кода
    user = userbase[str(message.from_user.id)]

    # добавляем действие
    await user.AddAction("start")

    # создаем клавиатуру
    ikb = InlineKeyboardMarkup()
    for city in cityes:
        ikb.add(InlineKeyboardButton(text=f"📍 {city}", callback_data=city))
    ikb.add(InlineKeyboardButton(text="Хочу добавить свой город!", callback_data="Krasnoyarsk"))

    if str(user.id) in son_admin:
        ikb.add(InlineKeyboardButton(text="Добавить город {admin}", callback_data=f"add_city"))

    # получаем фото
    png = open(Path(dir_path, "files", "photo", "start.png"), "rb")

    # отправляем сообщение
    msg = await bot.send_photo(caption="Привет, я креативный стартап Взлёт! Выбери свой город",
                               reply_markup=ikb,
                               chat_id=user.id,
                               photo=png)
    png.close()

    # сохраняем последнее сообщение
    user.last_message = msg.message_id


callback_user_regs = [f"reg_{i}" for i in range(50)]
#Регистрации пользователя
@dp.message_handler(commands=["registrations"])
async def myregs(message: types.Message):

    await message.delete()

    #Получаем сегодняшнюю дату
    date_list = str(datetime.datetime.now()).split("-")
    now_date = await date(f"{str(date_list[2].split()[0])}.{str(date_list[1])}.{str(date_list[0])}")

    # получаем объект класса юзер. Чисто для укорачивания кода
    user = userbase[str(message.from_user.id)]

    # добавляем действие
    await user.AddAction(f"Выбрал")

    if user.city!=None:
        if user.registrations == []:

            # добавляем клавиатуру
            ikb = InlineKeyboardMarkup()
            btn3 = InlineKeyboardButton(text="🗂Главное меню", callback_data=user.city)
            ikb.add(btn3)

            # Получаем фото
            png = open(Path(dir_path, "files", "photo", "mainmenu.png"), "rb")
            photo = types.InputMediaPhoto(png,
                                          caption="Ты ещё никуда не зарегистрировался!")

            # Редактируем сообщения
            await bot.edit_message_media(chat_id=user.id,
                                         message_id=user.last_message,
                                         media=photo,
                                         reply_markup=ikb)

            png.close()

        else:

            #сортируем регистрации пользователя, чтобы всё было по датам
            user.registrations = await sort_user_regs(user.registrations)

            # добавляем клавиатуру
            ikb = InlineKeyboardMarkup()
            s=0
            for i in user.registrations:

                if await date(i.date) >= now_date:

                    forwrite = i.name
                    if len(i.name)>=15:
                        forwrite = f"{i.name[:15]}..."

                    ikb.add(InlineKeyboardButton(text = forwrite + f" ({i.date})", callback_data=f"reg_{s}"))
                s+=1

            ikb.add(InlineKeyboardButton(text="🗂Главное меню", callback_data=user.city))

            # Получаем фото
            png = open(Path(dir_path, "files", "photo", "mainmenu.png"), "rb")
            photo = types.InputMediaPhoto(png,
                                          caption="Нажми на мероприятие и увидишь всю важную инфу!")

            # Редактируем сообщения
            await bot.edit_message_media(chat_id=user.id,
                                         message_id=user.last_message,
                                         media=photo,
                                         reply_markup=ikb)

            png.close()

#Регистрации пользователя колбэком
@dp.callback_query_handler(text = "registrations")
async def myregs(message: types.Message):

    # Получаем сегодняшнюю дату
    date_list = str(datetime.datetime.now()).split("-")
    now_date = await date(f"{str(date_list[2].split()[0])}.{str(date_list[1])}.{str(date_list[0])}")

    # получаем объект класса юзер. Чисто для укорачивания кода
    user = userbase[str(message.from_user.id)]

    # добавляем действие
    await user.AddAction(f"Выбрал")

    if user.city != None:
        if user.registrations == []:

            # добавляем клавиатуру
            ikb = InlineKeyboardMarkup()
            btn3 = InlineKeyboardButton(text="🗂Главное меню", callback_data=user.city)
            ikb.add(btn3)

            # Получаем фото
            png = open(Path(dir_path, "files", "photo", "mainmenu.png"), "rb")
            photo = types.InputMediaPhoto(png,
                                          caption="Ты ещё никуда не зарегистрировался!")

            # Редактируем сообщения
            await bot.edit_message_media(chat_id=user.id,
                                         message_id=user.last_message,
                                         media=photo,
                                         reply_markup=ikb)

            png.close()

        else:

            # сортируем регистрации пользователя, чтобы всё было по датам
            user.registrations = await sort_user_regs(user.registrations)

            # добавляем клавиатуру
            ikb = InlineKeyboardMarkup()
            s = 0
            for i in user.registrations:

                if await date(i.date) >= now_date:

                    forwrite = i.name
                    if len(i.name) >= 15:
                        forwrite = f"{i.name[:15]}..."

                    ikb.add(InlineKeyboardButton(text=forwrite + f" ({i.date})", callback_data=f"reg_{s}"))
                s += 1

            ikb.add(InlineKeyboardButton(text="🗂Главное меню", callback_data=user.city))

            # Получаем фото
            png = open(Path(dir_path, "files", "photo", "mainmenu.png"), "rb")
            photo = types.InputMediaPhoto(png,
                                          caption="Нажми на мероприятие и увидишь всю важную инфу!")

            # Редактируем сообщения
            await bot.edit_message_media(chat_id=user.id,
                                         message_id=user.last_message,
                                         media=photo,
                                         reply_markup=ikb)

            png.close()

#Вывод мероприятия, на которое зарегистрирован пользователь
@dp.callback_query_handler(text = callback_user_regs)
async def user_regs_info(message: types.CallbackQuery):

    # получаем объект класса юзер. Чисто для укорачивания кода
    user = userbase[str(message.from_user.id)]

    # добавляем действие
    await user.AddAction(f"Выбрал")

    #находим мероприятие которое нужно выдать
    event = user.registrations[int(message.data.split("_")[1])]

    # клавиатура
    ikb = InlineKeyboardMarkup()
    ikb.add(InlineKeyboardButton(text="🔗 Общий чат мероприятия", url=event.url_to_tgchat))
    ikb.add(InlineKeyboardButton(text="Назад", callback_data="registrations"))
    ikb.add(InlineKeyboardButton(text="🗂Главное меню", callback_data=user.city))



    # Получаем фото
    png = open(event.photo_path, "rb")
    photo = types.InputMediaPhoto(png, caption=f"<b>🎟 Событие:</b>\n<code>{event.name}</code>\n\n"
                                               f"<b>🗓 Дата:</b>\n<code>{event.date} {event.time}</code>\n\n"
                                               f"<b>📍 Место:</b>\n<code>{event.location}</code>\n\n")

    # Редактируем сообщения
    await bot.edit_message_media(chat_id=user.id,
                                 message_id=user.last_message,
                                 media=photo,
                                 reply_markup=ikb)

    png.close()



# Главное меню
@dp.callback_query_handler(text=cityes)
async def city(message: types.CallbackQuery):
    # получаем объект класса юзер. Чисто для укорачивания кода
    user = userbase[str(message.from_user.id)]

    # Обнуляем карусель
    user.location = None

    # Добавляем юзеру город
    user.city = message.data

    # добавляем действие
    await user.AddAction(f"Выбрал {message.data}")

    # клавиатура
    ikb = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(text="Мероприятия", callback_data="eventsnext")
    btn2 = InlineKeyboardButton(text="Обучение", callback_data="learningnext")
    btn3 = InlineKeyboardButton(text="Стажировки", callback_data="worknext")
    btn4 = InlineKeyboardButton(text="Взлёт.Бизнес", callback_data="business")
    btn5 = InlineKeyboardButton(text="Гранты", callback_data="grantnext")

    ikb.add(btn1).add(btn2).add(btn3).add(btn5).add(btn4)

    # Получаем фото
    png = open(Path(dir_path, "files", "photo", "mainmenu.png"), "rb")
    photo = types.InputMediaPhoto(png,
                                  caption="Здесь ты можешь найти мощное мероприятие, обучение или стажировку и мгновенно зарегистрироваться!")

    # Редактируем сообщения
    await bot.edit_message_media(chat_id=user.id,
                                 message_id=user.last_message,
                                 media=photo,
                                 reply_markup=ikb)

    png.close()



#переход во взлет бизнес
@dp.callback_query_handler(text="business")
async def business_func(message: types.CallbackQuery):
    # получаем объект класса юзер. Чисто для укорачивания кода
    user = userbase[str(message.from_user.id)]

    # добавляем действие
    await user.AddAction(f"Выбрал {message.data}")

    # клавиатура
    ikb = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(text="🗂 Главное меню", callback_data=user.city)
    ikb.add(btn1)

    # Получаем фото
    png = open(Path(dir_path, "files", "photo", "razrabotka.png"), "rb")
    photo = types.InputMediaPhoto(png,
                                  caption="Здесь ты сможешь опубликовать свой стартап, найти подходящий грант и даже интересных партнёров.\n\nТе, кто интересуются IT, смогут найти для себя тут бесплатное обучение современным технологиям.\n\nПомимо этого, мы собираемся реализовать мощный стартап-акселератор, где каждый сможет понять основы создания интересных проектов и здесь же создать и опубликовать свой проект\n\n"
                                          "<code>{ Этот раздел ещё в разработке }</code>")

    # Редактируем сообщения
    await bot.edit_message_media(chat_id=user.id,
                                 message_id=user.last_message,
                                 media=photo,
                                 reply_markup=ikb)

    png.close()



#Добавить город
@dp.callback_query_handler(text="add_city")
async def addcity_func(message: types.CallbackQuery):
    # получаем объект класса юзер. Чисто для укорачивания кода
    user = userbase[str(message.from_user.id)]

    # добавляем действие
    await user.AddAction(f"Выбрал")

    # Получаем фото
    png = open(Path(dir_path, "files", "photo", "mainmenu.png"), "rb")
    photo = types.InputMediaPhoto(png,
                                  caption="Введи название города")

    # Редактируем сообщения
    await bot.edit_message_media(chat_id=user.id,
                                 message_id=user.last_message,
                                 media=photo)

    png.close()

    await AddCity.get_city.set()

@dp.message_handler(state=AddCity.get_city)
async def getcityname(message: types.Message, state: FSMContext):
    await message.delete()

    # получаем объект класса юзер. Чисто для укорачивания кода
    user = userbase[str(message.from_user.id)]

    # Добавляем юзеру город
    user.city = message.text

    # добавляем действие
    await user.AddAction(f"Выбрал")

    cityes.append(message.text)
    city = message.text

    for i in [learningbase, workbase, eventbase, grantbase]:
        i[city] = {}

        i[city]["0"] = Event(name="В этом разделе пока ничего нет, но скоро будет!",
                             url_to_tgchat="https://t.me/+9PY3bcf3ZH01MDZi",
                             photo_path=Path(dir_path, "files", "photo", "razrabotka.png"),
                             description="",
                             date="16.03.2030",
                             time="12:00",
                             creator="5965231899",
                             location="Культурная станция Гагарин. Маерчака 17",
                             city=user.city)

    ikb = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(text="Главное меню", callback_data=user.city)
    ikb.add(btn1)

    # Получаем фото
    png = open(Path(dir_path, "files", "photo", "mainmenu.png"), "rb")
    photo = types.InputMediaPhoto(png, caption="Город добавлен")

    # Редактируем сообщения
    await bot.edit_message_media(chat_id=user.id,
                                 message_id=user.last_message,
                                 media=photo,
                                 reply_markup=ikb)

    cityes.sort(key=lambda x: x[0])

    await state.finish()



callback_event_setpriority = [f"event_setpriority_{index}" for index in range(0, 50)]
callback_event_location = [f"event_registration_{index}" for index in range(0, 50)]
callback_delete_event = [f"delete_event_{index}" for index in range(0, 50)]
callback_info_event = [f"info_event_{index}" for index in range(0, 50)]
# Движение по карусели эвентам
@dp.callback_query_handler(text=["eventsnext", "eventsback"])
async def events1(message: types.CallbackQuery):
    # получаем объект класса юзер. Чисто для укорачивания кода
    user = userbase[str(message.from_user.id)]

    # добавляем действие
    await user.AddAction(f"листнул на эвент")

    # Движение по карусели
    if user.location == None:
        user.location = "0"

    elif message.data == "eventsnext":
        if int(user.location) < len(eventbase[user.city]) - 1:
            user.location = str(int(user.location) + 1)
        else:
            user.location = "0"
    else:
        if int(user.location) > 0:
            user.location = str(int(user.location) - 1)
        else:
            user.location = str(len(eventbase[user.city]) - 1)

    # получаем из базы событие
    event = eventbase[user.city][user.location]

    # клавиатура
    ikb = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(text="Назад", callback_data="eventsback")
    btn2 = InlineKeyboardButton(text="Далее", callback_data="eventsnext")

    if str(user.id) in event.registrations:
        btn3 = InlineKeyboardButton(text="✅ Вы зарегистрированы", url=f"{event.url_to_tgchat}")
    else:
        btn3 = InlineKeyboardButton(text="🕹 Зарегистрироваться", callback_data=f"event_registration_{user.location}")

    btn5 = InlineKeyboardButton(text="🗂 Главное меню", callback_data=user.city)
    ikb.row(btn1, btn2).add(btn3).add(btn5)

    if str(user.id) in son_admin:
        ikb.add(InlineKeyboardButton(text="Добавить мероприятие {admin}", callback_data="add_event"))
        ikb.add(InlineKeyboardButton(text="Удалить мероприятие {admin}", callback_data=f"delete_event_{user.location}"))
        ikb.add(InlineKeyboardButton(text="Сводка {admin}", callback_data=f"info_event_{user.location}"))

        if event.priority == True:
            ikb.add(
                InlineKeyboardButton(text="✅ Приоритет {admin}", callback_data=f"event_setpriority_{user.location}"))
        else:
            ikb.add(InlineKeyboardButton(text="Приоритет {admin}", callback_data=f"event_setpriority_{user.location}"))

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


callback_learning_setpriority = [f"learning_setpriority_{index}" for index in range(0, 50)]
callback_learning_location = [f"learning_registration_{index}" for index in range(0, 50)]
callback_delete_learning = [f"delete_learning_{index}" for index in range(0, 50)]
callback_info_learning = [f"info_learning_{index}" for index in range(0, 50)]
# Движение по карусели обучения
@dp.callback_query_handler(text=["learningnext", "learningback"])
async def events2(message: types.CallbackQuery):
    # получаем объект класса юзер. Чисто для укорачивания кода
    user = userbase[str(message.from_user.id)]

    # подключаем базы для карусели
    base = learningbase[user.city]
    key = "learning"

    # добавляем действие
    await user.AddAction(f"листнул на эвент")

    # Движение по карусели
    if user.location == None:
        user.location = "0"

    elif message.data == f"{key}next":
        if int(user.location) < len(base) - 1:
            user.location = str(int(user.location) + 1)
        else:
            user.location = "0"
    else:
        if int(user.location) > 0:
            user.location = str(int(user.location) - 1)
        else:
            user.location = str(len(base) - 1)

    # получаем из базы событие
    event = base[user.location]

    # клавиатура
    ikb = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(text="Назад", callback_data=f"{key}back")
    btn2 = InlineKeyboardButton(text="Далее", callback_data=f"{key}next")

    if str(user.id) in event.registrations:
        btn3 = InlineKeyboardButton(text="✅ Вы зарегистрированы", url=f"{event.url_to_tgchat}")
    else:
        btn3 = InlineKeyboardButton(text="🕹 Зарегистрироваться", callback_data=f"{key}_registration_{user.location}")

    btn5 = InlineKeyboardButton(text="🗂 Главное меню", callback_data=user.city)
    ikb.row(btn1, btn2).add(btn3).add(btn5)

    if str(user.id) in son_admin:
        ikb.add(InlineKeyboardButton(text="Добавить обучение {admin}", callback_data=f"add_{key}"))
        ikb.add(InlineKeyboardButton(text="Удалить обучение {admin}", callback_data=f"delete_{key}_{user.location}"))
        ikb.add(InlineKeyboardButton(text="Сводка {admin}", callback_data=f"info_{key}_{user.location}"))

        if event.priority == True:
            ikb.add(
                InlineKeyboardButton(text="✅ Приоритет {admin}", callback_data=f"learning_setpriority_{user.location}"))
        else:
            ikb.add(
                InlineKeyboardButton(text="Приоритет {admin}", callback_data=f"learning_setpriority_{user.location}"))

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


callback_work_setpriority = [f"work_setpriority_{index}" for index in range(0, 50)]
callback_work_location = [f"work_registration_{index}" for index in range(0, 50)]
callback_delete_work = [f"delete_work_{index}" for index in range(0, 50)]
callback_info_work = [f"info_work_{index}" for index in range(0, 50)]
# Движение по карусели стажировок
@dp.callback_query_handler(text=["worknext", "workback"])
async def events2(message: types.CallbackQuery):
    # получаем объект класса юзер. Чисто для укорачивания кода
    user = userbase[str(message.from_user.id)]

    # подключаем базы для карусели
    base = workbase[user.city]
    key = "work"

    # добавляем действие
    await user.AddAction(f"листнул на эвент")

    # Движение по карусели
    if user.location == None:
        user.location = "0"

    elif message.data == f"{key}next":
        if int(user.location) < len(base) - 1:
            user.location = str(int(user.location) + 1)
        else:
            user.location = "0"
    else:
        if int(user.location) > 0:
            user.location = str(int(user.location) - 1)
        else:
            user.location = str(len(base) - 1)

    # получаем из базы событие
    event = base[user.location]

    # клавиатура
    ikb = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(text="Назад", callback_data=f"{key}back")
    btn2 = InlineKeyboardButton(text="Далее", callback_data=f"{key}next")

    if str(user.id) in event.registrations:
        btn3 = InlineKeyboardButton(text="✅ Вы зарегистрированы", url=f"{event.url_to_tgchat}")
    else:
        btn3 = InlineKeyboardButton(text="🕹 Зарегистрироваться", callback_data=f"{key}_registration_{user.location}")

    btn5 = InlineKeyboardButton(text="🗂 Главное меню", callback_data=user.city)
    ikb.row(btn1, btn2).add(btn3).add(btn5)

    if str(user.id) in son_admin:
        ikb.add(InlineKeyboardButton(text="Добавить стажировку {admin}", callback_data=f"add_{key}"))
        ikb.add(InlineKeyboardButton(text="Удалить стажировку {admin}", callback_data=f"delete_{key}_{user.location}"))
        ikb.add(InlineKeyboardButton(text="Сводка {admin}", callback_data=f"info_{key}_{user.location}"))

        if event.priority == True:
            ikb.add(InlineKeyboardButton(text="✅ Приоритет {admin}", callback_data=f"work_setpriority_{user.location}"))
        else:
            ikb.add(InlineKeyboardButton(text="Приоритет {admin}", callback_data=f"work_setpriority_{user.location}"))

    png = open(event.photo_path, "rb")
    photo = types.InputMediaPhoto(png, caption=f"<b>{event.name}</b>\n\n"
                                               f"{event.description}\n\n"
                                               f"<b>Дедлайн:</b> {event.date}, {event.time}\n")

    # Редактируем сообщения
    await bot.edit_message_media(chat_id=user.id,
                                 message_id=user.last_message,
                                 media=photo,
                                 reply_markup=ikb)

    png.close()


callback_grant_setpriority = [f"grant_setpriority_{index}" for index in range(0, 50)]
callback_grant_location = [f"grant_registration_{index}" for index in range(0, 50)]
callback_delete_grant = [f"delete_grant_{index}" for index in range(0, 50)]
callback_info_grant = [f"info_grant_{index}" for index in range(0, 50)]
# Движение по карусели грантов
@dp.callback_query_handler(text=["grantnext", "grantback"])
async def events2(message: types.CallbackQuery):
    # получаем объект класса юзер. Чисто для укорачивания кода
    user = userbase[str(message.from_user.id)]

    # подключаем базы для карусели
    base = grantbase[user.city]
    key = "grant"

    # добавляем действие
    await user.AddAction(f"листнул на эвент")

    # Движение по карусели
    if user.location == None:
        user.location = "0"

    elif message.data == f"{key}next":
        if int(user.location) < len(base) - 1:
            user.location = str(int(user.location) + 1)
        else:
            user.location = "0"
    else:
        if int(user.location) > 0:
            user.location = str(int(user.location) - 1)
        else:
            user.location = str(len(base) - 1)

    # получаем из базы событие
    event = base[user.location]

    # клавиатура
    ikb = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(text="Назад", callback_data=f"{key}back")
    btn2 = InlineKeyboardButton(text="Далее", callback_data=f"{key}next")

    if str(user.id) in event.registrations:
        btn3 = InlineKeyboardButton(text="✅ Вы зарегистрированы", url=f"{event.url_to_tgchat}")
    else:
        btn3 = InlineKeyboardButton(text="🕹 Зарегистрироваться", callback_data=f"{key}_registration_{user.location}")

    btn5 = InlineKeyboardButton(text="🗂 Главное меню", callback_data=user.city)
    ikb.row(btn1, btn2).add(btn3).add(btn5)

    if str(user.id) in son_admin:
        ikb.add(InlineKeyboardButton(text="Добавить грант {admin}", callback_data=f"add_{key}"))
        ikb.add(InlineKeyboardButton(text="Удалить грант {admin}", callback_data=f"delete_{key}_{user.location}"))
        ikb.add(InlineKeyboardButton(text="Сводка {admin}", callback_data=f"info_{key}_{user.location}"))

        if event.priority == True:
            ikb.add(
                InlineKeyboardButton(text="✅ Приоритет {admin}", callback_data=f"{key}_setpriority_{user.location}"))
        else:
            ikb.add(InlineKeyboardButton(text="Приоритет {admin}", callback_data=f"{key}_setpriority_{user.location}"))

    png = open(event.photo_path, "rb")
    photo = types.InputMediaPhoto(png, caption=f"<b>{event.name}</b>\n\n"
                                               f"{event.description}\n\n"
                                               f"<b>Дедлайн:</b> {event.date}, {event.time}\n")

    # Редактируем сообщения
    await bot.edit_message_media(chat_id=user.id,
                                 message_id=user.last_message,
                                 media=photo,
                                 reply_markup=ikb)

    png.close()


# Регистрация
@dp.callback_query_handler(
    text=callback_event_location + callback_learning_location + callback_work_location + callback_grant_location)
async def registration1(message: types.CallbackQuery):
    # получаем объект класса юзер. Чисто для укорачивания кода
    user = userbase[str(message.from_user.id)]

    if message.data.split("_")[0] == "event":
        user.registration_hub = eventbase[user.city][message.data[-1]]
    elif message.data.split("_")[0] == "learning":
        user.registration_hub = learningbase[user.city][message.data[-1]]
    elif message.data.split("_")[0] == "work":
        user.registration_hub = workbase[user.city][message.data[-1]]
    elif message.data.split("_")[0] == "grant":
        user.registration_hub = grantbase[user.city][message.data[-1]]

    if user.fio != None and user.phone != None:

        ikb = InlineKeyboardMarkup()
        btn1 = InlineKeyboardButton(text="Да", callback_data="registration_finish")
        btn2 = InlineKeyboardButton(text="Изменить", callback_data="registration_start")
        ikb.add(btn1).add(btn2)

        png = open(user.registration_hub.photo_path, "rb")
        photo = types.InputMediaPhoto(png, caption=f"<i>🕹 Регистрация</i>\n\n"
                                                   f"<b>🎟 Событие:</b>\n<code>{user.registration_hub.name}</code>\n\n"
                                                   f"<b>🗓 Дата:</b>\n<code>{user.registration_hub.date} {user.registration_hub.time}</code>\n\n"
                                                   f"<b>📍 Место:</b>\n<code>{user.registration_hub.location}</code>\n\n"
                                                   f"<b>ФИО</b>:\n<code>{user.fio}</code>\n\n"
                                                   f"<b>Номер</b>:\n<code>{user.phone}</code>\n\n"
                                                   f"<b>⚠️Проверь правильность ФИО и номера телефона. Всё верно?</b>")

        # Редактируем сообщения
        await bot.edit_message_media(chat_id=user.id,
                                     message_id=user.last_message,
                                     media=photo,
                                     reply_markup=ikb)

    else:

        # добавляем картинку и текст
        png = open(user.registration_hub.photo_path, "rb")
        photo = types.InputMediaPhoto(png, caption=f"<i>🕹 Регистрация</i>\n\n"
                                                   f"<b>🎟 Событие:</b>\n<code>{user.registration_hub.name}</code>\n\n"
                                                   f"<b>🗓 Дата:</b>\n<code>{user.registration_hub.date} {user.registration_hub.time}</code>\n\n"
                                                   f"<b>📍 Место:</b>\n<code>{user.registration_hub.location}</code>\n\n"
                                                   f"<b>⚠️ Чтобы зарегистрироваться, введи ФИО</b>")

        # Редактируем сообщения
        await bot.edit_message_media(chat_id=user.id,
                                     message_id=user.last_message,
                                     media=photo)

        await StepsForm.get_fio.set()

@dp.callback_query_handler(text="registration_start")
async def registration_start(message: types.CallbackQuery):
    # получаем объект класса юзер. Чисто для укорачивания кода
    user = userbase[str(message.from_user.id)]

    # добавляем картинку и текст
    png = open(user.registration_hub.photo_path, "rb")
    photo = types.InputMediaPhoto(png, caption=f"<i>🕹 Регистрация</i>\n\n"
                                               f"<b>🎟 Событие:</b>\n<code>{user.registration_hub.name}</code>\n\n"
                                               f"<b>🗓 Дата:</b>\n<code>{user.registration_hub.date} {user.registration_hub.time}</code>\n\n"
                                               f"<b>📍 Место:</b>\n<code>{user.registration_hub.location}</code>\n\n"
                                               f"<b>⚠️ Чтобы зарегистрироваться, введи ФИО</b>")

    # Редактируем сообщения
    await bot.edit_message_media(chat_id=user.id,
                                 message_id=user.last_message,
                                 media=photo)

    await StepsForm.get_fio.set()

@dp.message_handler(state=StepsForm.get_fio)
async def registration2(message: types.Message, state: FSMContext):
    # получаем объект класса юзер. Чисто для укорачивания кода
    user = userbase[str(message.from_user.id)]

    # удаляем сообщение пользователя
    await message.delete()

    # Добавляем ФИО в базу
    if message.text not in ["/start", "/profile"]:
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

    else:

        # добавляем действие
        await user.AddAction(f"Неверный ввод: {message.text}")

        # добавляем картинку и текст
        png = open(user.registration_hub.photo_path, "rb")
        photo = types.InputMediaPhoto(png, caption=f"<i>🕹 Регистрация</i>\n\n"
                                                   f"<b>🎟 Событие:</b>\n<code>{user.registration_hub.name}</code>\n\n"
                                                   f"<b>🗓 Дата:</b>\n<code>{user.registration_hub.date} {user.registration_hub.time}</code>\n\n"
                                                   f"<b>📍 Место:</b>\n<code>{user.registration_hub.location}</code>\n\n"
                                                   f"<b>⚠️ Чтобы зарегистрироваться, введи ФИО</b>\n"
                                                   f"<code>Ошибка: Неверный формат ввода. Попробуй ещё раз</code>")

        # Редактируем сообщения
        await bot.edit_message_media(chat_id=user.id,
                                     message_id=user.last_message,
                                     media=photo)

        await StepsForm.get_fio.set()

@dp.message_handler(state=StepsForm.get_phone)
async def registration3(message: types.Message, state: FSMContext):
    # получаем объект класса юзер. Чисто для укорачивания кода
    user = userbase[str(message.from_user.id)]

    # удаляем сообщение пользователя
    await message.delete()

    if message.text not in ["/start", "/profile"]:

        # Добавляем ФИО в базу
        user.phone = message.text

        # добавляем действие
        await user.AddAction(f"Номер: {user.phone}")

        # Регистрируем пользователя на мероприятие
        user.registration_hub.registrations.append(str(user.id))
        user.registrations.append(user.registration_hub)

        ikb = InlineKeyboardMarkup()
        btn1 = InlineKeyboardButton(text="🔗 Общий чат мероприятия", url=user.registration_hub.url_to_tgchat)
        btn2 = InlineKeyboardButton(text="🗂 Главное меню", callback_data=user.city)
        ikb.row(btn1).add(btn2)

        # добавляем картинку и текст
        png = open(user.registration_hub.photo_path, "rb")
        photo = types.InputMediaPhoto(png, caption=f"<i>🕹 Регистрация</i>\n\n"
                                                   f"<b>🎟 Событие:</b>\n<code>{user.registration_hub.name}</code>\n\n"
                                                   f"<b>🗓 Дата и время:</b>\n<code>{user.registration_hub.date} {user.registration_hub.time}</code>\n\n"
                                                   f"<b>📍 Место:</b>\n<code>{user.registration_hub.location}</code>\n\n"
                                                   f"<b>🙎‍♂️ ФИО:</b>\n<code>{user.fio}</code>\n\n"
                                                   f"<b>️📱 Номер:</b>\n<code>{user.phone}</code>\n\n"
                                                   f"<b>️--------------------------</b>\n"
                                                   f"<b>🎉 Ты успешно зарегистрирован!</b>\n\n<i>Все твои регистрации:</i>\n/registrations\n\n")
        # Редактируем сообщения
        await bot.edit_message_media(chat_id=user.id,
                                     message_id=user.last_message,
                                     media=photo,
                                     reply_markup=ikb)
        await state.finish()

        allregs = ''
        for event in user.registrations:
            allregs += '📍' + event.name + '\n'

        regfile = await user.registration_hub.GetInfoFile()

        # Оповещаем админов
        for ad in list(set(dad_admin + [user.registration_hub.creator])):
            await statisticbot.send_document(chat_id=ad,
                                             document=open(regfile, "rb"),
                                             caption=f"<b>Регистрация</b>\n\n"
                                                     f"<b>🎟 {user.registration_hub.type}:</b>\n<code>{user.registration_hub.name}</code>\n\n"
                                                     f"<b> 👤 Пользователь:</b>\n@{user.username} (<code>{user.id}</code>)\n\n"
                                                     f"<b>Номер:</b> \n{user.phone}\n\n"
                                                     f"<b>ФИО:</b> \n{user.fio}\n\n"
                                                     f"<b>🗂 Все реги:</b> \n<code>{allregs}</code>")

        user.registration_hub = None

    else:

        # добавляем картинку и текст
        png = open(user.registration_hub.photo_path, "rb")
        photo = types.InputMediaPhoto(png, caption=f"<i>🕹 Регистрация</i>\n\n"
                                                   f"<b>🎟 Событие:</b>\n<code>{user.registration_hub.name}</code>\n\n"
                                                   f"<b>🗓 Дата:</b>\n<code>{user.registration_hub.date} {user.registration_hub.time}</code>\n\n"
                                                   f"<b>📍 Место:</b>\n<code>{user.registration_hub.location}</code>\n\n"
                                                   f"<b>🙎‍♂️ ФИО:</b>\n<code>{user.fio}</code>\n\n"
                                                   f"<b>⚠️Введи номер телефона</b>\n"
                                                   f"<code>Ошибка: Неверный формат ввода. Попробуй ещё раз</code>")
        # Редактируем сообщения
        await bot.edit_message_media(chat_id=user.id,
                                     message_id=user.last_message,
                                     media=photo)
        await StepsForm.get_phone.set()

@dp.callback_query_handler(text="registration_finish")
async def registration_finish(message: types.CallbackQuery):
    # получаем объект класса юзер. Чисто для укорачивания кода
    user = userbase[str(message.from_user.id)]

    # добавляем действие
    await user.AddAction(f"Номер: {user.phone}")

    # Регистрируем пользователя на мероприятие
    user.registration_hub.registrations.append(str(user.id))
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
                                               f"<b>🎉 Ты успешно зарегистрирован!</b>\n\n<i>Все твои регистрации:</i>\n/registrations\n\n")
    # Редактируем сообщения
    await bot.edit_message_media(chat_id=user.id,
                                 message_id=user.last_message,
                                 media=photo,
                                 reply_markup=ikb)

    allregs = ''
    for event in user.registrations:
        allregs += '📍' + event.name + '\n'

    regfile = await user.registration_hub.GetInfoFile()

    # Оповещаем админов
    for ad in list(set(dad_admin + [user.registration_hub.creator])):
        await statisticbot.send_document(chat_id=ad,
                                         document=open(regfile, "rb"),
                                         caption=f"<b>Регистрация</b>\n\n"
                                                 f"<b>🎟 {user.registration_hub.type}:</b>\n<code>{user.registration_hub.name}</code>\n\n"
                                                 f"<b> 👤 Пользователь:</b>\n@{user.username} (<code>{user.id}</code>)\n\n"
                                                 f"<b>Номер:</b> \n{user.phone}\n\n"
                                                 f"<b>ФИО:</b> \n{user.fio}\n\n"
                                                 f"<b>🗂 Все реги:</b> \n<code>{allregs}</code>")

    user.registration_hub = None




# Добавить мероприятие
@dp.callback_query_handler(text=["add_event", "add_learning", "add_work", "add_grant"])
async def add_event(message: types.CallbackQuery):
    # получаем объект класса юзер. Чисто для укорачивания кода
    user = userbase[str(message.from_user.id)]

    if message.data.split("_")[-1] == "event":
        user.create_hub = "event"
    elif message.data.split("_")[-1] == "learning":
        user.create_hub = "learning"
    elif message.data.split("_")[-1] == "work":
        user.create_hub = "work"
    elif message.data.split("_")[-1] == "grant":
        user.create_hub = "grant"

    # добавляем действие
    await user.AddAction(f"Добавить мероприятие")

    # добавляем картинку и текст
    png = open(Path(dir_path, "files", "photo", "createevent.png"), "rb")
    photo = types.InputMediaPhoto(png, caption=f"<b>⚠️Введи название</b>")

    # Редактируем сообщения
    await bot.edit_message_media(chat_id=user.id,
                                 message_id=user.last_message,
                                 media=photo)

    await AddEvent.get_name.set()

@dp.message_handler(state=AddEvent.get_name)
async def add_event(message: types.Message, state: FSMContext):
    await message.delete()
    # получаем объект класса юзер. Чисто для укорачивания кода
    user = userbase[str(message.from_user.id)]

    # добавляем действие
    await user.AddAction(f"Добавить мероприятие")

    # Складируем инфу во временной памяти
    await state.update_data(name=message.text)
    data = await state.get_data()

    # добавляем картинку и текст
    png = open(Path(dir_path, "files", "photo", "createevent.png"), "rb")
    photo = types.InputMediaPhoto(png, caption=f"<b> Название:</b>\n<code>{data['name']}</code>\n\n"
                                               f"<b>⚠️Введи дату</b>\nФормат: дд.мм.гггг\nПример: 16.03.2024")

    # Редактируем сообщения
    await bot.edit_message_media(chat_id=user.id,
                                 message_id=user.last_message,
                                 media=photo)

    await AddEvent.get_date.set()

@dp.message_handler(state=AddEvent.get_date)
async def add_event(message: types.Message, state: FSMContext):
    # удаляем сообщение пользователя
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
    photo = types.InputMediaPhoto(png, caption=f"<b>Название:</b>\n<code>{data['name']}</code>\n\n"
                                               f"<b>Дата:</b>\n<code>{data['date']}</code>\n\n"
                                               f"<b>⚠️Введи время</b>\nФормат: чч:мм\nПример: 12:00")

    # Редактируем сообщения
    await bot.edit_message_media(chat_id=user.id,
                                 message_id=user.last_message,
                                 media=photo)

    await AddEvent.get_time.set()

@dp.message_handler(state=AddEvent.get_time)
async def add_event(message: types.Message, state: FSMContext):
    # удаляем сообщение пользователя
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
    photo = types.InputMediaPhoto(png, caption=f"<b>Название:</b>\n<code>{data['name']}</code>\n\n"
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
    # удаляем сообщение пользователя
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
    photo = types.InputMediaPhoto(png, caption=f"<b>Название:</b>\n<code>{data['name']}</code>\n\n"
                                               f"<b>Дата:</b>\n<code>{data['date']}</code>\n\n"
                                               f"<b>Время:</b>\n<code>{data['time']}</code>\n\n"
                                               f"<b>Место:</b>\n<code>{data['location']}</code>\n\n"
                                               f"<b>⚠️Создайте пригласительную ссылку на общий чат и отправьте</b>")

    # Редактируем сообщения
    await bot.edit_message_media(chat_id=user.id,
                                 message_id=user.last_message,
                                 media=photo)

    await AddEvent.get_url.set()

@dp.message_handler(state=AddEvent.get_url)
async def add_event(message: types.Message, state: FSMContext):
    # удаляем сообщение пользователя
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
    photo = types.InputMediaPhoto(png, caption=f"<b>Название:</b>\n<code>{data['name']}</code>\n\n"
                                               f"<b>Дата:</b>\n<code>{data['date']}</code>\n\n"
                                               f"<b>Время:</b>\n<code>{data['time']}</code>\n\n"
                                               f"<b>Место:</b>\n<code>{data['location']}</code>\n\n"
                                               f"<b>Ссылка:</b>\n{data['url']}\n\n"
                                               f"<b>⚠️Введите описание. Максимум 90 знаков</b>")

    # Редактируем сообщения
    await bot.edit_message_media(chat_id=user.id,
                                 message_id=user.last_message,
                                 media=photo)

    await AddEvent.get_description.set()

@dp.message_handler(state=AddEvent.get_description)
async def add_event(message: types.Message, state: FSMContext):
    # удаляем сообщение пользователя
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
    photo = types.InputMediaPhoto(png, caption=f"<b>Название:</b>\n<code>{data['name']}</code>\n\n"
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
    # удаляем сообщение пользователя
    await message.delete()

    # получаем объект класса юзер. Чисто для укорачивания кода
    user = userbase[str(message.from_user.id)]

    # добавляем действие
    await user.AddAction(f"Добавить мероприятие")

    # Сохраняем фото
    data = await state.get_data()
    photo_name = (data['date'] + data['time'] + str(user.id)).replace('.', '').replace(':', '')
    await message.document.download(destination_file=Path(dir_path, 'files', 'photo', 'events', f"{photo_name}.png"))

    # Складируем инфу во временной памяти
    await state.update_data(photo_path=Path(dir_path, 'files', 'photo', 'events', f"{photo_name}.png"))
    data = await state.get_data()

    ikb = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(text="Опубликовать", callback_data="publicevent")
    btn2 = InlineKeyboardButton(text="Заполнить заново", callback_data="add_event")
    btn3 = InlineKeyboardButton(text="Главное меню", callback_data=user.city)
    ikb.add(btn1).add(btn2).add(btn3)

    # добавляем картинку и текст
    png = open(Path(dir_path, "files", "photo", f"{data['photo_path']}"), "rb")
    photo = types.InputMediaPhoto(png, caption=f"<b>Название:</b>\n<code>{data['name']}</code>\n\n"
                                               f"<b>Дата:</b>\n<code>{data['date']}</code>\n\n"
                                               f"<b>Время:</b>\n<code>{data['time']}</code>\n\n"
                                               f"<b>Место:</b>\n<code>{data['location']}</code>\n\n"
                                               f"<b>Ссылка:</b>\n{data['url']}\n\n"
                                               f"<b>Описание:</b>\n<code>{data['description']}</code>\n\n"
                                               f"<b>Фото загружено:</b>\n<code>{data['photo_path']}</code>\n\n")

    # Редактируем сообщения
    await bot.edit_message_media(chat_id=user.id,
                                 message_id=user.last_message,
                                 media=photo,
                                 reply_markup=ikb)

    if user.create_hub == "event":
        user.create_hub = Event(name=data['name'],
                                url_to_tgchat=data['url'],
                                photo_path=data['photo_path'],
                                description=data['description'],
                                creator=str(user.id),
                                date=data['date'],
                                location=data['location'],
                                time=data['time'],
                                city=user.city)

    elif user.create_hub == "learning":
        user.create_hub = Learning(name=data['name'],
                                   url_to_tgchat=data['url'],
                                   photo_path=data['photo_path'],
                                   description=data['description'],
                                   creator=str(user.id),
                                   date=data['date'],
                                   location=data['location'],
                                   time=data['time'],
                                   city=user.city)

    elif user.create_hub == "work":
        user.create_hub = Work(name=data['name'],
                               url_to_tgchat=data['url'],
                               photo_path=data['photo_path'],
                               description=data['description'],
                               creator=str(user.id),
                               date=data['date'],
                               location=data['location'],
                               time=data['time'],
                               city=user.city)

    elif user.create_hub == "grant":
        user.create_hub = Grant(name=data['name'],
                                url_to_tgchat=data['url'],
                                photo_path=data['photo_path'],
                                description=data['description'],
                                creator=str(user.id),
                                date=data['date'],
                                location=data['location'],
                                time=data['time'],
                                city=user.city)

    await state.finish()

@dp.callback_query_handler(text="publicevent")
async def publicevent(message: types.CallbackQuery):
    # получаем объект класса юзер. Чисто для укорачивания кода
    user = userbase[str(message.from_user.id)]

    # добавляем действие
    await user.AddAction(f"Добавить мероприятие")

    # Оповещаем админов
    for ad in dad_admin:
        await statisticbot.send_message(chat_id=ad,
                                        text=f"@{user.username} добавил мероприятие.\n\n"
                                             f"{await user.create_hub.GetInfo()}")

    global eventbase
    global learningbase
    global workbase
    global grantbase

    if user.create_hub.type == "Мероприятие":
        # Добавляем в базу эвентов новый эвент и обнуляем креатехаб
        eventbase[user.city][str(int(list(eventbase[user.city].keys())[-1]) + 1)] = user.create_hub
        user.create_hub = None

        # Сортируем эвенты по датам
        eventbase[user.city] = await sort_eventbase(eventbase[user.city])

    elif user.create_hub.type == "Обучение":

        # Добавляем в базу эвентов новый эвент и обнуляем креатехаб
        learningbase[user.city][str(int(list(learningbase[user.city].keys())[-1]) + 1)] = user.create_hub
        user.create_hub = None
        # Сортируем эвенты по датам
        learningbase[user.city] = await sort_eventbase(learningbase[user.city])

    elif user.create_hub.type == "Стажировка":
        # Добавляем в базу эвентов новый эвент и обнуляем креатехаб
        workbase[user.city][str(int(list(workbase[user.city].keys())[-1]) + 1)] = user.create_hub
        user.create_hub = None
        # Сортируем эвенты по датам
        workbase[user.city] = await sort_eventbase(workbase[user.city])

    elif user.create_hub.type == "Грант":
        # Добавляем в базу эвентов новый эвент и обнуляем креатехаб
        grantbase[user.city][str(int(list(grantbase[user.city].keys())[-1]) + 1)] = user.create_hub
        user.create_hub = None
        # Сортируем эвенты по датам
        grantbase[user.city] = await sort_eventbase(grantbase[user.city])

    # добавляем клавиатуру
    ikb = InlineKeyboardMarkup()
    btn3 = InlineKeyboardButton(text="🗂Главное меню", callback_data=user.city)
    ikb.add(btn3)

    # добавляем картинку и текст
    png = open(Path(dir_path, "files", "photo", "fio.png"), "rb")
    photo = types.InputMediaPhoto(png, caption=f"<b>Успешно добавлено в базу</b>\n\n")

    # Редактируем сообщения
    await bot.edit_message_media(chat_id=user.id,
                                 message_id=user.last_message,
                                 media=photo,
                                 reply_markup=ikb)



# Удалить мероприятие
@dp.callback_query_handler(text=callback_delete_event)
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
                                             f"<b>Название: </b>{eventbase[user.city][message.data[-1]].name}")

    eventbase[user.city] = await sort_after_delete(eventbase[user.city], message.data[-1])

    ikb = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(text="🗂Главное меню", callback_data=user.city)
    ikb.add(btn1)

    # добавляем картинку и текст
    png = open(Path(dir_path, "files", "photo", "fio.png"), "rb")
    photo = types.InputMediaPhoto(png, caption=f"Мероприятие удалено\n\n")

    # Редактируем сообщения
    await bot.edit_message_media(chat_id=user.id,
                                 message_id=user.last_message,
                                 media=photo,
                                 reply_markup=ikb)

# Удалить обучение
@dp.callback_query_handler(text=callback_delete_learning)
async def delete_event(message: types.CallbackQuery):
    # получаем объект класса юзер. Чисто для укорачивания кода
    user = userbase[str(message.from_user.id)]

    # добавляем действие
    await user.AddAction(f"Добавить мероприятие")

    global learningbase
    # Оповещаем админов
    for ad in dad_admin:
        await statisticbot.send_message(chat_id=ad,
                                        text=f"@{user.username} удалил обучение\n\n"
                                             f"<b>Название: </b>{learningbase[user.city][message.data[-1]].name}")

    learningbase[user.city] = await sort_after_delete(learningbase[user.city], message.data[-1])

    ikb = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(text="🗂Главное меню", callback_data=user.city)
    ikb.add(btn1)

    # добавляем картинку и текст
    png = open(Path(dir_path, "files", "photo", "fio.png"), "rb")
    photo = types.InputMediaPhoto(png, caption=f"Обучение удалено\n\n")

    # Редактируем сообщения
    await bot.edit_message_media(chat_id=user.id,
                                 message_id=user.last_message,
                                 media=photo,
                                 reply_markup=ikb)

# Удалить cтажировку
@dp.callback_query_handler(text=callback_delete_work)
async def delete_event(message: types.CallbackQuery):
    # получаем объект класса юзер. Чисто для укорачивания кода
    user = userbase[str(message.from_user.id)]

    # добавляем действие
    await user.AddAction(f"Добавить мероприятие")

    global workbase
    # Оповещаем админов
    for ad in dad_admin:
        await statisticbot.send_message(chat_id=ad,
                                        text=f"@{user.username} удалил обучение\n\n"
                                             f"<b>Название: </b>{workbase[user.city][message.data[-1]].name}")

    workbase[user.city] = await sort_after_delete(workbase[user.city], message.data[-1])

    ikb = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(text="🗂Главное меню", callback_data=user.city)
    ikb.add(btn1)

    # добавляем картинку и текст
    png = open(Path(dir_path, "files", "photo", "fio.png"), "rb")
    photo = types.InputMediaPhoto(png, caption=f"Стажировка удалена\n\n")

    # Редактируем сообщения
    await bot.edit_message_media(chat_id=user.id,
                                 message_id=user.last_message,
                                 media=photo,
                                 reply_markup=ikb)

# Удалить грант
@dp.callback_query_handler(text=callback_delete_grant)
async def delete_event(message: types.CallbackQuery):
    # получаем объект класса юзер. Чисто для укорачивания кода
    user = userbase[str(message.from_user.id)]

    # добавляем действие
    await user.AddAction(f"Добавить мероприятие")

    global grantbase
    # Оповещаем админов
    for ad in dad_admin:
        await statisticbot.send_message(chat_id=ad,
                                        text=f"@{user.username} удалил обучение\n\n"
                                             f"<b>Название: </b>{workbase[user.city][message.data[-1]].name}")

    grantbase[user.city] = await sort_after_delete(grantbase[user.city], message.data[-1])

    ikb = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(text="🗂Главное меню", callback_data=user.city)
    ikb.add(btn1)

    # добавляем картинку и текст
    png = open(Path(dir_path, "files", "photo", "fio.png"), "rb")
    photo = types.InputMediaPhoto(png, caption=f"Грант удален\n\n")

    # Редактируем сообщения
    await bot.edit_message_media(chat_id=user.id,
                                 message_id=user.last_message,
                                 media=photo,
                                 reply_markup=ikb)



# Информация о мероприяти
@dp.callback_query_handler(text=callback_info_event)
async def info_event(message: types.CallbackQuery):

    # получаем объект класса юзер. Чисто для укорачивания кода
    user = userbase[str(message.from_user.id)]

    # добавляем действие
    await user.AddAction(f"Добавить мероприятие")

    regfile = await eventbase[user.city][message.data[-1]].GetInfoFile()

    await statisticbot.send_document(chat_id=user.id,
                                     document=open(regfile, "rb"),
                                     caption=f"<b>сводка по мероприятию {eventbase[user.city][message.data[-1]].name}</b>")

# Информация о обучении
@dp.callback_query_handler(text=callback_info_learning)
async def info_event(message: types.CallbackQuery):
    # получаем объект класса юзер. Чисто для укорачивания кода
    user = userbase[str(message.from_user.id)]

    # добавляем действие
    await user.AddAction(f"Добавить мероприятие")

    regfile = await learningbase[user.city][message.data[-1]].GetInfoFile()

    await statisticbot.send_document(chat_id=user.id,
                                     document=open(regfile, "rb"),
                                     caption=f"<b>сводка по обучению {learningbase[user.city][message.data[-1]].name}</b>")

# Информация о стажировке
@dp.callback_query_handler(text=callback_info_work)
async def info_event(message: types.CallbackQuery):
    # получаем объект класса юзер. Чисто для укорачивания кода
    user = userbase[str(message.from_user.id)]

    # добавляем действие
    await user.AddAction(f"Добавить мероприятие")

    regfile = await workbase[user.city][message.data[-1]].GetInfoFile()

    await statisticbot.send_document(chat_id=user.id,
                                     document=open(regfile, "rb"),
                                     caption=f"<b>сводка по обучению {workbase[user.city][message.data[-1]].name}</b>")

# Информация о гранте
@dp.callback_query_handler(text=callback_info_grant)
async def info_event(message: types.CallbackQuery):
    # получаем объект класса юзер. Чисто для укорачивания кода
    user = userbase[str(message.from_user.id)]

    # добавляем действие
    await user.AddAction(f"Добавить мероприятие")

    regfile = await grantbase[user.city][message.data[-1]].GetInfoFile()

    await statisticbot.send_document(chat_id=user.id,
                                     document=open(regfile, "rb"),
                                     caption=f"<b>сводка по гранту:</b>\n{grantbase[user.city][message.data[-1]].name}")



# Установка приоритета
@dp.callback_query_handler(
    text=callback_learning_setpriority + callback_event_setpriority + callback_work_setpriority + callback_grant_setpriority)
async def setpriority_func(message: types.CallbackQuery):
    global workbase
    global eventbase
    global learningbase

    # получаем объект класса юзер. Чисто для укорачивания кода
    user = userbase[str(message.from_user.id)]

    # добавляем действие
    await user.AddAction(f"Добавить мероприятие")

    data = message.data.split("_")
    msg = ""
    name = ""

    if data[0] == "event":

        if eventbase[user.city][data[2]].priority == True:
            eventbase[user.city][data[2]].priority = None
        else:
            eventbase[user.city][data[2]].priority = True
        msg = "мероприятие"

        name = eventbase[user.city][data[2]].name
        eventbase[user.city] = await sort_eventbase(eventbase[user.city])

    elif data[0] == "learning":
        if learningbase[user.city][data[2]].priority == True:
            learningbase[user.city][data[2]].priority = None
        else:
            learningbase[user.city][data[2]].priority = True
        msg = "обучение"
        name = learningbase[user.city][data[2]].name
        learningbase[user.city] = await sort_eventbase(learningbase[user.city])

    elif data[0] == "work":
        if workbase[user.city][data[2]].priority == True:
            workbase[user.city][data[2]].priority = None
        else:
            workbase[user.city][data[2]].priority = True
        msg = "стажировка"
        name = workbase[user.city][data[2]].name
        workbase[user.city] = await sort_eventbase(workbase[user.city])

    await statisticbot.send_message(chat_id=user.id,
                                    text=f"<b>{msg}: {name}\nИзменен приоритет</b>")

    ikb = InlineKeyboardMarkup()
    ikb.add(InlineKeyboardButton("Главное меню", callback_data=user.city))

    png = open(Path(dir_path, "files", "photo", "fio.png"), "rb")
    photo = types.InputMediaPhoto(png, caption=f"Приоритет изменён. Базы отсортированы")

    # Редактируем сообщения
    await bot.edit_message_media(chat_id=user.id,
                                 message_id=user.last_message,
                                 media=photo,
                                 reply_markup=ikb)

    png.close()


if __name__ == "__main__":
    executor.start_polling(dp,
                           skip_updates=True)
