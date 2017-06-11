from Utils.Exceptions.GeneralExceptions import ParameterDoesNotExists

class RequestValidation():
    @staticmethod
    def parameters_assertion(parameters,args_or_form='args'):
        """
        Decorator for assertion parameters
        :param parameters:
        :return:
        """
        def assertions(func):
            def func_wrapper(self,*args,**kwargs):
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
                return func(self,*args,**kwargs)

            return func_wrapper
        return assertions

    @staticmethod
    def parameter_assertion(dictionary, params):
        for val in params:
            if val not in dictionary:
                raise ParameterDoesNotExists(val)
        return True
