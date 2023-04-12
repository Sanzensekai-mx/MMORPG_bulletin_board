from django.urls import path
from .views import ListPosts

urlpatterns = [
    path('all', ListPosts.as_view(), name='all'),
    # path('/profile'),
    # path('/profile/my_post')
]
