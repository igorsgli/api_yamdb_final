from rest_framework import permissions


class GeneralPermission(permissions.BasePermission):

    message = 'У Вас не достаточно прав для выполнения операции!'

    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated
            and (request.user.is_staff or request.user.is_admin)
            or request.method in permissions.SAFE_METHODS)


class IsAdminOrModeratorOrAuthorOrReadOnly(permissions.BasePermission):

    message = (
        'Операция доступна только для администратора, '
        'автора или модератора!'
    )

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in permissions.SAFE_METHODS
            or (
                not request.user.is_anonymous
                and (
                    request.user.is_admin
                    or request.user.is_moderator
                    or obj.author == request.user
                )
            )
        )


class AdminOnly(permissions.BasePermission):

    message = 'Вы не являетесь администратором!'

    def has_permission(self, request, view):
        return (
            not request.user.is_anonymous and (
                request.user.is_admin
                or request.user.is_superuser
            )
        )
