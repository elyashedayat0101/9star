from collections import OrderedDict

from rest_framework.pagination import LimitOffsetPagination as _LimitOffsetPagination
from rest_framework.response import Response


class LimitOffsetPagination(_LimitOffsetPagination):
    default_limit = 10
    max_limit = 50


def get_paginated_response(*, pagination_class, serializer_class, queryset, request, view):
    paginator = pagination_class()

    page = paginator.paginate_queryset(queryset, request, view=view)

    if page is not None:
        serializer = serializer_class(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    serializer = serializer_class(queryset, many=True)

    return Response(data=serializer.data)


def get_paginated_response_context(*, pagination_class, serializer_class, queryset, request, view):
    """Same as `get_paginated_response`, but returns the raw dict instead of a Response.

    Handy when you need to fold pagination data into a bigger response payload.
    """
    paginator = pagination_class()

    page = paginator.paginate_queryset(queryset, request, view=view)

    if page is not None:
        serializer = serializer_class(page, many=True)
        return OrderedDict(
            [
                ("limit", paginator.limit),
                ("offset", paginator.offset),
                ("count", paginator.count),
                ("next", paginator.get_next_link()),
                ("previous", paginator.get_previous_link()),
                ("results", serializer.data),
            ]
        )

    serializer = serializer_class(queryset, many=True)
    return OrderedDict([("results", serializer.data)])
