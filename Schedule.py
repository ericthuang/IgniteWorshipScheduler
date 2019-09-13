import Band as b


class Schedule:
    def __init__(self, role_params, availability_matrx):
        # availability_matrix: date -> role -> primary/secondary -> list of emails
        self.availability_matrix = availability_matrx;
        self.role_params = role_params

        self.bands = dict() # key: datestr, value: band object
        self.current_score = 0

    def generate_new_schedule(self):
        self._clear_current_schedule()
        for this_band in self.bands.keys():
            self.bands[this_band] = b.Band(self.role_params, self.availability_matrix[this_band])
            self.bands[this_band].generate_band()
        self._score_current_schedule()

    def _score_current_schedule(self):
        '''
        +3 for each sunday band that is complete (contains leader, lead rhythm instrument, bass, keys, drums)
        +2 if low variability of utilization across all ministry members (goal is for close to uniform utilization)
        +2 for each pair of consecutive Sundays that do not have carryover members (check with moving window)
        +2 for each set of 3 consecutive Sundays that do not have carryover members (check with moving window)
        +2 for each sunday band that has two leads
        +2 for each sunday band that has a secondary vocalist
        +2 for each sunday band that has a lead electric guitarist
        +1 for each sunday band that that has a second keyboardist
        +1 for each sunday band that has a percussionist
        +1 for each member that serves in their secondary role at least once per term and no more than 50% of their Sundays
        '''

        import random
        self.current_score = random.randint(1, 101)

    def get_current_schedule_dict(self):
        this_schedule = dict()
        this_schedule['score'] = self.get_current_score()
        for this_band_date in self.bands.keys():
            this_schedule[this_band_date] = self.bands[this_band_date].get_band_dict()
        return this_schedule

    def get_current_score(self):
        return self.current_score

    def _clear_current_schedule(self):
        for sunday in self.availability_matrix.keys():
            self.bands[sunday] = None
        self.current_score = 0
