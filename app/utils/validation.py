from utils.exceptions.general_exceptions import ParameterDoesNotExists, MethodError
import models

class RequestValidation(object):
    @staticmethod
    def parameters_assertion(parameters, args_or_form='args'):
        """
        Decorator for assertion parameters
        :param parameters:
        :return:
        """

        def assertions(func):
            def func_wrapper(self, *args, **kwargs):
                try:
                    if args_or_form == 'args':
                        for parameter in parameters:
                            if parameter not in self.request.args:
                                raise ParameterDoesNotExists(parameter)
                    elif args_or_form == 'form':
                        for parameter in parameters:
                            if parameter not in self.request.form:
                                raise ParameterDoesNotExists(parameter)
                    else:
                        for parameter in parameters:
                            if parameter not in self.request.get_json():
                                raise ParameterDoesNotExists(parameter)
                except TypeError:
                    raise MethodError(type=args_or_form)
                return func(self, *args, **kwargs)

            return func_wrapper

        return assertions

    @staticmethod
    def parameter_assertion(dictionary, params):
        for val in params:
            if val not in dictionary:
                raise ParameterDoesNotExists(val)
        return True

def permission_validator(*external_args):
    def validator(func):
        def func_wrapper(self, *args, **kwargs):
            from flask import g as global_storage
            user = global_storage.user
            for arg in external_args:
                per_level = arg.split('.')
                if per_level[0] == 'business': # business.admin.edit_professionals
                    configs = models.Config.objects.get(config_id='general')
                    business = kwargs['business'] if 'business' in kwargs else None
                    if business is None:
                        raise Exception
                    business_doc = None
                    for i in getattr(user, per_level[1]):
                        if i.business == business.id:
                            business_doc = i
                            break
                    if business_doc is None:
                        raise Exception
                    # if edit_professionals is in business_doc['permissions'] or in role permissions
                    if per_level[2] not in business_doc['permissions'] and per_level[2] not in configs['roles'][per_level[1]]['permissions']:
                        raise Exception
                else:
                    if per_level not in user.permissions:
                        raise Exception

            return func(self, *args, **kwargs)

        return func_wrapper

    return validator