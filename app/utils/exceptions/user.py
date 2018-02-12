from utils.exceptions import BasicException

PREFIX_CODE = 'us'


class RoleError(BasicException):
    def __init__(self, role):
        self.message = 'The proper role of user should be ' + role
        self.code = PREFIX_CODE + '01'
        self.parameters = {'role': role}


class MaxBusinessLimit(BasicException):
    def __init__(self, plan):
        self.message = 'You can not add more shops at ' + plan + ' plan'
        self.code = PREFIX_CODE + '02'
        self.parameters = {'plan': plan}


class UserHasNotPlan(BasicException):
    def __init__(self):
        self.message = 'You have not any plan yet'
        self.code = PREFIX_CODE + '03'
