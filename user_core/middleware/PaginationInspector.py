from collections import OrderedDict
from drf_yasg.inspectors import PaginatorInspector
from drf_yasg import openapi


class PageNumberPaginatorInspectorClass(PaginatorInspector):

    def get_paginated_response(self, paginator, response_schema):
        return openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties=OrderedDict((
                ('count', openapi.Schema(type=openapi.TYPE_INTEGER)),
                ('page_size', openapi.Schema(type=openapi.TYPE_INTEGER)),
                ('total_pages', openapi.Schema(type=openapi.TYPE_INTEGER)),
                ('current_page', openapi.Schema(type=openapi.TYPE_INTEGER)),
                ('results', response_schema),
            )),
            required=['results']
        )

    def get_paginator_parameters(self, paginator):
        return [
            openapi.Parameter('page_size', openapi.IN_QUERY,
                              "Page Size", False, None, openapi.TYPE_INTEGER)
        ]
