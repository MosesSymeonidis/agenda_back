from aggregation_builder import AggregateQuerySet
from mongoengine import Document, DynamicDocument, queryset_manager

from utils.base import ModelConverter


class BaseDocument(Document):
    meta = {'abstract': True}

    __converter__ = ModelConverter

    @queryset_manager
    def objects(cls, query_Set):
        """
        This method overrides the class of query_set of python
        :param query_Set: The mongoengine queryset
        :return: The override queryset
        """
        query_Set.__class__ = AggregateQuerySet
        return query_Set

    @classmethod
    def get_converter(cls):
        """
        Util method for creating the class model converter
        :return: A model converter class
        """

        class Temp(cls.__converter__):
            model = cls

        return Temp


class BaseDynamicDocument(DynamicDocument, BaseDocument):
    meta = {'abstract': True}
