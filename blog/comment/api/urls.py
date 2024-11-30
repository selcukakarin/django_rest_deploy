from django.urls import path, include

from comment.api.views import CommentCreateAPIView, CommentListAPIView, CommentUpdateAPIView

app_name = "comment"
# 127.0.0.1:8000/api/comment/create/
urlpatterns = [
    path('create/', CommentCreateAPIView.as_view(), name='create'),
    path('list/', CommentListAPIView.as_view(), name='list'),
    # path('delete/<pk>', CommentDeleteAPIView.as_view(), name='delete'),
    path('update/<pk>', CommentUpdateAPIView.as_view(), name='update'),
]
