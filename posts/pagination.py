from rest_framework.pagination import PageNumberPagination




class CommentApiPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 1000

class PostApiPagination(CommentApiPagination):
    pass
