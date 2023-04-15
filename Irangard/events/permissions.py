from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import permissions


# class IsIsAuthenticatedOrReadOnly(IsAuthenticated):
#     def has_permission(self, request, view):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         if request.method == 'destroy':
#             return IsAdminUser.has_permission(request, view)
#             # return request.user and request.user.is_staff
#         return super().has_permission(request, view) 

class EventPermission(IsAuthenticated):
    
    def has_permission(self, request, view):
        print(request)
        print(self)
        print(view)
        if request.method in permissions.SAFE_METHODS:
            return True
        # if view.action in ['update', 'partial_update', 'destroy']:
        #     return False
        return super().has_permission(request, view)
                                                                                                
    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            return True
        if view.action in ['update', 'partial_update', 'destroy']:
            return obj.added_by == request.user or request.user.is_admin
    
        return super().has_object_permission()