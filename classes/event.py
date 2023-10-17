

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

