from datetime import datetime

dad_admin = ["5965231899"]
son_admin = ["5965231899"]
cityes = ["Красноярск", "Другой город"]

class User:

    id = None             #айдёюзера
    username = None       #телеграмм юзернейм
    last_message = None   #последнее сообщение юзеру
    fio = None            #ФИО

    city = None           #город
    vuz = None            #вуз
    phone = None          #номер телефона

    actions = []          #действия, совершённые пользователем
    target_keys = []      #метки для таргетированной рекламы
    registrations = []    #мероприятия, на которые зарегистрирован юзер

    portfolio = None      #портфолио

    permission = None     #разрешение (admin,user,redactor)

    location = None       #место в карусели
    registration_hub = None  #Хаб для регистрации
    create_hub = None        #Хаб для создания эвента
    priority = None          #Приоритет в выдаче
    admin_ikb = None



    def __init__(self,username,id):
        self.id = id
        self.username = username
        self.last_message = None
        self.fio = None
        self.city = None
        self.vuz = None
        self.phone = None
        self.actions = []
        self.target_keys = []
        self.registrations = []
        self.portfolio = None
        self.permission = None
        self.location = None
        self.registration_hub = None
        self.create_hub = None
        self.admin_ikb = None

    async def AddAction(self, action):
        time = datetime.now().strftime("%d.%m %H:%M:%S")
        self.actions.append(f"{time} = {action}")

    async def GetInfo(self):
        message = f"<b>username:</b> @{self.username}\n"\
                  f"<b>id:</b> <code>{self.id}</code>\n"
        return message

    async def GetSystemFile(self):
        system_file = {}
        system_file['actions'] = ''
        system_file['registrations'] = ''
        for attr in self.__dict__.keys():
            if attr == 'registrations':
                system_file[attr] = ''
            elif attr == 'actions':
                for event in self.__dict__[attr]:
                    system_file[attr]+=f'{event}*'
            else:
                system_file[attr] = str(self.__dict__[attr])
        return system_file


