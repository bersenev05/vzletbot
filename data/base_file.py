import pathlib
from pathlib import Path

from classes.event import Event
from classes.user import User

dir_path = pathlib.Path.cwd()
import datetime

userbase = {}
# айди : объект класса юзер

eventbase = {}
# имя : объект класса эвент

learningbase = {}

workbase = {}

grantbase = {}

key_base = {}


async def date(date1):
    ddmmyyyy = date1.split(".")
    yyyymmdd = (int(ddmmyyyy[2]), int(ddmmyyyy[1]), int(ddmmyyyy[0]))
    return datetime.datetime(*yyyymmdd)


async def sort_user_regs(base):
    for x in range(len(base)):
        for y in range(x + 1, len(base)):
            date1 = await date(base[x].date)
            date2 = await date(base[y].date)
            if date1 > date2:
                base[x], base[y] = base[y], base[x]
    return base


async def sort_eventbase(eventbase):
    priority_event = []
    no_priority_event = []

    cases = list(eventbase.keys())

    # Получаем сегодняшнюю дату
    date_list = str(datetime.datetime.now()).split("-")
    now_date = await date(f"{str(date_list[2].split()[0])}.{str(date_list[1])}.{str(date_list[0])}")

    for event in cases:

        if await date(eventbase[str(event)].date) >= now_date:

            if eventbase[str(event)].priority == True:
                priority_event.append(eventbase[str(event)])
            else:
                no_priority_event.append(eventbase[str(event)])

    for x in range(len(no_priority_event)):
        for y in range(x + 1, len(no_priority_event)):
            date1 = await date(no_priority_event[x].date)
            date2 = await date(no_priority_event[y].date)
            if date1 > date2:
                no_priority_event[x], no_priority_event[y] = no_priority_event[y], no_priority_event[x]

    for x in range(len(priority_event)):
        for y in range(x + 1, len(priority_event)):
            date1 = await date(priority_event[x].date)
            date2 = await date(priority_event[y].date)
            if date1 > date2:
                priority_event[x], priority_event[y] = priority_event[y], priority_event[x]

    for_return_base = {}
    s = 0

    for event in priority_event + no_priority_event:
        for_return_base[str(s)] = event
        s += 1

    return for_return_base


async def sort_after_delete(eventbase, location):
    new_eventbase = {}
    del eventbase[location]

    val = [eventbase[key] for key in eventbase.keys()]
    for i in range(len(val)):
        new_eventbase[str(i)] = val[i]

    return new_eventbase


async def GetSystemFile_All():
    jsonbase = {}
    jsonbase['classes'] = {}
    jsonbase['keys'] = {}
    jsonbase['users'] = {}

    # Добавляем в словарь все классы и тд
    for base in [eventbase, learningbase, workbase, grantbase]:
        for city in base:
            if len(base[city]) != 0:
                for event in base[city]:

                    basename = ''
                    if base == eventbase:
                        basename = "eventbase"
                    elif base == learningbase:
                        basename = "learningbase"
                    elif base == workbase:
                        basename = 'workbase'
                    elif base == grantbase:
                        basename = 'grantbase'

                    if basename not in jsonbase['classes']: jsonbase['classes'][basename] = {}
                    if city not in jsonbase['classes'][basename]: jsonbase['classes'][basename][city] = {}
                    if event not in jsonbase['classes'][basename][city]: jsonbase['classes'][basename][city][event] = ''

                    jsonbase['classes'][basename][city][event] = await base[city][event].GetSystemFile()

    for user in userbase:
        if user not in jsonbase['users']: jsonbase['users'][user] = {}
        jsonbase['users'][user] = await userbase[str(user)].GetSystemFile()

    for key in key_base:
        if key not in jsonbase['keys']: jsonbase['keys'][key] = {}
        jsonbase['keys'][key] = await key_base[key].GetSystemFile()

    file = open('SystemFile.txt', 'w+')
    file.write(str(jsonbase))
    file.close()

async def antinone(none):
    if none == "None":
        return None
    else:
        return none
async def raspakovka(systemfile, basename):

    newbase = {}
    for datatype in systemfile:
        if datatype == 'classes':
            for city in systemfile['classes'][basename]:
                if city not in newbase: newbase[city] = {}
                for event in systemfile['classes'][basename][city]:
                    info = systemfile['classes'][basename][city][event]

                    base_hub = ''
                    key_event = False
                    for new_city in newbase:
                        for new_event in newbase[new_city]:
                            if newbase[new_city][new_event].key == info['key']:
                                base_hub = newbase[new_city][new_event]
                                key_event = True

                    if key_event == True:
                        newbase[city][event] = base_hub
                    else:
                        systemfile_event = Event(name=await antinone(info['name']),
                                                 url_to_tgchat=await antinone(info['url_to_tgchat']),
                                                 photo_path=await antinone(info['photo_path']),
                                                 description=await antinone(info['description']),
                                                 date=await antinone(info['date']),
                                                 time=await antinone(info['time']),
                                                 creator=await antinone(info['creator']),
                                                 location=await antinone(info['location']),
                                                 city=await antinone(info['city']),
                                                 key = await antinone(info['key']),
                                                 registrationmode=await antinone(info['registrationmode']))

                        systemfile_event.registrations = info['registrations'].split("*")[:-1]
                        newbase[city][event] = systemfile_event

    return newbase

async def raspakovka_users(systemfile):
    new_userbase = {}
    for datatype in systemfile:
        if datatype == 'users':
            for user_id in systemfile['users']:
                info = systemfile['users'][user_id]

                new_userbase[user_id] = User(username=info['username'], id = info['id'])

                new_userbase[user_id].city = await antinone(info['city'])
                new_userbase[user_id].last_message = await antinone(info['last_message'])
                new_userbase[user_id].fio = await antinone(info['fio'])
                new_userbase[user_id].vuz = await antinone(info['vuz'])
                new_userbase[user_id].phone = await antinone(info['phone'])
                new_userbase[user_id].portfolio = await antinone(info['portfolio'])
                new_userbase[user_id].permission = await antinone(info['permission'])
                new_userbase[user_id].location = '0'
                new_userbase[user_id].admin_ikb = await antinone(info['admin_ikb'])

                new_userbase[user_id].create_hub = ''
                new_userbase[user_id].registration_hub = ''

                new_userbase[user_id].actions = info['actions'].split("*")[:-1]
                new_userbase[user_id].target_keys = []
                new_userbase[user_id].registrations = []

    return new_userbase




