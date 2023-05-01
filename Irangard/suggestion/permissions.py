from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import permissions


class SuggestionPermission(IsAuthenticated):
    
    def has_permission(self, request, view):
        if view.action == 'list':
            return request.user.is_superuser
        return super().has_permission(request, view)
    
    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            return obj.sender == request.user or obj.receiver == request.user \
                or request.user.is_superuser
        if view.action in ['update', 'partial_update', 'destroy']:
            return obj.sender == request.user or request.user.is_staff
        return False
    