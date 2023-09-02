from rest_framework.permissions import BasePermission
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet


class isContributor(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not obj.contributors:
            if obj.project:
                # In the case of an issue, the project is the parent
                return request.user in obj.project.contributors.all()
            if obj.issue:
                # In the case of a comment, the issue is the parent
                return request.user in obj.issue.project.contributors.all()
        return request.user in obj.contributors.all()


class isAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.author


def shared_get_permissions(self: ModelViewSet):
    if self.action == "list":
        permission_classes = [IsAuthenticated | IsAdminUser]
    if self.action == "destroy":
        permission_classes = [IsAdminUser | isAuthor]
    else:
        permission_classes = [IsAdminUser | isContributor | isAuthor]
    return [permission() for permission in permission_classes]
