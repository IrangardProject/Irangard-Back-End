from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import permissions


class IsIsAuthenticatedOrReadOnly(IsAuthenticated):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == 'destroy':
            return IsAdminUser.has_permission(request, view)
            # return request.user and request.user.is_staff
        return super().has_permission(request, view) 

