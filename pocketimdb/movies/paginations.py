from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

DEFAULT_PAGE = 1

class CustomPageNumberPagination(PageNumberPagination):
    page = DEFAULT_PAGE
    page_size = 10

    def get_paginated_response(self, data):
        return Response({
            'total': self.page.paginator.count,
            'page': int(self.request.GET.get('page', DEFAULT_PAGE)),
            'page_size': self.page_size,
            'results': data
        })