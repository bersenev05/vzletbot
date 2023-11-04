from classes.event import Event
from classes.work import Work
from classes.grant import Grant
from classes.learning import Learning
from data.base_file import userbase, eventbase, sort_eventbase, sort_after_delete, learningbase, workbase, grantbase
import pathlib
from pathlib import Path

dir_path = pathlib.Path.cwd()

workbase["Красноярск"] = {}
learningbase["Красноярск"] = {}
eventbase["Красноярск"] = {}
grantbase["Красноярск"] = {}

workbase["Красноярск"]["0"] = Work(name="Менеджер по работе с партнерами Вконтакте",
                                   url_to_tgchat="https://t.me/+9PY3bcf3ZH01MDZi",
                                   photo_path=Path(dir_path, "files", "photo", "events", "vk-min.png"),
                                   description="Стажёр будет участвовать в разработке концепций и интеграций сервисов и продуктов ВКонтакте с партнёрами в направлении «Образование и книги»",
                                   date="19.11.2023",
                                   time="12:00",
                                   creator="5965231899",
                                   location="online",
                                   city="Красноярск")

workbase["Красноярск"]["1"] = Work(name="Flutter-разработчик в Яндекс",
                                   url_to_tgchat="https://t.me/+9PY3bcf3ZH01MDZi",
                                   photo_path=Path(dir_path, "files", "photo", "python.jpg"),
                                   description="Открыт набор на осеннюю оплачиваемую стажировку. Подавайте заявки! Если вы отлично себя проявите, можете продолжить работать с нами. Более 50% стажёров становятся штатными сотрудниками Яндекса.",
                                   date="20.12.2023",
                                   time="12:00",
                                   creator="5965231899",
                                   location="online",
                                   city="Красноярск")

learningbase["Красноярск"]["0"] = Learning(name="Школа анализа данных от Яндекса",
                                           url_to_tgchat="https://t.me/+9PY3bcf3ZH01MDZi",
                                           photo_path=Path(dir_path, "files", "photo", "events", "shad-min.png"),
                                           description="Двухгодичная программа, на которой вы научитесь разрабатывать сервисы на базе ML, анализировать данные, создавать системы хранения и обработки больших данных и многое другое",
                                           date="12.11.2023",
                                           time="12:00",
                                           creator="5965231899",
                                           location="online",
                                           city="Красноярск")

learningbase["Красноярск"]["1"] = Learning(name="Тинькофф.Финтех - онлайн курс по бизнес-анализу",
                                           url_to_tgchat="https://t.me/+9PY3bcf3ZH01MDZi",
                                           photo_path=Path(dir_path, "files", "photo", "events", "tinkoff-min.jpg"),
                                           description="Проводим обучение и оплачиваемые стажировки по направлениям аналитики, бэкенд- и фронтенд-разработки, QA, маркетинга и другим",
                                           date="16.12.2023",
                                           time="12:00",
                                           creator="5965231899",
                                           location="online",
                                           city="Красноярск")

learningbase["Красноярск"]["2"] = Learning(name="Разработка программного обеспечения на Python. Цифровая кафедра СФУ",
                                           url_to_tgchat="https://t.me/+9PY3bcf3ZH01MDZi",
                                           photo_path=Path(dir_path, "files", "photo", "events", "python-min.jpg"),
                                           description="Бесплатное обучение! Описание...",
                                           date="16.03.2025",
                                           time="12:00",
                                           creator="5965231899",
                                           location="online",
                                           city="Красноярск")

eventbase["Красноярск"]["0"] = Event(name="Встреча клуба Росмолодежь.Бизнес",
                                     url_to_tgchat="https://t.me/+9PY3bcf3ZH01MDZi",
                                     photo_path=Path(dir_path, "files", "photo", "events", "rosmolbusiness-min.jpg"),
                                     description="Мощнейшее объединение молодых предпринимателей твоего города. Проводим встречи, мастермайнды, встречи с большим бизнесом и т.д.",
                                     date="4.11.2023",
                                     time="12:00",
                                     creator="5965231899",
                                     location="Культурная станция Гагарин. Маерчака 17",
                                     city="Красноярск")

eventbase["Красноярск"]["1"] = Event(name="Я в деле",
                                     url_to_tgchat="https://t.me/+9PY3bcf3ZH01MDZi",
                                     photo_path=Path(dir_path, "files", "photo", "events", "yavdele-min.jpg"),
                                     description="Предпринимательский кейс-чемпионат. Создай свой бизнес-проект с помощью наставников. Победитель регионального этапа едет в Москву!",
                                     date="5.11.2023",
                                     time="12:00",
                                     creator="5965231899",
                                     location="Точка Кипения. Квант",
                                     city="Красноярск")

eventbase["Красноярск"]["2"] = Event(name="Битва Креаторов",
                                     url_to_tgchat="https://t.me/+9PY3bcf3ZH01MDZi",
                                     photo_path=Path(dir_path, "files", "photo", "events", "bitva-min.jpg"),
                                     description="Первое в Красноярске реалити-шоу о креативных предпринимателях Сибири. Проходи отбор! Пять победителей получат по миллиону рублей!",
                                     date="6.11.2023",
                                     time="12:00",
                                     creator="5965231899",
                                     location="Креативный кластер Квадрат",
                                     city="Красноярск")

eventbase["Красноярск"]["3"] = Event(name="Красноярский экономический форум",
                                     url_to_tgchat="https://t.me/+9PY3bcf3ZH01MDZi",
                                     photo_path=Path(dir_path, "files", "photo", "events", "kef-min.jpg"),
                                     description="Самый масштабный в Сибири форум об экономическом развитии страны. Будет много спикеров и интересных площадок. Обсудим взаимодействие госудаства с бизнесом.",
                                     date="7.11.2023",
                                     time="12:00",
                                     creator="5965231899",
                                     location="Конгресс-холл СФУ",
                                     city="Красноярск")

grantbase["Красноярск"]["0"] = Grant(name="Фонд Бортника",
                                     url_to_tgchat="https://t.me/+9PY3bcf3ZH01MDZi",
                                     photo_path=Path(dir_path, "files", "photo", "events", "kef-min.jpg"),
                                     description="Гранты до 3 млн.руб",
                                     date="7.11.2023",
                                     time="12:00",
                                     creator="5965231899",
                                     location="online",
                                     city="Красноярск")
