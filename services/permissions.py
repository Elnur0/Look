from rest_framework.permissions import BasePermission, SAFE_METHODS


class CustomPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user


class HasAddDeletePermission(BasePermission):
    def has_delete_permission(self, request, obj=None):
        if request.user.email == 'admin@gmail.com':
            return True
        else:
            return False
        
    def has_add_permission(self, request):
        if request.user.email == 'admin@gmail.com':
            return True
        else:
            return False