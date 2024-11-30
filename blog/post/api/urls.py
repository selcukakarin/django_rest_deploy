from django.urls import path, include

from post.api.views import PostListAPIView, PostDetailAPIView, PostDeleteAPIView, PostUpdateAPIView, PostCreateAPIView
from django.views.decorators.cache import cache_page
# 127.0.0.1:8000/api/post/list
app_name = "post"
urlpatterns = [
    path("list", cache_page(60*1)(PostListAPIView.as_view()), name='list'),
    path("detail/<slug>", PostDetailAPIView.as_view(), name='detail'),
    path("delete/<slug>", PostDeleteAPIView.as_view(), name='delete'),
    path("update/<slug>", PostUpdateAPIView.as_view(), name='update'),
    path("create/", PostCreateAPIView.as_view(), name='create'),
]
