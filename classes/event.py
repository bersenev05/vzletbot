import data
import pathlib
from pathlib import Path
dir_path = pathlib.Path.cwd()

class Event:
    type = "Мероприятие"
    name = None
    date = None
    time = None
    location = None
    priority = None
    city = None
    key = None

    url_to_tgchat = None
    photo_path = None
    description = None
    creator = None
    vzletbusiness = None

    registrations = []

    def __init__(self, key, city, name, url_to_tgchat, photo_path, description, creator, date, location, time):
        self.name = name
        self.url_to_tgchat = url_to_tgchat
        self.photo_path = photo_path
        self.description = description
        self.creator = creator
        self.date = date
        self.location = location
        self.time = time
        self.registrations = []
        self.city = city
        self.key = key

    async def GetInfo(self):

        message =(f'<b>Название:</b> {self.name}\n\n'
                  f'<b>Описание:</b> {self.description}\n\n'
                  f''
                  f'<b>Дата:</b> {self.date}\n'
                  f'<b>Время:</b> {self.time}\n'
                  f'<b>Место:</b> {self.location}\n\n'
                  f''
                  f'<b>Создатель:</b> @{data.base_file.userbase[str(self.creator)].username}\n'
                  f'<b>Чат:</b> {self.url_to_tgchat}\n'
                  f'<b>Фото:</b> {self.photo_path}\n\n'
                  f'<b>Город:</b> {self.city}\n\n')

        return message

    async def GetInfoFile(self):

        file = open(Path(dir_path, "files", "EventFiles", f"{self.name}.txt"), "w")

        file.write(f'Название: {self.name}\n\n'
                  f'Описание: {self.description}\n\n'
                  f''
                  f'Дата: {self.date}\n'
                  f'Время: {self.time}\n'
                  f'Место: {self.location}\n\n'
                  f''
                  f'Создатель: @{data.base_file.userbase[str(self.creator)].username}\n'
                  f'Чат: {self.url_to_tgchat}\n'
                  f'Фото: {self.photo_path}\n\n'
                  f'Город: {self.city}\n\n'
                   f'Ключ: {self.key}\n\n'
                   f'-----------------------------------------\n\n')

        file.write("ЗАРЕГИСТРИРОВАННЫЕ ПОЛЬЗОВАТЕЛИ\n\n")

        s=0
        for id in self.registrations:
            s+=1
            user = data.base_file.userbase[id]
            file.write(f'{s}. @{user.username}, {user.fio}, {user.phone}\n')

        file.close()

        return Path(dir_path, "files", "EventFiles", f"{self.name}.txt")


