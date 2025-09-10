from rest_framework import permissions



class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role == "admin" or request.user.is_superuser:
            return True

        if request.method in permissions.SAFE_METHODS:  
            return True
        return obj.created_by == request.user

class IsSelfOrAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        
        if not request.user.is_authenticated:
            return False

        
        if getattr(request.user, "role", "").lower() == "admin" or request.user.is_superuser:
            return True

        return obj == request.user