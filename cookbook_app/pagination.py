from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response



class RecipePagination(PageNumberPagination):
    page_size = 3


    def get_paginated_response(self, data):

        return Response({
            'links': {
               'next': self.get_next_link(),
               'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page_number': self.page.number,
            'results': data
        })
        
class UserPagination(PageNumberPagination):
    page_size = 5


    def get_paginated_response(self, data):

        return Response({
            'links': {
               'next': self.get_next_link(),
               'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page_number': self.page.number,
            'results': data
        })