from django.urls import path
from .views import ListPosts, DetailPost, AddPost, UpdatePost, DeletePost, UserSelfPostsReplies

urlpatterns = [
    path('', ListPosts.as_view(), name='all'),
    path('bulletin/<int:pk>', DetailPost.as_view(), name='bulletin_detail'),
    path('bulletin/add', AddPost.as_view(), name='add_post'),
    path('bulletin/<int:pk>/edit', UpdatePost.as_view(), name='update_post'),
    path('bulletin/<int:pk>/delete', DeletePost.as_view(), name='delete_post'),
    path('bulletin/self_posts_replies', UserSelfPostsReplies.as_view(), name='user_post_replies')
    # path('upload/', PostUploadView.as_view(), name='post_upload')
]
