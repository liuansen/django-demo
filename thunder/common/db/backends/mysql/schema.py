# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db.backends.mysql.schema import DatabaseSchemaEditor as BaseDatabaseSchemaEditor


class DatabaseSchemaEditor(BaseDatabaseSchemaEditor):
    sql_alter_column_no_default = ""
    sql_alter_column_no_default_bak = "ALTER COLUMN %(column)s DROP DEFAULT"
    sql_alter_column_default_null = "ALTER COLUMN %(column)s SET DEFAULT NULL"
    sql_rename_column = "ALTER TABLE %(table)s CHANGE %(old_column)s %(new_column)s %(type)s %(default)s"

    def column_sql(self, model, field, include_default=False):
        '''
        修改 设置字段允许为NULL时，增加DEFAULT NULL
        修改 include_default为FALSE时，有设置DEFAULT的值列设置DEFAULT，方法的不设置
        '''
        # Get the column's type and use that as the basis of the SQL
        db_params = field.db_parameters(connection=self.connection)
        sql = db_params['type']
        params = []
        # Check for fields that aren't actually columns (e.g. M2M)
        if sql is None:
            return None, None
        # Work out nullability
        null = field.null

        ############# modify 20170420 ###################
        # If we were told to include a default value, do so
        if not self.skip_default(field):
            include_default = self._has_default(field) \
                if not include_default else include_default

            if include_default:
                default_value = self.effective_default(field)
                if default_value is not None:
                    if self.connection.features.requires_literal_defaults:
                        # Some databases can't take defaults as a parameter (oracle)
                        # If this is the case, the individual schema backend should
                        # implement prepare_default
                        sql += " DEFAULT %s" % self.prepare_default(default_value)
                    else:
                        sql += " DEFAULT %s"
                        params += [default_value]
                else:
                    if field.null:
                        # 没有DEFAULT，可允许为空，需要设置DEFAULT NULL
                        sql += ' DEFAULT NULL'
        ############# modify end ###################

        # Oracle treats the empty string ('') as null, so coerce the null
        # option whenever '' is a possible value.
        if (field.empty_strings_allowed and not field.primary_key and
                self.connection.features.interprets_empty_strings_as_nulls):
            null = True
        if null and not self.connection.features.implied_column_null:
            sql += " NULL"
        elif not null:
            sql += " NOT NULL"
        # Primary key/unique outputs
        if field.primary_key:
            sql += " PRIMARY KEY"
        elif field.unique:
            sql += " UNIQUE"
        # Optionally add the tablespace if it's an implicitly indexed column
        tablespace = field.db_tablespace or model._meta.db_tablespace
        if tablespace and self.connection.features.supports_tablespaces and field.unique:
            sql += " %s" % self.connection.ops.tablespace_sql(tablespace, inline=True)
        # Return the sql
        return sql, params

    def add_field(self, model, field):
        '''
        修改 当DEFAULT为方法生成的时，要删除DEFAULT，其它情况保留DEFAULT
        '''
        super(DatabaseSchemaEditor, self).add_field(model, field)

        # 删除不需要保留的default
        result = self._del_auto_default(model, field)
        if field.null and result:
            # 删除默认值，又允许空，那要设置default null
            self._set_default_null(model, field)


    def _alter_field(self, model, old_field, new_field, old_type, new_type,
                     old_db_params, new_db_params, strict=False):
        '''
        调用父类方法前，当新字段没有default而旧的有时，先删除
        调完后，删除不需要保留的default
        '''
        old_has_default = self._has_default(old_field)
        new_has_default = self._has_default(new_field)

        if old_has_default and not new_has_default:
            # 新的字段没有default,删除
            self._del_default(model, old_field)
                
        super(DatabaseSchemaEditor, self)._alter_field(model, old_field, 
            new_field, old_type, new_type, old_db_params, new_db_params, strict)

        # 删除不需要保留的default
        result = self._del_auto_default(model, new_field)
        if new_field.null and (result or self.effective_default(new_field) is None):
            # 没设置default或有设置但被删了，但可为空,设置default null
            self._set_default_null(model, new_field)

    def _rename_field_sql(self, table, old_field, new_field, new_type):
        ''' 列重命令操作语句'''

        default_value = ''
        if not self.skip_default(new_field):
            default = self.effective_default(new_field)
            if default is not None:
                default_value = 'DEFAULT {0}'.format(default)
            else:
                if new_field.null:
                    # 没有DEFAULT，可允许为空，需要设置DEFAULT NULL
                    default_value = ' DEFAULT NULL'

        return self.sql_rename_column % {
            "table": self.quote_name(table),
            "old_column": self.quote_name(old_field.column),
            "new_column": self.quote_name(new_field.column),
            "type": new_type,
            "default": default_value
        }


    def _has_default(self, field):
        '''
        字段是否有设置default
        '''
        if self.skip_default(field):
            return False

        if field.null:
            # 允许为空，不管有没有设置DEFAULT都会有
            return True

        if field.has_default():
            default = field.default
            if default is not None and not callable(default):
                return True
        if field.blank and field.empty_strings_allowed:
            return True

        return False

    
    def _del_auto_default(self, model, field):
        '''
        删除自动生成的DEFAULT，如方法、auto_now、auto_now_add
        '''
        if self.skip_default(field):
            return False

        default = None
        if field.has_default():
            default = field.default

        if getattr(field, 'auto_now', False) or \
            getattr(field, 'auto_now_add', False) or \
            (default is not None and callable(default)):
            # 删除DEFAULT
            self._del_default(model, field)
            return True

        return False


    def _del_default(self, model, field):
        '''
        删除DEFAULT
        '''
        sql = self.sql_alter_column % {
            "table": self.quote_name(model._meta.db_table),
            "changes": self.sql_alter_column_no_default_bak % {
                "column": self.quote_name(field.column)
                }
            }

        self.execute(sql)


    def _set_default_null(self, model, field):
        '''
        设置DEFAULT NULL
        '''
        sql = self.sql_alter_column % {
            "table": self.quote_name(model._meta.db_table),
            "changes": self.sql_alter_column_default_null % {
                "column": self.quote_name(field.column)
                }
            }

        self.execute(sql)
