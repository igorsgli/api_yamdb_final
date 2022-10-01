from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):

    message = 'Изменение чужого ревью запрещено!'

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)


class IsAdminOrAuthorOrReadOnly(permissions.BasePermission):

    message = 'Вы должны быть администратором или автором!'

    def has_object_permission(self, request, view, obj):
        return (request.user.role == 'admin'
                or obj.author == request.user
                or request.method in permissions.SAFE_METHODS
                )


class IsAdmin(permissions.BasePermission):

    message = 'Вы не являетесь администратором!'

    def has_permission(self, request, view):
        return request.user.role == 'admin'
