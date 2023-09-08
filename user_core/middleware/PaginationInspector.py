from collections import OrderedDict
from drf_yasg.inspectors import PaginatorInspector
from drf_yasg import openapi


class PageNumberPaginatorInspectorClass(PaginatorInspector):

    def get_paginated_response(self, paginator, response_schema):
        """
        :param BasePagination paginator: the paginator
        :param openapi.Schema response_schema: the response schema that must be paged.
        :rtype: openapi.Schema
        """

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
        """
        Get the pagination parameters for a single paginator **instance**.

        Should return :data:`.NotHandled` if this inspector does not know how to handle the given `paginator`.

        :param BasePagination paginator: the paginator
        :rtype: list[openapi.Parameter]
        """

        return [
            openapi.Parameter('page_size', openapi.IN_QUERY,
                              "Page Size", False, None, openapi.TYPE_INTEGER)
        ]
