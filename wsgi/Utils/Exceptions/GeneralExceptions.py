from Utils.Exceptions import BasicException

PREFIX_CODE = 'ge'

BASIC_ERROR_500 = {'error_code': PREFIX_CODE+'00', 'error_message': 'General Error', 'parameters': {} }

BASIC_ERROR_404 = {'error_code': PREFIX_CODE+'01', 'error_message': 'Not Found Error', 'parameters': {}}

class ParameterDoesNotExists(BasicException):

    def __init__(self, parameter):
        self.message = 'Parameter ' + parameter + ' is missing'
        self.code = PREFIX_CODE+'11'
        self.parameters={'parameter': parameter}
