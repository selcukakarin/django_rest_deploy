from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        print("has_permission çalıştı")
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        print("has_object_permission çalıştı...")
        return obj.user == request.user
