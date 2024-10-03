from rest_framework.pagination import PageNumberPagination




class CommentApiPagination(PageNumberPagination):
    page_size = 4
    page_size_query_param = 'page_size'
    max_page_size = 1000

class PostApiPagination(CommentApiPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 1000
