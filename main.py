
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from classes.user import User, admin, cityes
from classes.event import Event
from data.base_file import userbase, eventbase, sort_eventbase
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


bot = Bot(token = "6100104762:AAFVZRJCVVhtula5Bo6bGlDlpPtjuav7qlI",
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
                       creator="@vanya_slash",
                       location = "Культурная станция Гагарин. Маерчака 17",
                       vzletbusiness=True)

eventbase["1"] = Event(name="Я в деле",
                       url_to_tgchat="https://t.me/+9PY3bcf3ZH01MDZi",
                       photo_path=Path(dir_path, "files", "photo", "yavdele.jpg"),
                       description="Предпринимательский кейс-чемпионат. Создай свой бизнес-проект с помощью наставников",
                       date = "15.03.2024",
                       time = "12:00",
                       creator="@vanya_slash",
                       location = "Культурная станция Гагарин. Маерчака 17",
                       vzletbusiness=True)

eventbase["2"] = Event(name="Битва Креаторов",
                       url_to_tgchat="https://t.me/+9PY3bcf3ZH01MDZi",
                       photo_path=Path(dir_path, "files", "photo", "institut.jpg"),
                       description="приходите пж",
                       date = "11.03.2024",
                       time = "12:00",
                       creator="@vanya_slash",
                       location = "Культурная станция Гагарин. Маерчака 17",
                       vzletbusiness=True)


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
    for adm in admin:
        await statisticbot.send_message(chat_id=adm,
                                        text=f"Новый пользователь\n\n"
                                             f"{await user.GetInfo()}")

    #сохраняем последнее сообщение
    user.last_message = msg.message_id


@dp.callback_query_handler(text = cityes)
async def city(message: types.CallbackQuery):

    # получаем объект класса юзер. Чисто для укорачивания кода
    user = userbase[str(message.from_user.id)]

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


# @dp.callback_query_handler(text = "events")
# async def events(message: types.CallbackQuery):
#
#     # получаем объект класса юзер. Чисто для укорачивания кода
#     user = userbase[str(message.from_user.id)]
#
#     # добавляем действие
#     await user.AddAction(f"Выбрал {message.data}")
#
#     # обнуляем локейшн для дальнейшего движения по карусели
#     user.location = None
#
#     #Сортируем эвенты по датам
#     global eventbase
#     eventbase = await sort_eventbase(eventbase)
#
#     # клавиатура
#     ikb = InlineKeyboardMarkup()
#     btn1 = InlineKeyboardButton(text="Полетели!", callback_data="eventsnext")
#     btn2 = InlineKeyboardButton(text="◀️ Назад", callback_data=user.city)
#     ikb.add(btn1).add(btn2)
#
#     png = open(Path(dir_path, "files", "photo", "events.png"), "rb")
#     photo = types.InputMediaPhoto(png, caption="В этом разделе собраны все ближайшие мероприятия в твоём городе.\n\n "
#                                                "Ты можешь мгновенно зарегистрироваться и получить ссылку на общий чат.\n\n "
#                                                "Участвуй в мероприятиях и получай баллы активности. "
#                                                "Ты можешь менять их на скидки и подарки у наших партнеров")
#
#     # Редактируем сообщения
#     await bot.edit_message_media(chat_id=user.id,
#                                  message_id=user.last_message,
#                                  media=photo,
#                                  reply_markup=ikb)
#
#     png.close()


callback_location = [f"event_registration_{index}" for index in list(eventbase.keys())]
@dp.callback_query_handler(text=["eventsnext","eventsback"])
async def events1(message: types.CallbackQuery):

    # получаем объект класса юзер. Чисто для укорачивания кода
    user = userbase[str(message.from_user.id)]

    # добавляем действие
    await user.AddAction(f"листнул на эвент")

    # Сортируем эвенты по датам
    global eventbase
    eventbase = await sort_eventbase(eventbase)

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


    png = open(event.photo_path, "rb")
    photo = types.InputMediaPhoto(png, caption=f"<b>{event.name}</b>\n\n"
                                               f"{event.description}\n\n"
                                               f"<b>Дата:</b> {event.date} {event.time}")

    # Редактируем сообщения
    await bot.edit_message_media(chat_id=user.id,
                                 message_id=user.last_message,
                                 media=photo,
                                 reply_markup=ikb)

    png.close()


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
                                               f"<b>Введи ФИО</b>")

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

    # добавляем картинку и текст
    png = open(user.registration_hub.photo_path, "rb")
    photo = types.InputMediaPhoto(png, caption=f"<i>🕹 Регистрация</i>\n\n"
                                               f"<b>🎟 Событие:</b>\n<code>{user.registration_hub.name}</code>\n\n"
                                               f"<b>🗓 Дата:</b>\n<code>{user.registration_hub.date} {user.registration_hub.time}</code>\n\n"
                                               f"<b>📍 Место:</b>\n<code>{user.registration_hub.location}</code>\n\n"
                                               f"<b>🙎‍♂️ ФИО:</b>\n<code>{user.fio}</code>\n\n"
                                               f"<b>Введи номер телефона</b>")

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

    user.registration_hub.registrations.append(user)
    user.registration_hub = None

    # Редактируем сообщения
    await bot.edit_message_media(chat_id=user.id,
                                 message_id=user.last_message,
                                 media=photo,
                                 reply_markup=ikb)

    await state.finish()



















if __name__ == "__main__":
    executor.start_polling(dp,
                           skip_updates=True)




