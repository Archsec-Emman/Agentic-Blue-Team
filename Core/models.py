import ast

from django.db import models


# Create your models here.

class DiyListField(models.TextField):
    """Used to store list type fields in the database"""
    description = "Stores a python list"

    def __init__(self, *args, **kwargs):
        super(DiyListField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        if value is None:
            return value

        return str(value)

    @staticmethod
    def from_db_value(value, expression, connection):
        if not value:
            value = []
        if isinstance(value, list):
            return value
        try:
            return ast.literal_eval(value)
        except Exception as E:
            from Lib.log import logger
            logger.exception(E)
            logger.error(value)
            return []

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)


class DiyDictField(models.TextField):
    """Used to store dict type fields in the database"""
    description = "Stores a python dict"

    def __init__(self, *args, **kwargs):
        super(DiyDictField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        if value is None:
            return value

        return str(value)

    def from_db_value(self, value, expression, connection):
        if not value:
            value = []
        if isinstance(value, dict):
            return value
        try:
            return ast.literal_eval(value)
        except Exception as E:
            from Lib.log import logger
            logger.exception(E)
            logger.error(value)
            return {}

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)
