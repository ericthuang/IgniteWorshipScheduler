import MemberData as md
import Schedule as s
import Util as u
import os
import time
import random as r
import pprint
import json
import copy

OUTPUT_DIR = "output"


class SchedulerExecutive:
    def __init__(self, quarter, year, team_json, iter_count):
        # read in param json
        self.role_params = dict()
        role_param_json = u.get_roles()
        for role in role_param_json:
            self.role_params[role['role']] = role
        priority_sequence = [x['role'] for x in role_param_json]

        # prep member data
        self.member_data = md.MemberData(self.role_params, team_json, quarter, year)

        # get all sundays in this quarter
        self.sundays_datestrs = list()
        for sunday in u.get_all_sundays_in_quarter(quarter, year):
            self.sundays_datestrs.append(u.datetime_to_datestring(sunday))

        self.iteration_count = iter_count
        self.top_three = [{'score': 0}, {'score': 0}, {'score': 0}]  # list of dict of schedule of bands

        self.schedule = s.Schedule(self.role_params, priority_sequence, self.member_data.get_availability_matrix(),
                                   self.member_data)

    def run(self):
        r.seed(self.member_data.get_member_count() * len(self.role_params))  # this is super arbitrary
        # generate schedules
        try:
            for i in range(self.iteration_count):
                print("Iteration: " + str(i+1) + " - Current Best: " + str([x['score'] for x in self.top_three]))
                self.schedule.generate_new_schedule()
                this_score = self.schedule.get_current_score()
                insertion_index = self.get_top_three_insertion_index(this_score)
                if insertion_index != -1:
                    self.update_top_schedules(self.schedule.get_current_schedule_dict(), insertion_index)
        except:
            print("FAILED - SAVING RESULTS")
        self.save_top_three_file()
        # print(self.top_three[0].get_stats())

    def get_top_three_insertion_index(self, score):
        scores = [x['score'] for x in self.top_three]
        if score > scores[0]:
            return 0
        if score > scores[1]:
            return 1
        if score > scores[2]:
            return 2
        return -1

    def update_top_schedules(self, new_schedule_dict, insertion_index):
        self.top_three[insertion_index] = new_schedule_dict

    def print_schedule(self, num):
        pp = pprint.PrettyPrinter(indent=4)
        if 0 <= num < len(self.top_three):
            the_schedule = copy.deepcopy(self.top_three[num])
            for set_date in the_schedule.keys():
                if set_date != 'score':
                    for role in self.role_params.keys():
                        if len(the_schedule[set_date][role]) == 0 and self.role_params[role]['minCountPerTeam'] != 0:
                            the_schedule[set_date][role] = ["!!!!!!!!! MISSING !!!!!!!!!"]
            pp.pprint(the_schedule)

    def save_top_three_file(self):
        save_str = json.dumps(self.top_three)
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)

        path = OUTPUT_DIR + "/schedules_" + str(time.time()).replace(".", "")
        with open(path, "w") as this_file:
            this_file.write(save_str)


if __name__ == '__main__':
    num_schedule_iterations = 10000000
    quarter_num = 4
    year_num = 2019
    team = "team2019Q4.json"
    SE = SchedulerExecutive(quarter_num, year_num, team, num_schedule_iterations)
    SE.run()
    SE.print_schedule(0)

