from rest_framework.response import Response
from urllib.parse import urlencode


class CustomPagination:
    def __init__(self, page_size=2):
        self.page_size = page_size

    def paginate_queryset(self, queryset, request):
        """
        Paginates the queryset manually based on page size and page number.

        queryset: The queryset to paginate
        request: The request object that contains pagination params
        """

        page_size = int(request.query_params.get("page_size", self.page_size))

        page_number = int(request.query_params.get("page", 1))

        offset = (page_number - 1) * page_size
        limit = page_size

        paginated_queryset = queryset[offset : offset + limit]

        return paginated_queryset, queryset.count()

    def get_paginated_response(self, data, request, total_count):
        """
        Builds the paginated response.
        """
        page_size = int(request.query_params.get("page_size", self.page_size))
        total_pages = (total_count + page_size - 1) // page_size
        page_number = int(request.query_params.get("page", 1))

        if page_number < total_pages:
            next = self.get_url(page_number + 1, request)
        else:
            next = None

        if page_number > 1:
            previous = self.get_url(page_number - 1, request)
        else:
            previous = None

        pagination_metadata = {
            "count": total_count,
            "next": next,
            "previous": previous,
            "results": data,
        }
        return Response(pagination_metadata)

    def get_url(self, page_number, request):
        """
        Generates the URL for the next page.
        """
        query_params = request.query_params.copy()
        query_params["page"] = page_number
        return f"{request.build_absolute_uri(request.path)}?{urlencode(query_params)}"
