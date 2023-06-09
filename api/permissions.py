
from rest_framework.permissions import BasePermission
from api.models import ManagementUser, SalesUser, SupportUser


class IsAdminAuthenticated(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_superuser)


class IsAdminOrManager(BasePermission):

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        if ManagementUser.objects.filter(manager=request.user):
            return True
        return False


class SupportReadOnly(BasePermission):

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        if ManagementUser.objects.filter(manager=request.user):
            return True
        if SalesUser.objects.filter(seller=request.user):
            return True
        if SupportUser.objects.filter(support=request.user):
            if request.method == 'GET':
                return True
            else:
                return False
        return False
