from mongoengine.errors import *

MONGO_PREFIX = 'mo'

errors = {
    DoesNotExist: {'error_code': MONGO_PREFIX+'01', 'error_message': 'Entity does not exist'},
    NotRegistered: {'error_code': MONGO_PREFIX+'02', 'error_message': 'Model is not register'},
    InvalidDocumentError: {'error_code': MONGO_PREFIX+'03', 'error_message': 'Invalid document'},
    LookUpError: {'error_code': MONGO_PREFIX+'04', 'error_message': 'Value does not valid'},
    MultipleObjectsReturned: {'error_code': MONGO_PREFIX+'05', 'error_message': 'Try to get one document but there are more than one'},
    InvalidQueryError: {'error_code': MONGO_PREFIX+'06', 'error_message': 'Invalid query'},
    OperationError: {'error_code': MONGO_PREFIX+'07', 'error_message': 'Operation Error'},
    NotUniqueError: {'error_code': MONGO_PREFIX+'08', 'error_message': 'The entity exists'},
    # FieldDoesNotExist: {'error_code': MONGO_PREFIX+'09', 'error_message': 'Field does not exists'},
    ValidationError: {'error_code': MONGO_PREFIX+'10', 'error_message': 'Field Validation Error'},
    SaveConditionError: {'error_code': MONGO_PREFIX+'11', 'error_message': 'Error at saving data'},
}
