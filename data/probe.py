from classes.event import Event
import pathlib
from pathlib import Path
dir_path = pathlib.Path.cwd()

import datetime

eventbase={}
eventbase["0"] = Event(name="Встреча клуба Росмолодежь.Бизнес",
                       url_to_tgchat="vk.com/undaunt3d",
                       photo_path=Path(dir_path, "files", "photo", "rosmol.jpg"),
                       description="максимум 90 знаков",
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

eventbase["2"] = Event(name="Индекс 2",
                       url_to_tgchat="vk.com/undaunt3d",
                       photo_path=Path(dir_path, "files", "photo", "rosmol.jpg"),
                       description="приходите пж",
                       date = "11.03.2024",
                       creator="@vanya_slash",
                       vzletbusiness=True)

def date(date1):
    ddmmyyyy = date1.split(".")
    yyyymmdd = (int(ddmmyyyy[2]), int(ddmmyyyy[1]), int(ddmmyyyy[0]))
    return datetime.datetime(*yyyymmdd)

def sort_eventbase(eventbase):

    cases = list(eventbase.keys())
    for x in range(len(cases)):
        for y in range(x+1,len(cases)):
            date1 = date(eventbase[str(x)].date)
            date2 = date(eventbase[str(y)].date)
            if date1>date2:
                eventbase[str(x)], eventbase[str(y)] = eventbase[str(y)], eventbase[str(x)]

sort_eventbase(eventbase)

for i in list(eventbase.keys()):
    print(eventbase[i].name, eventbase[i].date)
