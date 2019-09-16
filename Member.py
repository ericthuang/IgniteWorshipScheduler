from datetime import datetime
import Util as u


class Member:
    def __init__(self, name, primary_roles, secondary_roles, blackout_dates):
        self.name = str(name)
        self.primaryRoles = [str(i) for i in primary_roles] # includes lead, vocal
        self.secondaryRoles = [str(i) for i in secondary_roles]
        self.blackoutDatesStr = [str(x) for x in blackout_dates]
        self.blackoutDates = [u.datestring_to_datetime(x) for x in blackout_dates]

    def get_name(self):
        return self.name

    def get_primary_roles(self):
        return self.primaryRoles

    def get_secondary_roles(self):
        return self.secondaryRoles

    def get_blackout_dates(self):
        return self.blackoutDates

    def get_blackout_dates_str(self):
        return self.blackoutDatesStr



if __name__ == '__main__':
    pass