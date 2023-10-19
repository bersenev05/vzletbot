import data
class Event:

    name = None
    date = None
    time = None
    location = None

    url_to_tgchat = None
    photo_path = None
    description = None
    creator = None
    vzletbusiness = None

    registrations = []

    def __init__(self, name, url_to_tgchat, photo_path, description, creator, vzletbusiness, date, location, time):
        self.name = name
        self.url_to_tgchat = url_to_tgchat
        self.photo_path = photo_path
        self.description = description
        self.creator = creator
        self.vzletbusiness = vzletbusiness
        self.date = date
        self.location = location
        self.time = time

    def GetInfo(self):

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
                  f'<b>Бизнес:</b> {self.vzletbusiness}\n\n')

        return message
