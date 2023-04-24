from django.urls import path
from .views import ListPosts, DetailPost, AddPost

urlpatterns = [
    path('all', ListPosts.as_view(), name='all'),
    path('bulletin/<int:pk>', DetailPost.as_view(), name='bulletin_detail'),
    path('bulletin/add', AddPost.as_view(), name='add_post')
    # path('/profile/my_post')
]
