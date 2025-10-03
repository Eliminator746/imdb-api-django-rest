from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination

class MovieListPagination(PageNumberPagination):
    page_size = 5
    max_page_size = 7
    
class MovieListLOPagination(LimitOffsetPagination):
    default_limit = 2
    max_limit = 7
    limit_query_param = 'limit'
    offset_query_param = 'start'
    
class MovieListCPagination(CursorPagination):
    page_size = 3
    cursor_query_param = 'record'
    ordering = '-avg_rating'