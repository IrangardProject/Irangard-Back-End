from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import permissions
from .models import Tour

class IsOwnerOrReadOnly(IsAuthenticated):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == 'destroy':
            return IsAdminUser.has_permission(request, view)
        
        if request.method in ['POST']:
            return request.user.is_special and super().has_permission(request, view) 

        return super().has_permission(request, view) 

    def has_object_permission(self, request, view, tour_obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method in ['PUT','POST','DELETE']:
            print(tour_obj.owner.user.id)
            print(request.user.id)
            return tour_obj.owner.user.id == request.user.id
        
class IsDiscountCodeOwnerOrReadOnly(IsAuthenticated):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == 'destroy':
            return IsAdminUser.has_permission(request, view)

        return super().has_permission(request, view) 

