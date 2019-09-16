import Band as b
import math


class Schedule:
    def __init__(self, role_params, priority_sequence, availability_matrix, member_data):
        self.member_data = member_data
        # availability_matrix: date -> role -> primary/secondary -> list of emails
        self.availability_matrix = availability_matrix # passed in so we dont have to rerun this func every time
        self.priority_sequence = priority_sequence
        self.role_params = role_params
        self.ordered_sunday_date_strs = sorted(self.availability_matrix.keys())
        self.bands = dict() # key: datestr, value: band object
        self.current_score = 0

    def get_stats(self):
        stats = dict()

        # score
        stats['score'] = self.current_score

        # number of sundays
        stats['sunday_count'] = len(self.availability_matrix)

        # percentage of sets complete
        total_complete_sets = 0
        for band in self.bands.keys():
            if self.bands[band].band_is_complete():
                total_complete_sets += 1
        stats['complete_sets_ratio'] = total_complete_sets / len(self.bands.keys())

        # mean utilization percent
        stats['mean_utilization'] = self.get_utilization_ratio_mean()

        # std utilization percent
        stats['std_utilization'] = self.get_utilization_ratio_std()

        # percentage of sets with co leaders
        stats['coled_sets_ratio'] = len([x if len(self.bands[x].get_band_dict()['lead']) > 1 else ''
                                         for x in self.bands.keys()]) / len(self.bands.keys())

        # percentage of fully loaded bands

    def get_utilization_ratio_mean(self):
        utilization = self.get_utilization_ratio()
        util_values = [utilization[x]/len(self.availability_matrix) for x in utilization.keys()]
        return sum(util_values) / len(util_values)

    def get_utilization_ratio_std(self):
        utilization = self.get_utilization_ratio()
        util_values = [utilization[x] / len(self.availability_matrix) for x in utilization.keys()]
        mean = sum(util_values) / len(util_values)
        var = sum(pow(x - mean, 2) for x in util_values) / len(util_values)
        return math.sqrt(var)

    def get_utilization_ratio(self):
        utilization = dict()
        for band in self.bands.keys():
            for mem_email in self.bands[band].get_member_emails():
                if mem_email not in utilization.keys():
                    utilization[mem_email] = 1
                else:
                    utilization[mem_email] += 1
        return utilization

    def generate_new_schedule(self):
        self._clear_current_schedule()

        # print(self.availability_matrix[self.bands.keys()[0]])
        for this_band in self.bands.keys():
            self.bands[this_band] = b.Band(self.role_params, self.priority_sequence, self.member_data,
                                           self.availability_matrix[this_band])
            self.bands[this_band].generate_band()
        self._score_current_schedule()

    def _score_current_schedule(self):
        # low variability in utilization ratio (people dont serve too dang much more than others)
        if self.get_utilization_ratio_std() < 1:
            self.current_score += 5

        # low utilization ratio
        if self.get_utilization_ratio_mean() < 0.4:
            self.current_score += 5

        # check all bands
        for band in self.bands:
            # +3 for each sunday band that is complete (meets minimum role requirements)
            if self.bands[band].band_is_complete():
                self.current_score += 3
            # +2 for each sunday band that has two leads
            if len(self.bands[band].get_band_dict()['lead']) > 1:
                self.current_score += 2
            # +2 for each sunday band that has a non-lead vocalist
            if len(self.bands[band].get_band_dict()['vocals']) > 0:
                self.current_score += 2
            # +2 for each sunday band that has a lead electric guitarist
            if len(self.bands[band].get_band_dict()['leadElectric']) > 0:
                self.current_score += 2
            # +1 for each sunday band that that has a lead keyboardist
            if len(self.bands[band].get_band_dict()['leadKeys']) > 0:
                self.current_score += 2
            # +1 for each sunday band that has a percussionist
            if len(self.bands[band].get_band_dict()['percussion']) > 0:
                self.current_score += 2

        # +10 for each pair of consecutive Sundays that do not have carryover members (check with moving window)
        for i in range(len(self.ordered_sunday_date_strs)-1):
            band_a_members = self.bands[self.ordered_sunday_date_strs[i]].get_member_emails()
            band_b_members = self.bands[self.ordered_sunday_date_strs[i+1]].get_member_emails()

            if len(band_a_members.union(band_b_members)) == len(list(band_a_members) + list(band_b_members)):
                self.current_score += 10

        # +10 for each set of 3 consecutive Sundays that do not have carryover members (check with moving window)
        for i in range(len(self.ordered_sunday_date_strs)-2):
            band_a_members = self.bands[self.ordered_sunday_date_strs[i]].get_member_emails()
            band_b_members = self.bands[self.ordered_sunday_date_strs[i+1]].get_member_emails()
            band_c_members = self.bands[self.ordered_sunday_date_strs[i+2]].get_member_emails()

            if len(band_a_members.union(band_b_members).union(band_c_members)) \
                    == len(list(band_a_members) + list(band_b_members) + list(band_c_members)):
                self.current_score += 10

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
