from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class MessagePagination(PageNumberPagination):
    page_size = 300
    page_query_param = 'page'

    def get_paginated_response(self, data):
        data.update({
            'next': self.get_next_link(),
            # 'count': self.page.paginator.count,
        })
        return Response(data)