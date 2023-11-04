
import pathlib
from pathlib import Path
dir_path = pathlib.Path.cwd()
import datetime

userbase = {}
# айди : объект класса юзер

eventbase = {}
# имя : объект класса эвент

learningbase = {}

workbase = {}

grantbase = {}



async def date(date1):
    ddmmyyyy = date1.split(".")
    yyyymmdd = (int(ddmmyyyy[2]), int(ddmmyyyy[1]), int(ddmmyyyy[0]))
    return datetime.datetime(*yyyymmdd)


async def sort_user_regs(base):

    for x in range(len(base)):
        for y in range(x+1,len(base)):
            date1 = await date(base[x].date)
            date2 = await date(base[y].date)
            if date1>date2:
                base[x], base[y] = base[y], base[x]
    return base

async def sort_eventbase(eventbase):

    priority_event = []
    no_priority_event = []

    cases = list(eventbase.keys())

    for event in cases:
        if eventbase[str(event)].priority == True:
            priority_event.append(eventbase[str(event)])
        else:
            no_priority_event.append(eventbase[str(event)])


    for x in range(len(no_priority_event)):
        for y in range(x+1,len(no_priority_event)):
            date1 = await date(no_priority_event[x].date)
            date2 = await date(no_priority_event[y].date)
            if date1>date2:
                no_priority_event[x], no_priority_event[y] = no_priority_event[y], no_priority_event[x]

    for x in range(len(priority_event)):
        for y in range(x+1,len(priority_event)):
            date1 = await date(priority_event[x].date)
            date2 = await date(priority_event[y].date)
            if date1>date2:
                priority_event[x], priority_event[y] = priority_event[y], priority_event[x]

    for_return_base = {}
    s = 0

    for event in priority_event + no_priority_event:
        for_return_base[str(s)] = event
        s+=1


    return for_return_base



async def sort_after_delete(eventbase,location):
    new_eventbase = {}
    del eventbase[location]

    val = [eventbase[key] for key in eventbase.keys()]
    for i in range(len(val)):
        new_eventbase[str(i)] = val[i]

    return new_eventbase
