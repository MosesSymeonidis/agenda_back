class RequestValidation():
    @staticmethod
    def parameters_assertion(parameters):
        """
        Decorator for assertion parameters
        :param parameters:
        :return:
        """
        def assertions(func):
            def func_wrapper(self,*args,**kwargs):
                for parameter in parameters:
                    if parameter not in self.request.args:
                        raise Exception('Error parameter')
                return func(self,*args,**kwargs)
            return func_wrapper
        return assertions

    @staticmethod
    def parameter_assertion(dictionary, params):
        for val in params:
            if val not in dictionary:
                raise Exception('Error parameter')
        return True
