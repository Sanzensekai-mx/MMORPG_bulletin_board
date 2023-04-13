from django.urls import path
from .views import ListPosts, DetailPost

urlpatterns = [
    path('all', ListPosts.as_view(), name='all'),
    path('bulletin/<int:pk>', DetailPost.as_view(), name='bulletin_detail'),
    # path('/profile/my_post')
]
