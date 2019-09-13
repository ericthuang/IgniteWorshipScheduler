import Band as b

class Schedule:
    def __init__(self, list_of_sunday_datestrs):
        self.sundays = dict()
        for sunday in list_of_sunday_datestrs:
            self.sundays[sunday] = b.Band()
