import random as r

class Band:
    def __init__(self, role_params, availability_matrix_date_slice):
        self.availability = availability_matrix_date_slice # role -> primary/secondary -> list of emails
        self.band_members = dict()  # key: role, value: list of members
        self.emails = set()
        self.role_params = role_params

        for role in self.role_params.keys():
            self.band_members[role] = list()

    def _prune_candidates(self, candidate_list):
        if not len(candidate_list):
            return list()
        # remove people already serving
        for cand in candidate_list:
            if cand in self.emails:
                candidate_list.remove(cand)
        # other pruning here

        return candidate_list

    def generate_band(self):
        for role in self.band_members.keys():
            required_minimum = self.role_params[role]['minCountPerTeam']

            # prune candidates list, remove people who are already serving in this set
            # (combo filling will implicitly be taken care of)
            pruned_primary_candidates = self._prune_candidates(self.availability[role]['primary'])
            pruned_secondary_candidates = self._prune_candidates(self.availability[role]['secondary'])

            # if there are 0 candidates available (both primary and secondary) for this role
            if len(pruned_primary_candidates) == 0 and len(pruned_secondary_candidates) == 0:
                # nothing we can do regardless of whether required_minimum is 0
                self.assign_role(role, None)
            else:
                candidates = pruned_primary_candidates
                if required_minimum != 0 and len(candidates) == 0:
                    # if we need at least 1 and there are no primary candidates, look in secondary
                    candidates = pruned_secondary_candidates # guaranteed non-empty

                # At this point, candidates can be either empty or filled with secondary candidates, both are fine.
                # If required minimum is not 0, and no primary candidates available, candidates will remain empty
                # and "NONE" will be sampled, leaving the position vacant

                # in case there are too many options haha
                max_that_can_be_assigned = min(len(candidates), self.role_params[role]['maxCountPerTeam'])
                if max_that_can_be_assigned == 0:
                    continue
                elif max_that_can_be_assigned == 1:
                    number_candidates_to_assign = 1
                else:
                    probability_array_for_multi_member_role = list()
                    for i in range(max_that_can_be_assigned):
                        probability_array_for_multi_member_role += [i+1 for x in range(max_that_can_be_assigned - i)]
                    number_candidates_to_assign = choose_random_element(probability_array_for_multi_member_role)

                while number_candidates_to_assign > 0:
                    if len(self.band_members[role]) < required_minimum:
                        random_person = choose_random_element(candidates, 0) # no Nones allowed
                    else:
                        random_person = choose_random_element(candidates, 1) # otherwise it's ok to omit

                    if random_person: # if it's not a None
                        candidates.remove(random_person) # so they don't get picked again
                        self.assign_role(role, random_person)
                    number_candidates_to_assign -= 1

        print(self.band_is_complete())

    def band_is_complete(self):
        for role in self.role_params:
            if len(self.band_members[role]) < self.role_params[role]['minCountPerTeam']:
                return False
        return True

    def assign_role(self, role, email):
        if not email or not role:
            return
        self.band_members[role].append(email)
        # add combo if available

        possible_combos = list() # randomly pick from this list
        for role in self.role_params[role]['possibleCombos']:
            if len(self.band_members[role]) < self.role_params[role]['maxCountPerTeam'] \
                    and role in self.availability[role]['primary']:
                possible_combos.append(role)
        if len(possible_combos) != 0:
            chosen_combo_role = choose_random_element(possible_combos, 0)
            self.band_members[chosen_combo_role].append(email)
        self.emails.add(email)

    def get_band_dict(self):
        return self.band_members


def choose_random_element(candidate_list, none_count = 0):
    if none_count:
        for i in range(none_count):
            candidate_list.append("##NONE##")

    chosen = r.choice(candidate_list)

    if chosen == "##NONE##":
        return None
    return chosen

if __name__ == '__main__':
    pass





