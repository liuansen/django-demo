# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.backends.mysql.base import DatabaseWrapper as BaseDatabaseWrapper
from .schema import DatabaseSchemaEditor
from django.utils.functional import cached_property


class DatabaseWrapper(BaseDatabaseWrapper):

    SchemaEditorClass = DatabaseSchemaEditor

    def __init__(self, *args, **kwargs):
        super(DatabaseWrapper, self).__init__(*args, **kwargs)


    def init_connection_state(self):
        pass

    @cached_property
    def mysql_version(self):
        return (5, 6, 16)