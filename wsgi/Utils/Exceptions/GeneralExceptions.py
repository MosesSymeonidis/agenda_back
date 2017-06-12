from Utils.Exceptions import BasicException

PREFIX_CODE = 'ge'

BASIC_ERROR_500 = {'error_code': PREFIX_CODE+'00', 'error_message': 'General Error'}

class ParameterDoesNotExists(BasicException):

    def __init__(self, parameter):
        self.message = 'Parameter ' + parameter + ' is missing'
        self.code = PREFIX_CODE+'01'
        self.parameters={'parameter': parameter}
