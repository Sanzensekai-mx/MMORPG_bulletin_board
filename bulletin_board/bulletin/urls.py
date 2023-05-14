from django.urls import path
from .views import ListPosts, DetailPost, AddPost, UpdatePost, DeletePost, UserSelfPostsReplies, \
    AcceptReplyStatusAPIView, RejectReplyStatusAPIView, admin_send_news_mail_view

urlpatterns = [
    path('', ListPosts.as_view(), name='all'),
    path('bulletin/<int:pk>', DetailPost.as_view(), name='bulletin_detail'),
    path('bulletin/add', AddPost.as_view(), name='add_post'),
    path('bulletin/<int:pk>/edit', UpdatePost.as_view(), name='update_post'),
    path('bulletin/<int:pk>/delete', DeletePost.as_view(), name='delete_post'),
    path('bulletin/self_posts_replies', UserSelfPostsReplies.as_view(), name='user_post_replies'),
    path('api/reply_accept/<int:pk>/', AcceptReplyStatusAPIView.as_view(), name='accept_reply'),
    path('api/reply_reject/<int:pk>/', RejectReplyStatusAPIView.as_view(), name='reject_reply'),
    path('bulletin/send_news', admin_send_news_mail_view, name='admin_send_mail'),
]
