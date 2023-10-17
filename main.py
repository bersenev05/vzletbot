
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from classes.user import User, admin, cityes
from classes.event import Event
from data.base_file import userbase, eventbase
import pathlib
from pathlib import Path
dir_path = pathlib.Path.cwd()



bot = Bot(token = "6100104762:AAFVZRJCVVhtula5Bo6bGlDlpPtjuav7qlI",
          parse_mode="HTML")
dp = Dispatcher(bot)

statisticbot = Bot(token = "6681358573:AAEDPtrd3jNn82es9LS69eDOicI0ih9FSxk",
                   parse_mode="HTML")





eventbase["0"] = Event(name="Встреча клуба Росмолодежь.Бизнес",
                       url_to_tgchat="vk.com/undaunt3d",
                       photo_path=Path(dir_path, "files", "photo", "rosmol.jpg"),
                       description="Тут будет описание",
                       date = "16.03.2024",
                       creator="@vanya_slash",
                       vzletbusiness=True)

eventbase["1"] = Event(name="Я в деле",
                       url_to_tgchat="vk.com/undaunt3d",
                       photo_path=Path(dir_path, "files", "photo", "yavdele.jpg"),
                       description="Предпринимательский кейс-чемпионат. Создай свой бизнес-проект с помощью наставников",
                       date = "15.03.2024",
                       creator="@vanya_slash",
                       vzletbusiness=True)

eventbase["2"] = Event(name="Битва Креаторов",
                       url_to_tgchat="vk.com/undaunt3d",
                       photo_path=Path(dir_path, "files", "photo", "institut.jpg"),
                       description="приходите пж",
                       date = "11.03.2024",
                       creator="@vanya_slash",
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
    btn1 = InlineKeyboardButton(text = "Мероприятия", callback_data="events")
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


@dp.callback_query_handler(text = "events")
async def events(message: types.CallbackQuery):

    # получаем объект класса юзер. Чисто для укорачивания кода
    user = userbase[str(message.from_user.id)]

    # добавляем действие
    await user.AddAction(f"Выбрал {message.data}")

    # обнуляем локейшн для дальнейшего движения по карусели
    user.location = None

    # клавиатура
    ikb = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(text="Полетели!", callback_data="eventsnext")
    btn2 = InlineKeyboardButton(text="◀️ Назад", callback_data=user.city)
    ikb.add(btn1).add(btn2)

    png = open(Path(dir_path, "files", "photo", "events.png"), "rb")
    photo = types.InputMediaPhoto(png, caption="В этом разделе собраны все ближайшие мероприятия в твоём городе.\n\n "
                                               "Ты можешь мгновенно зарегистрироваться и получить ссылку на общий чат.\n\n "
                                               "Участвуй в мероприятиях и получай баллы активности. "
                                               "Ты можешь менять их на скидки и подарки у наших партнеров")

    # Редактируем сообщения
    await bot.edit_message_media(chat_id=user.id,
                                 message_id=user.last_message,
                                 media=photo,
                                 reply_markup=ikb)

    png.close()



@dp.callback_query_handler(text=["eventsnext","eventsback"])
async def events1(message: types.CallbackQuery):

    # получаем объект класса юзер. Чисто для укорачивания кода
    user = userbase[str(message.from_user.id)]

    # добавляем действие
    await user.AddAction(f"кейс ")

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

    event = eventbase[user.location]

    # клавиатура
    ikb = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(text="Назад", callback_data="eventsback")
    btn2 = InlineKeyboardButton(text="Далее", callback_data="eventsnext")
    btn3 = InlineKeyboardButton(text="🕹 Зарегистрироваться", callback_data="registration")
    btn5 = InlineKeyboardButton(text="🗂 Главное меню", callback_data="mainmenu")
    ikb.row(btn1,btn2).add(btn3).add(btn5)


    png = open(event.photo_path, "rb")
    photo = types.InputMediaPhoto(png, caption=f"<b>{event.name}</b>\n\n"
                                               f"{event.description}\n\n"
                                               f"<b>Дата:</b> {event.date}")

    # Редактируем сообщения
    await bot.edit_message_media(chat_id=user.id,
                                 message_id=user.last_message,
                                 media=photo,
                                 reply_markup=ikb)

    png.close()
























if __name__ == "__main__":
    executor.start_polling(dp,
                           skip_updates=True)




