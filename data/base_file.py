from classes.event import Event
import pathlib
from pathlib import Path
dir_path = pathlib.Path.cwd()
import datetime

userbase = {}
# айди : объект класса юзер

eventbase = {}
# имя : объект класса эвент


async def date(date1):
    ddmmyyyy = date1.split(".")
    yyyymmdd = (int(ddmmyyyy[2]), int(ddmmyyyy[1]), int(ddmmyyyy[0]))
    return datetime.datetime(*yyyymmdd)

async def sort_eventbase(eventbase):

    cases = list(eventbase.keys())
    for x in range(len(cases)):
        for y in range(x+1,len(cases)):
            date1 = await date(eventbase[str(x)].date)
            date2 = await date(eventbase[str(y)].date)
            if date1>date2:
                eventbase[str(x)], eventbase[str(y)] = eventbase[str(y)], eventbase[str(x)]
    return eventbase

