from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):

    message = 'Изменение чужого ревью запрещено!'

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)


class GeneralPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and
                    (request.user.is_staff or
                     request.user.role == 'admin') or
                    request.method in permissions.SAFE_METHODS)


class IsAdminOrAuthorOrReadOnly(permissions.BasePermission):

    message = 'Вы должны быть администратором или автором!'

    def has_object_permission(self, request, view, obj):
        return (request.user.role == 'admin'
                or obj.author == request.user
                or request.method in permissions.SAFE_METHODS
                )


class IsAdminOrModeratorOrAuthorOrReadOnly(permissions.BasePermission):

    message = 'Вы должны быть администратором, автором или модератором!'

    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS
            or request.user
            and request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in permissions.SAFE_METHODS
            or (
                not request.user.is_anonymous
                and (
                    request.user.role == 'admin'
                    or request.user.role == 'moderator'
                    or obj.author == request.user
                )
            )
        )


class IsAdmin(permissions.BasePermission):

    message = 'Вы не являетесь администратором!'

    def has_permission(self, request, view):
        return request.user.role == 'admin'


class AdminOnly(permissions.BasePermission):

    def has_permission(self, request, view):

        if (
            request.user.is_authenticated
            and request.user.role == 'admin'
        ):
            return True

        if (
            request.user.is_authenticated
            and request.user.role != 'admin'
            and request.user.is_superuser
        ):
            return True

        return False


class UserOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated