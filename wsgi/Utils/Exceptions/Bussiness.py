from Utils.Exceptions import BasicException

PREFIX_CODE = 'bu'


class NotFoundFacetException(BasicException):
    def __init__(self, facet_name):
        self.message = 'Does not exists facet ' + facet_name
        self.code = PREFIX_CODE+'01'


class NotProperField(BasicException):

    def __init__(self, field_name):
        self.message = 'Does not exists facet ' + field_name
        self.code = PREFIX_CODE+'02'
