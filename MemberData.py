import Member as m
import Util as u
import copy as cp
import json


class MemberData:
    def __init__(self, json_path, quarter, year):
        self.memberInfo = dict()  # key: emailstr, value: Member object
        self.availability_matrix = dict()  # date -> role -> primary/secondary -> list of emails

        self._from_json(json_path)
        self._set_availability_matrix(quarter, year)

    def _from_json(self, path):
        # import member data
        data = None
        with open(path, 'r') as file:
            data = file.read()

        member_dicts = json.loads(data)

        for mem in member_dicts:
            self._add_member(mem['email'], mem['name'], mem['primary'], mem['secondary'], mem['unavailableSundays'])

    def _add_member(self, email, name, primary_roles, secondary_roles, blackout_dates):
        thisMember = m.Member(name, primary_roles, secondary_roles, blackout_dates)
        self.memberInfo[str(email)] = thisMember

    def _set_availability_matrix(self, quarter, year):
        sundays_datestrs = list()

        # set all dates
        for sunday in u.get_all_sundays_in_quarter(quarter, year):
            sundays_datestrs.append(u.datetime_to_datestring(sunday))

        template_dict_of_all_roles = dict()
        for role in u.ROLES:
            template_dict_of_all_roles[role] = dict()
            template_dict_of_all_roles[role]["primary"] = list()
            template_dict_of_all_roles[role]["secondary"] = list()

        # initialize
        for i in sundays_datestrs:
            self.availability_matrix[i] = cp.deepcopy(template_dict_of_all_roles)

        for memEmail in self.memberInfo.keys():
            available_sundays = [x for x in sundays_datestrs
                                 if x not in self.memberInfo[memEmail].get_blackout_dates_str()]
            for sunday in available_sundays:
                for prole in self.memberInfo[memEmail].get_primary_roles():
                    self.availability_matrix[sunday][prole]["primary"].append(memEmail)
                for srole in self.memberInfo[memEmail].get_secondary_roles():
                    self.availability_matrix[sunday][srole]["secondary"].append(memEmail)

    def get_availability_matrix(self):
        return self.availability_matrix

    def get_member_count(self):
        return len(self.memberInfo.keys())

    def get_member_names(self):
        return [self.memberInfo[y].getName() for y in self.memberInfo.keys()]

    def get_member_emails(self):
        return self.memberInfo.keys()

    def get_member(self, email):
        return self.memberInfo[email]


if __name__ == '__main__':
    x = MemberData("team.json", 3, 2019)
    AM = x.get_availability_matrix()
    # date -> role -> primary/secondary -> list of emails

    # assert that the blackout dates are correct
    for mem_email in x.get_member_emails():
        this_member = x.get_member(mem_email)
        blackout = this_member.get_blackout_dates_str()
        roles_prim = this_member.get_primary_roles()
        roles_sec = this_member.get_secondary_roles()

        for date_str in blackout:
            for role in roles_prim:
                assert (mem_email not in AM[date_str][role]["primary"])
            for role in roles_sec:
                assert (mem_email not in AM[date_str][role]["secondary"])
