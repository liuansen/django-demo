# -*-coding:utf-8-*-
from __future__ import unicode_literals
import urlparse

from django.contrib.admindocs.utils import trim_docstring
from rest_framework import exceptions, renderers, serializers
from rest_framework.schemas import SchemaGenerator as BaseSchemaGenerator
from rest_framework.schemas.generators import get_pk_name, LinkNode, insert_into
from rest_framework.compat import coreapi
from rest_framework.permissions import AllowAny
from rest_framework.renderers import CoreJSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.utils.field_mapping import ClassLookupDict
from rest_framework_swagger import renderers


class SchemaGenerator(BaseSchemaGenerator):
    '''
        自定义
    '''

    def coerce_path(self, path, method, view):
        """
        Coerce {pk} path arguments into the name of the model field,
        where possible. This is cleaner for an external representation.
        (Ie. "this is an identifier", not "this is a database primary key")
        """
        if not self.coerce_path_pk or '{pk}' not in path:
            return path

        model = getattr(getattr(view, 'queryset', None), 'model', None)
        if model:
            field_name = get_pk_name(model)
            path = path.replace('{pk}', '{%s}' % field_name)

        return path

    def get_links(self, request=None):
        links = LinkNode()
        # Generate (path, method, view) given (path, method, callback).
        paths = []
        view_endpoints = []
        for path, method, callback in self.endpoints:
            view = self.create_view(callback, method, request)
            path = self.coerce_path(path, method, view)
            paths.append(path)
            view_endpoints.append((path, method, view))

        # Only generate the path prefix for paths that will be included
        if not paths:
            return None
        prefix = self.determine_path_prefix(paths)

        for path, method, view in view_endpoints:
            if not self.has_view_permissions(path, method, view):
                continue
            fields = view.schema.get_path_fields(path, method)
            fields += view.schema.get_serializer_fields(path, method)
            fields += view.schema.get_pagination_fields(path, method)
            fields += view.schema.get_filter_fields(path, method)

            manual_fields = view.schema.get_manual_fields(path, method)
            fields = view.schema.update_fields(fields, manual_fields)

            if fields and any([field.location in ('form', 'body') for field in fields]):
                encoding = view.schema.get_encoding(path, method)
            else:
                encoding = None

            description = view.schema.get_description(path, method)
            if description and len(description) > 0:
                query_fields, description = self.get_docstring_fields(
                    description)
                fields += query_fields
            if self.url and path.startswith('/'):
                path = path[1:]

            link = coreapi.Link(
                url=urlparse.urljoin(self.url, path),
                action=method.lower(),
                encoding=encoding,
                fields=fields,
                description=description
            )

            subpath = path[len(prefix):]
            keys = self.get_keys(subpath, method, view)
            insert_into(links, keys, link)

        return links

    def get_docstring_fields(self, description):
        # bubble modify(add) 
        fields = []
        split_lines = trim_docstring(description).split('\n')
        temp_lines = []

        for line in split_lines:
            param = line.split(' -- ')
            if len(param) == 2:
                fields.append(coreapi.Field(name=param[0].strip(),
                                            required=False,
                                            location='query',
                                            description=param[1].strip()))
            else:
                temp_lines.append(line)
                temp_lines.append('\n')

        description = ''.join(temp_lines)

        return fields, description


def get_swagger_view(title=None, url=None, patterns=None, urlconf=None):
    """
    Returns schema view which renders Swagger/OpenAPI.
    """
    class SwaggerSchemaView(APIView):
        _ignore_model_permissions = True
        exclude_from_schema = True
        permission_classes = [AllowAny]
        renderer_classes = [
            CoreJSONRenderer,
            renderers.OpenAPIRenderer,
            renderers.SwaggerUIRenderer
        ]

        def get(self, request):
            generator = SchemaGenerator(
                title=title,
                url=url,
                patterns=patterns,
                urlconf=urlconf
            )
            schema = generator.get_schema(request=request)

            if not schema:
                raise exceptions.ValidationError(
                    'The schema generator did not return a schema Document'
                )

            return Response(schema)

    return SwaggerSchemaView.as_view()