import random as r
import copy


class Band:
    def __init__(self, role_params, priority_sequence, member_data, availability_matrix):
        self.member_data = member_data
        # role -> primary/secondary -> list of emails
        self.availability = availability_matrix
        self.priority_sequence = priority_sequence
        self.band_members = dict()  # key: role, value: list of members
        self.emails = set()
        self.role_params = role_params

        for role in self.role_params.keys():
            self.band_members[role] = list()

    def get_member_emails(self):
        return self.emails

    # def _prune_candidates(self, candidate_list, target_role):
    #     # return empty candidate list if role is already maxed out or candidate list is already empty
    #     if not len(candidate_list):
    #         return dict()
    #
    #     for cand in candidate_list:
    #         # remove people already serving
    #         if cand in self.emails:
    #             candidate_list.remove(cand)
    #         # if target_role is not lead, but this candidate is a lead, remove
    #         elif target_role != 'lead' and cand in self.availability['lead']['primary']:
    #             candidate_list.remove(cand)
    #
    #     # add combo roles
    #     candidates_with_combos = dict()
    #     for cand in candidate_list:
    #         all_roles_for_this_candidate = self.member_data.get_member(cand).get_primary_roles()
    #         candidates_with_combos[cand] = list(all_roles_for_this_candidate)  # make copy
    #         # prune combo roles
    #         try:
    #             candidates_with_combos[cand].remove(str(target_role))  # remove this target role
    #         except:
    #             who_cares = 0
    #
    #         for cr in candidates_with_combos[cand]:
    #             if len(self.band_members[cr]) == self.role_params[cr]['maxCountPerTeam']:
    #                 candidates_with_combos[cand].remove(cr)
    #
    #         # don't schedule additional worship leaders if their pruned combo list len is 0
    #         # exception if vocalist leaders, who don't have combo besides 'lead'
    #         if all_roles_for_this_candidate != ['lead'] and target_role == 'lead' and len(candidates_with_combos[cand]):
    #             candidates_with_combos.pop(cand)
    #     return candidates_with_combos

    def _prune_candidates(self, candidate_list, target_role):
        # return empty candidate list if role is already maxed out or candidate list is already empty
        candidates_with_combos = dict()
        if not len(candidate_list)\
                or len(self.band_members[target_role]) >= self.role_params[target_role]['maxCountPerTeam']:
            return candidates_with_combos

        for cand in candidate_list:
            # add people not already serving
            if cand not in self.emails:
                candidates_with_combos[cand] = list()
            # don't let leaders get added to non lead roles
            elif target_role != 'lead':
                if cand not in self.availability['lead']['primary']:
                    candidates_with_combos[cand] = list()
        # assign legal combos
        for cand in candidates_with_combos.keys():
            for combo_role in self.member_data.get_member(cand).get_primary_roles():
                if combo_role != target_role:
                    if len(self.band_members[combo_role]) < self.role_params[combo_role]['maxCountPerTeam']:
                        candidates_with_combos[cand].append(combo_role)
            if ('lead' in self.member_data.get_member(cand).get_primary_roles()
                    or 'vocals' in self.member_data.get_member(cand).get_primary_roles()) \
                    and not len(candidates_with_combos[cand]):
                candidates_with_combos.pop(cand)

        return candidates_with_combos

    def generate_band(self):
        for role in self.priority_sequence:
            required_minimum = self.role_params[role]['minCountPerTeam']

            # prune candidates list, remove people who are already serving in this set
            pruned_primary_candidates_dict = self._prune_candidates(copy.deepcopy(self.availability[role]['primary']),
                                                                    role)
            pruned_secondary_candidates_dict = self._prune_candidates(
                copy.deepcopy(self.availability[role]['secondary']), role)

            # if there are 0 candidates available (both primary and secondary) for this role
            if len(pruned_primary_candidates_dict.keys()) or len(pruned_secondary_candidates_dict.keys()):
                candidates = pruned_primary_candidates_dict
                if required_minimum != 0 and len(candidates) == 0:
                    # if we need at least 1 and there are no primary candidates, look in secondary
                    candidates = pruned_secondary_candidates_dict  # guaranteed non-empty

                # At this point, candidates can be either empty or filled with secondary candidates, both are fine.
                # If required minimum is not 0, and no primary candidates available, candidates will remain empty
                # and "NONE" will be sampled, leaving the position vacant

                # in case there are too many options haha... someday
                max_that_can_be_assigned = min(len(candidates.keys()), self.role_params[role]['maxCountPerTeam'])
                if max_that_can_be_assigned == 0:
                    continue
                elif max_that_can_be_assigned == 1:
                    number_of_people_to_assign_for_this_role = 1
                else:
                    probability_array_for_multi_member_role = list()
                    for i in range(max_that_can_be_assigned):
                        # at least 1
                        probability_array_for_multi_member_role += [i + 1 for x in range(max_that_can_be_assigned - i)]
                    number_of_people_to_assign_for_this_role = \
                        choose_random_element(probability_array_for_multi_member_role)

                while number_of_people_to_assign_for_this_role > 0:
                    if len(self.band_members[role]) < required_minimum:
                        random_person = choose_random_element(candidates.keys(), 0)  # no Nones allowed
                    else:
                        none_count = (max_that_can_be_assigned - len(self.band_members[role])) * 10
                        random_person = choose_random_element(candidates.keys(), none_count)  # otherwise it's ok to omit sometimes

                    if random_person:  # if it's not a None
                        self.assign_role(role, candidates[random_person], random_person)
                        candidates.pop(random_person)  # so they don't get picked again
                    number_of_people_to_assign_for_this_role -= 1

    def band_is_complete(self):
        for role in self.role_params:
            if len(self.band_members[role]) < self.role_params[role]['minCountPerTeam']:
                return False
        return True

    def assign_role(self, role, possible_combos, email):
        self.band_members[role].append(email)
        if possible_combos and len(possible_combos) > 0:
            chosen_combo_role = choose_random_element(possible_combos, 0)
            self.band_members[chosen_combo_role].append(email)
        self.emails.add(email)

    def get_band_dict(self):
        return self.band_members


def choose_random_element(candidate_list, none_count=0):
    contains_none = False
    if none_count:
        for i in range(none_count):
            candidate_list.append("##NONE##")
            contains_none = True

    chosen = r.choice(candidate_list)

    if chosen == "##NONE##":
        chosen = None

    if contains_none:
        candidate_list.remove("##NONE##")
    return chosen


if __name__ == '__main__':
    pass
