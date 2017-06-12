from Utils.Exceptions import BasicException

PREFIX_CODE = 'bu'


class NotFoundFacetException(BasicException):
    def __init__(self, facet_name):
        self.message = 'Does not exists facet ' + facet_name
        self.code = PREFIX_CODE+'01'
        self.parameters = {'facet_name': facet_name}



class NotProperField(BasicException):

    def __init__(self, field_name):
        self.message = 'Does not exists field ' + field_name
        self.code = PREFIX_CODE+'02'
        self.parameters = {'field_name': field_name}
