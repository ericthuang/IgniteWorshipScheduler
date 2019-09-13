import Util as u

class Band:
    def __init__(self):
        for role in u.ROLES:
            exec("self." + role + " = None")  # init list to store userEmail

    def assign_role(self, role, email):
        exec ("self." + role + " = " + email)

