from rest_framework.permissions import IsAdminUser, IsAuthenticated, BasePermission
from rest_framework import permissions, status

from chat.models import UserInRoom


class IsRoomMember(BasePermission):
    def has_permission(self, request, view):
        return UserInRoom.objects.filter(user=request.user, room_id=view.kwargs['pk']).exists()
