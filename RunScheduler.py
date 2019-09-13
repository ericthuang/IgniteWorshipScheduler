import MemberData as md
import Schedule as s
import Util as u
import random as r

num_schedule_iterations = 100000
quarter = 3
year = 2019
r.seed(1234) # seed for reproducibility

if __name__ == '__main__':
    # prep member data
    member_data = md.MemberData("team.json", 3, 2019)

    # get all sundays in this quarter
    sundays_datestrs = list()
    for sunday in u.get_all_sundays_in_quarter(quarter, year):
        sundays_datestrs.append(u.datetime_to_datestring(sunday))

    # # generate schedules
    # high_score = 0
    # high_score_schedule_of_bands = None  # list sequence of current high score band
    # for i in range(num_schedule_iterations):
    #     this_schedule = s.Schedule(sundays_datestrs)
    #     # DO STUFF
    #
    #     # SCORE
    #     # this_schedule_score = score_schedule(this_schedule)
    #
    #     # high_score = max(high_score, this_schedule_score)

