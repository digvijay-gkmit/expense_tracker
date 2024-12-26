# your_project/utils/pagination.py

class CustomPagination:
    def __init__(self, page_size=10):
        self.page_size = page_size

    def paginate_queryset(self, queryset, page):
        """
        Paginate a queryset or list based on the current page and page size.
        """
        total_count = len(queryset)
        start = (page - 1) * self.page_size
        end = start + self.page_size

        # Handle invalid page numbers
        if start >= total_count or page < 1:
            return [], total_count

        return queryset[start:end], total_count

    def get_paginated_response(self, data, total_count, page):
        """
        Return a structured response with pagination metadata.
        """
        total_pages = (total_count + self.page_size - 1) // self.page_size

        return {
            "page": page,
            "page_size": self.page_size,
            "total_items": total_count,
            "total_pages": total_pages,
            "next": page + 1 if page < total_pages else None,
            "previous": page - 1 if page > 1 else None,
            "results": data,
        }
