from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.mixins import UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin, ListModelMixin

from comment.api.paginations import CommentPagination
from comment.api.permissions import IsOwner
from comment.api.serializers import CommentCreateSerializer, CommentListSerializer, CommentDeleteUpdateSerializer
from comment.models import Comment


class CommentCreateAPIView(CreateAPIView, ListModelMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class CommentListAPIView(ListAPIView):
    # queryset = Comment.objects.all()
    serializer_class = CommentListSerializer
    pagination_class = CommentPagination

    def get_queryset(self):
        # api/comment/list/?q=9
        queryset = Comment.objects.filter(parent=None)
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(post=query)
        return queryset


# class CommentDeleteAPIView(DestroyAPIView, UpdateModelMixin, RetrieveModelMixin):
#     queryset = Comment.objects.all()
#     serializer_class = CommentDeleteUpdateSerializer
#     lookup_field = 'pk'
#     permission_classes = [IsOwner]
#
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)


class CommentUpdateAPIView(UpdateAPIView, RetrieveModelMixin, DestroyModelMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentDeleteUpdateSerializer
    lookup_field = 'pk'
    permission_classes = [IsOwner]

    def get(self, request, *args, **kwargs):
        return self.retrieve(self, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
