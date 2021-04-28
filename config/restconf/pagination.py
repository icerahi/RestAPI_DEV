from rest_framework import permissions,generics,pagination

class CustomAPIPagination(pagination.LimitOffsetPagination): # PageNumberPagination):
    #page_size = 3
    default_limit = 2
    max_limit   = 20
   # limit_query_param = "lim"
